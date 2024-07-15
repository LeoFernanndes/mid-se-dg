import os
import requests

from datetime import datetime
from dotenv import load_dotenv
from typing import List

from application.dtos.weather_data import WeatherDataApiDto, WeatherDataInputDto, WeatherDataOutputDto, WeatherRetrievalStatusInputDto, WeatherRetrievalStatusOutputDto
from application.dtos.weather_request import WeatherRequestOutputDto, WeatherRequestInputDto
from application.repositories.weather_data_repository import WeatherDataRepository
from application.repositories.weather_request_repository import WeatherRequestRepository
from domain.models.weather_data import WeatherData
from domain.models.weather_request import WeatherRequest
from domain.city_ids import city_ids


load_dotenv()


class WeatherService:
    def __init__(self, weather_data_repository: WeatherDataRepository, weather_request_repository: WeatherRequestRepository):
        self.weather_data_repository = weather_data_repository
        self.weather_request_repository = weather_request_repository

    def get_weather_request_by_id(self, weather_request_id: str) -> WeatherRequestOutputDto | None:
        weather_request = self.weather_request_repository.get_by_id(weather_request_id)
        if not weather_request:
            return None
        return WeatherRequestOutputDto(id=weather_request.id, timestamp=weather_request.timestamp, completed=weather_request.completed)

    def get_weather_request_retrieval_status(
            self, weather_retrieval_status_input_dto: WeatherRetrievalStatusInputDto
    ) -> WeatherRetrievalStatusOutputDto:
        weather_request = self.weather_request_repository.get_by_id(weather_retrieval_status_input_dto.id)
        if not weather_request:
            raise Exception(f"WeatherRequest with id {weather_retrieval_status_input_dto.id} not found")
        weather_data = self.weather_data_repository.filter_by_request_id(weather_retrieval_status_input_dto.id)
        retrieval_percentage_status = len(set([wd.city_id for wd in weather_data]))/len(city_ids)
        return WeatherRetrievalStatusOutputDto(
            id=weather_retrieval_status_input_dto.id, percentage_status=retrieval_percentage_status, timestamp=weather_request.timestamp)

    def filter_retrieved_weather_data_by_request_id(self, weather_request_id: str) -> List[WeatherDataOutputDto]:
        retrieved_weather_data = self.weather_data_repository.filter_by_request_id(weather_request_id)
        return [WeatherDataOutputDto(
            id=d.id, city_id=d.city_id, humidity=d.humidity, ow_request_timestamp=d.ow_request_timestamp, request_id=d.request_id,
            temperature_celsius=d.temperature_celsius, user_request_timestamp=d.user_request_timestamp) for d in retrieved_weather_data]

    def list_uncompleted_weather_requests(self) -> List[WeatherRequestOutputDto]:
        uncompleted_requests = self.weather_request_repository.filter_uncompleted()
        return [WeatherRequestOutputDto(id=r.id, timestamp=r.timestamp, completed=r.completed) for r in uncompleted_requests]

    def save_weather_data(self, weather_data_input_dto: WeatherDataInputDto) -> WeatherDataOutputDto:
        weather_data = WeatherData(**weather_data_input_dto.model_dump())
        created_weather_data = self.weather_data_repository.save(weather_data)
        return WeatherDataOutputDto(id=created_weather_data.id, ow_request_timestamp=created_weather_data.ow_request_timestamp,
                                    temperature_celsius=created_weather_data.temperature_celsius, humidity=created_weather_data.humidity,
                                    request_id=created_weather_data.request_id, city_id=created_weather_data.city_id,
                                    user_request_timestamp=created_weather_data.user_request_timestamp)

    def save_weather_request(self, weather_request_dto: WeatherRequestInputDto) -> WeatherRequestOutputDto:
        weather_request = WeatherRequest(id=weather_request_dto.id, timestamp=datetime.now(), completed=False)
        saved_weather_request = self.weather_request_repository.save(weather_request)
        return WeatherRequestOutputDto(id=saved_weather_request.id, timestamp=saved_weather_request.timestamp, completed=saved_weather_request.completed)

    def request_weather_data_for_city_id(self, city_id: str) -> WeatherDataApiDto:
        open_weather_api_key = os.environ.get("OPEN_WEATHER_API_KEY")
        url = f"https://api.openweathermap.org/data/2.5/weather?id={city_id}&appid={open_weather_api_key}"
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception("Failed to retrieve data from weather api.")
        response_json = response.json()["main"]
        return WeatherDataApiDto(city_id=city_id, humidity=response_json["humidity"], temperature_celsius=response_json["temp"]-273, timestamp=datetime.now())

    def update_weather_request_to_complete(self, request_id: str) -> WeatherRequestOutputDto:
        weather_request = self.weather_request_repository.get_by_id(request_id)
        weather_request.completed = True
        updated_request = self.weather_request_repository.save(weather_request)
        return WeatherRequestOutputDto(id=updated_request.id, timestamp=updated_request.timestamp, completed=updated_request.completed)
