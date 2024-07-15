from sqlalchemy import Column, String, Integer, DateTime, Float

from infrastructure.persistence.database import Base


class WeatherData(Base):
    __tablename__ = "weather_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    city_id = Column(String, nullable=False)
    humidity = Column(Float, nullable=False)
    ow_request_timestamp = Column(DateTime, nullable=False)
    request_id = Column(String, index=True, nullable=False)
    temperature_celsius = Column(Float, nullable=False)
    user_request_timestamp = Column(DateTime, nullable=False)
