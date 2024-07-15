import logging

from dotenv import load_dotenv
from fastapi import Depends, HTTPException, APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from application.dtos.weather_data import WeatherRetrievalStatusInputDto
from application.dtos.weather_request import WeatherRequestInputDto
from infrastructure.persistence.database import SessionLocal
from infrastructure.repositories.weather_data_sqlalchemy_repository import WeatherDataSqlalchemyRepository
from infrastructure.repositories.weather_request_sqlalchemy_repository import WeatherRequestSqlalchemyRepository
from application.services.weather import WeatherService


load_dotenv()
logger = logging.getLogger(__name__)

router = APIRouter(prefix="")


def get_weather_service():
    db = SessionLocal()
    try:
        weather_data_repository = WeatherDataSqlalchemyRepository(db)
        weather_request_repository = WeatherRequestSqlalchemyRepository(db)
        yield WeatherService(weather_data_repository=weather_data_repository, weather_request_repository=weather_request_repository)
    finally:
        db.close()


@router.post("/")
def create_weather_request(weather_request_dto: WeatherRequestInputDto, weather_service: WeatherService = Depends(get_weather_service)):
    weather_request = weather_service.get_weather_request_by_id(weather_request_dto.id)
    if weather_request:
        raise HTTPException(detail=f"Id {weather_request_dto.id} is already in use.", status_code=400)
    created_weather_request_dto = weather_service.save_weather_request(weather_request_dto)
    return JSONResponse(content=jsonable_encoder(created_weather_request_dto), status_code=201)


@router.get("/{weather_request_id}")
def get_retrieval_status(weather_request_id: str, weather_service: WeatherService = Depends(get_weather_service)):
    weather_request = weather_service.get_weather_request_by_id(weather_request_id)
    if not weather_request:
        raise HTTPException(404)
    weather_retrieval_status_input_dto = WeatherRetrievalStatusInputDto(id=weather_request_id)
    weather_retrieval_status_output_dto = weather_service.get_weather_request_retrieval_status(weather_retrieval_status_input_dto)
    return JSONResponse(jsonable_encoder(weather_retrieval_status_output_dto))
