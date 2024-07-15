from typing import List

from sqlalchemy.orm import Session

from domain.models import WeatherData
from application.repositories.weather_data_repository import WeatherDataRepository


class WeatherDataSqlalchemyRepository(WeatherDataRepository):
    def __init__(self, db_session: Session):
        self._db_session = db_session

    def filter_by_request_id(self, id: str) -> List[WeatherData]:
        return self._db_session.query(WeatherData).filter(WeatherData.request_id == id).all()

    def save(self, weather_data: WeatherData) -> WeatherData:
        self._db_session.add(weather_data)
        self._db_session.commit()
        self._db_session.refresh(weather_data)
        return weather_data
