from abc import ABC, abstractmethod
from typing import List

from domain.models.weather_data import WeatherData


class WeatherDataRepository(ABC):

    @abstractmethod
    def get_by_id(self, id: str) -> WeatherData:
        pass

    @abstractmethod
    def save(self, weather_data: WeatherData) -> WeatherData:
        pass

    @abstractmethod
    def filter_by_request_id(self, id: str) -> List[WeatherData]:
        pass
