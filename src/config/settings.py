from enum import Enum

from decouple import config

class Settings(Enum):
    """Configuration for project."""

    # Setup for db
    DB_USER = config("POSTGRES_USER")
    DB_NAME = config("POSTGRES_NAME")
    DB_HOST = config("POSTGRES_HOST")
    DB_PASSWORD = config("POSTGRES_PASSWORD")
    DB_PORT = 5432

    # Setup for redis
    REDIS_HOST = config("REDIS_URL")
    REDIS_PORT = config("REDIS_PORT")

    # Setup for s3
    S3_BUCKET_NAME = config("S3_BUCKET_NAME")
    S3_ENDPOINT = config("S3_ENDPOINT")
    S3_ACCESS_KEY = config("S3_ACCESS_KEY")
    S3_SECRET_KEY = config("S3_SECRET_KEY")

    # Setup for JWT
    JWT_SECRET_KEY = config("JWT_SECRET_KEY")
    JWT_ALGORITHM = config("JWT_ALGORITHM", default="HS256")
    JWT_EXPIRE_MINUTES = config("JWT_EXPIRE_MINUTES", default=30, cast=int)
