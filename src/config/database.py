from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sqlalchemy


from .settings import Settings


DATABASE_URL = "postgresql+asyncpg://{}@{}:5432/{}?async_fallback=True".format(
    Settings.DB_USER.value,
    Settings.DB_PASSWORD.value,
    Settings.DB_HOST.value,
    Settings.DB_NAME.value,
)

engine = create_async_engine(DATABASE_URL)

async_session = sessionmaker(bind=engine, class_=AsyncSession)

Base = declarative_base()


async def get_session() -> AsyncSession:
    """Yield database session."""
    async with async_session.begin() as session:
        yield session
