import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, declarative_base


load_dotenv()


pg_db = os.environ.get('POSTGRES_DATABASE', 'dg-database')
pg_host = os.environ.get('POSTGRES_HOST', 'database')
pg_password = os.environ.get('POSTGRES_PASSWORD', 'password123')
pg_port = os.environ.get('POSTGRES_PORT', 5432)
pg_user = os.environ.get('POSTGRES_USER', 'admin')

SQLALCHEMY_DATABASE_URL = f"postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_db}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base(metadata=MetaData(schema="public"))
Base = declarative_base()
