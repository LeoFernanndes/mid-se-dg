from datetime import datetime
from pydantic import BaseModel


class WeatherDataApiDto(BaseModel):
    city_id: str
    humidity: float
    temperature_celsius: float
    timestamp: datetime


class WeatherDataBaseDto(BaseModel):
    city_id: str
    humidity: float
    ow_request_timestamp: datetime
    request_id: str
    temperature_celsius: float
    user_request_timestamp: datetime


class WeatherDataInputDto(WeatherDataBaseDto):
    pass


class WeatherDataOutputDto(WeatherDataBaseDto):
    id: int


class WeatherRetrievalStatusInputDto(BaseModel):
    id: str


class WeatherRetrievalStatusOutputDto(WeatherRetrievalStatusInputDto):
    percentage_status: float
    timestamp: datetime
