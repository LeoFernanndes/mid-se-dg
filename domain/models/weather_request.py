from sqlalchemy import Column, String, DateTime, Boolean

from infrastructure.persistence.database import Base


class WeatherRequest(Base):
    __tablename__ = "weather_request"

    id = Column(String, primary_key=True)
    timestamp = Column(DateTime)
    completed = Column(Boolean, nullable=False)
