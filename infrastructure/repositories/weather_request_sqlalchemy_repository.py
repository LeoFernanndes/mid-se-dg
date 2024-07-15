from sqlalchemy.orm import Session
from typing import List

from domain.models.weather_request import WeatherRequest
from application.repositories.weather_request_repository import WeatherRequestRepository


class WeatherRequestSqlalchemyRepository(WeatherRequestRepository):
    def __init__(self, db_session: Session):
        self._db_session = db_session

    def get_by_id(self, id: str) -> WeatherRequest:
        return self._db_session.query(WeatherRequest).filter(WeatherRequest.id == id).first()

    def filter_uncompleted(self) -> List[WeatherRequest]:
        return self._db_session.query(WeatherRequest).filter(WeatherRequest.completed == False).all()

    def save(self, weather_request: WeatherRequest) -> WeatherRequest:
        self._db_session.add(weather_request)
        self._db_session.commit()
        self._db_session.refresh(weather_request)
        return weather_request
