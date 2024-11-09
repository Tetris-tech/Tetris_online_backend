from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sqlalchemy


from .settings import Settings

DATABASE_URL = "postgresql+asyncpg://{}:{}@{}:5432/{}?async_fallback=True".format(
    Settings.DB_USER.value,
    Settings.DB_PASSWORD.value,
    Settings.DB_HOST.value,
    Settings.DB_NAME.value
)

Base = declarative_base()

engine = create_async_engine(DATABASE_URL, echo=True)

async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

class BaseModel(Base):
    """Base model with general fields."""

    __abstract__ = True

    id = sqlalchemy.Column(
        sqlalchemy.INTEGER,
        name="id",
        nullable=False,
        primary_key=True,
        autoincrement=True,
    )
    created = sqlalchemy.Column(
        sqlalchemy.DateTime,
        name="created",
        default=sqlalchemy.func.now(),
    )
    modified = sqlalchemy.Column(
        sqlalchemy.DateTime,
        name="modified",
        default=sqlalchemy.func.now(),
        onupdate=sqlalchemy.func.current_timestamp(),
    )
