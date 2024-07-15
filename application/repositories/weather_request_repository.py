from abc import ABC, abstractmethod
from typing import List

from domain.models.weather_request import WeatherRequest


class WeatherRequestRepository(ABC):

    @abstractmethod
    def get_by_id(self, id: str) -> WeatherRequest:
        pass

    @abstractmethod
    def filter_uncompleted(self) -> List[WeatherRequest]:
        pass

    @abstractmethod
    def save(self, weather_request: WeatherRequest) -> WeatherRequest:
        pass
