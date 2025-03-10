from sqlalchemy import URL
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

from .settings import Settings

DATABASE_URL = URL.create(
    "postgresql+asyncpg",
    username=Settings.DB_USER.value,
    password=Settings.DB_PASSWORD.value,
    host=Settings.DB_HOST.value,
    database=Settings.DB_NAME.value,
)
engine = create_async_engine(DATABASE_URL, echo=True)

session_factory = async_sessionmaker(bind=engine, expire_on_commit=False)

Base = declarative_base()
