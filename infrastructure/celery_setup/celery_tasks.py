import logging

from sqlalchemy.orm import Session

from application.dtos.weather_data import WeatherDataInputDto
from application.services.weather import WeatherService
from infrastructure.celery_setup.celery_config import celery_app
from domain.city_ids import city_ids
from infrastructure.repositories.weather_data_sqlalchemy_repository import WeatherDataSqlalchemyRepository
from infrastructure.repositories.weather_request_sqlalchemy_repository import WeatherRequestSqlalchemyRepository
from infrastructure.persistence.database import SessionLocal


logger = logging.getLogger(__name__)


db_ = SessionLocal()


@celery_app.task(name="celery_tasks.periodic")
def periodic(db: Session = db_):
    import time
    time.sleep(1)
    try:
        weather_data_sqlalchemy_repository = WeatherDataSqlalchemyRepository(db)
        weather_request_sqlalchemy_repository = WeatherRequestSqlalchemyRepository(db)
        weather_service = WeatherService(weather_data_sqlalchemy_repository, weather_request_sqlalchemy_repository)

        uncompleted_weather_requests = weather_service.list_uncompleted_weather_requests()
        if not uncompleted_weather_requests:
            logger.info('No uncompleted task.')
            return None
        older_weather_request = uncompleted_weather_requests[0]
        retrieved_weather_data = weather_service.filter_retrieved_weather_data_by_request_id(older_weather_request.id)
        retrieved_city_ids = [d.city_id for d in retrieved_weather_data]
        str_city_ids = [str(city_id) for city_id in city_ids]
        pending_city_ids = set(str_city_ids) - set(retrieved_city_ids)
        if not pending_city_ids:
            weather_service.update_weather_request_to_complete(older_weather_request.id)
            logger.info('No pending city to be retrieve.')
            return None
        city_id_to_be_retrieved = list(pending_city_ids)[0]
        weather_api_data = weather_service.request_weather_data_for_city_id(str(city_id_to_be_retrieved))
        logger.info('Requested weather api data.')
        weather_data_input_dto = WeatherDataInputDto(city_id=weather_api_data.city_id, humidity=weather_api_data.humidity,
                                                     ow_request_timestamp=weather_api_data.timestamp, request_id=older_weather_request.id,
                                                     temperature_celsius=weather_api_data.temperature_celsius, user_request_timestamp=older_weather_request.timestamp)
        weather_data_output_dto = weather_service.save_weather_data(weather_data_input_dto)
        return weather_data_output_dto.model_dump()
    except Exception as e:
        db.close()
        return str(e)
    finally:
        db.close()
