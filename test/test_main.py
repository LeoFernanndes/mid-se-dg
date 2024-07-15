import pytest

from datetime import datetime
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from sqlalchemy.sql import text

from application.dtos.weather_data import WeatherRetrievalStatusInputDto, WeatherDataInputDto
from application.dtos.weather_request import WeatherRequestInputDto
from application.services.weather import WeatherService
from domain.models.weather_data import WeatherData
from domain.models.weather_request import WeatherRequest
from infrastructure.repositories.weather_data_sqlalchemy_repository import WeatherDataSqlalchemyRepository
from infrastructure.repositories.weather_request_sqlalchemy_repository import WeatherRequestSqlalchemyRepository
from infrastructure.persistence.database import Base
from main import app
from routes.main import get_weather_service


SQLALCHEMY_DATABASE_URL = "sqlite://"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_weather_service():
    db = TestingSessionLocal()
    try:
        weather_data_repository = WeatherDataSqlalchemyRepository(db)
        weather_request_repository = WeatherRequestSqlalchemyRepository(db)
        yield WeatherService(weather_data_repository=weather_data_repository, weather_request_repository=weather_request_repository)
    finally:
        db.close()


app.dependency_overrides[get_weather_service] = override_get_weather_service
client = TestClient(app)


@pytest.fixture
def seed_weather_requests():
    db = TestingSessionLocal()
    db.add_all([
        WeatherRequest(id="test1", timestamp=datetime.now(), completed=False),
        WeatherRequest(id="test2", timestamp=datetime.now(), completed=False),
        WeatherRequest(id="test3", timestamp=datetime.now(), completed=False),
        WeatherRequest(id="test4", timestamp=datetime.now(), completed=False),
        WeatherData(id=1, user_request_timestamp=datetime.now(), city_id="3439902", temperature_celsius=8.66, humidity=66, request_id="test1", ow_request_timestamp=datetime.now()),
        WeatherData(id=2, user_request_timestamp=datetime.now(), city_id="3442805", temperature_celsius=8.66, humidity=66, request_id="test1", ow_request_timestamp=datetime.now()),
        WeatherData(id=3, user_request_timestamp=datetime.now(), city_id="3443952", temperature_celsius=8.66, humidity=66, request_id="test1", ow_request_timestamp=datetime.now()),
        WeatherData(id=4, user_request_timestamp=datetime.now(), city_id="3442720", temperature_celsius=8.66, humidity=66, request_id="test1", ow_request_timestamp=datetime.now()),
        WeatherData(id=5, user_request_timestamp=datetime.now(), city_id="3439902", temperature_celsius=8.66, humidity=66, request_id="test1", ow_request_timestamp=datetime.now()),
        WeatherData(id=6, user_request_timestamp=datetime.now(), city_id="3439902", temperature_celsius=8.66, humidity=66, request_id="test1", ow_request_timestamp=datetime.now()),
        WeatherData(id=7, user_request_timestamp=datetime.now(), city_id="3439902", temperature_celsius=8.66, humidity=66, request_id="test1", ow_request_timestamp=datetime.now()),
        WeatherData(id=8, user_request_timestamp=datetime.now(), city_id="3439902", temperature_celsius=8.66, humidity=66, request_id="test1", ow_request_timestamp=datetime.now()),
    ])
    # print('created')
    db.commit()
    db.close()
    yield
    db.rollback()
    # truncate all tables
    for table in reversed(Base.metadata.sorted_tables):
        db.execute(text(f'delete from {table.name};'))
        db.commit()
    db.close()


def tear_down_weather_requests():
    db = TestingSessionLocal()
    for table in reversed(Base.metadata.sorted_tables):
        db.execute(text(f'delete from {table.name};'))
        db.commit()
    db.commit()
    db.close()


def test_http_request_create_weather_request_201(seed_weather_requests):
    payload = {
        "id": "test5"
    }
    response = client.post("/", json=payload)
    json_response = response.json()
    assert response.status_code == 201
    assert json_response['id'] == payload['id']
    assert json_response['completed'] is False


def test_http_request_create_weather_request_400(seed_weather_requests):
    payload = {
        "id": "test4"
    }
    response = client.post("/", json=payload)
    json_response = response.json()
    assert response.status_code == 400
    assert json_response == {'detail': 'Id test4 is already in use.'}


def test_http_request_crate_weather_request_422(seed_weather_requests):
    payload = {
        "_id": "test4"
    }
    response = client.post("/", json=payload)
    json_response = response.json()
    assert response.status_code == 422


def test_http_request_get_retrieval_status_with_repeated_values_200(seed_weather_requests):
    response = client.get("/test1")
    json_response = response.json()
    expected_result = {'id': 'test1', 'percentage_status': 0.023952095808383235}
    assert response.status_code == 200
    assert json_response == expected_result


def test_http_request_get_retrieval_status_empty_200(seed_weather_requests):
    response = client.get("/test2")
    json_response = response.json()
    expected_result = {'id': 'test2', 'percentage_status': 0.0}
    assert response.status_code == 200
    assert json_response == expected_result


def test_http_request_get_retrieval_status_404(seed_weather_requests):
    response = client.get("/test404")
    assert response.status_code == 404


def test_weather_service_get_weather_request_by_id_found(seed_weather_requests):
    weather_service = next(override_get_weather_service())
    weather_request = weather_service.get_weather_request_by_id("test1")
    assert weather_request.id == "test1"


def test_weather_service_get_weather_request_by_id_not_found(seed_weather_requests):
    weather_service = next(override_get_weather_service())
    weather_request = weather_service.get_weather_request_by_id("test404")
    assert weather_request is None


def test_weather_service_get_weather_request_retrieval_status(seed_weather_requests):
    weather_service = next(override_get_weather_service())
    retrieval_status = weather_service.get_weather_request_retrieval_status(WeatherRetrievalStatusInputDto(id="test1"))
    assert retrieval_status.id == "test1"


def test_weather_service_get_weather_request_retrieval_status_not_found_raises_exception(seed_weather_requests):
    weather_service = next(override_get_weather_service())
    with pytest.raises(Exception):
        weather_service.get_weather_request_retrieval_status(WeatherRetrievalStatusInputDto(id="test404"))


def test_weather_service_update_weather_request_to_complete(seed_weather_requests):
    weather_service = next(override_get_weather_service())
    updated_request = weather_service.update_weather_request_to_complete(request_id="test1")
    assert updated_request.completed is True


def test_weather_service_update_weather_request_to_complete_not_fount_raises_attribute_error(seed_weather_requests):
    weather_service = next(override_get_weather_service())
    with pytest.raises(AttributeError):
        weather_service.update_weather_request_to_complete(request_id="test404")


def test_weather_service_request_weather_data_for_city_id(seed_weather_requests):
    weather_service = next(override_get_weather_service())
    api_data = weather_service.request_weather_data_for_city_id("3439902")
    assert api_data.city_id == "3439902"


def test_weather_service_request_weather_data_for_city_id_404_raises_exception(seed_weather_requests):
    weather_service = next(override_get_weather_service())
    with pytest.raises(Exception):
        weather_service.request_weather_data_for_city_id("Non_existent_3439902")


def test_weather_service_filter_retrieved_weather_data_by_request_id(seed_weather_requests):
    weather_service = next(override_get_weather_service())
    retrieved_weather_data = weather_service.filter_retrieved_weather_data_by_request_id("test1")
    assert len(retrieved_weather_data) == 8


def test_weather_service_filter_retrieved_weather_data_by_request_id_empty(seed_weather_requests):
    weather_service = next(override_get_weather_service())
    retrieved_weather_data = weather_service.filter_retrieved_weather_data_by_request_id("test4")
    assert len(retrieved_weather_data) == 0


def test_weather_service_filter_retrieved_weather_data_by_request_id_not_found(seed_weather_requests):
    weather_service = next(override_get_weather_service())
    retrieved_weather_data = weather_service.filter_retrieved_weather_data_by_request_id("test4")
    assert len(retrieved_weather_data) == 0


def test_weather_service_list_uncompleted_requests(seed_weather_requests):
    weather_service = next(override_get_weather_service())
    uncompleted_requests = weather_service.list_uncompleted_weather_requests()
    assert len(uncompleted_requests) == 4


def test_weather_service_save_weather_request(seed_weather_requests):
    weather_service = next(override_get_weather_service())
    weather_request_dto = WeatherRequestInputDto(id="test5")
    created_weather_request = weather_service.save_weather_request(weather_request_dto)
    assert created_weather_request.id == "test5"

