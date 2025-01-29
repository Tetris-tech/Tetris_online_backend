import sqlalchemy
from config.database import Base

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
