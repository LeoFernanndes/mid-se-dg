from abc import ABC
from datetime import datetime
from pydantic import BaseModel


class WeatherRequestBaseDto(ABC, BaseModel):
    id: str
    # timestamp: datetime = datetime.now()


class WeatherRequestInputDto(WeatherRequestBaseDto):
    pass


class WeatherRequestOutputDto(WeatherRequestBaseDto):
    timestamp: datetime
    completed: bool
