import pydantic

from src.config import TimeStampModel

class UserSignUp(pydantic.BaseModel):
    """Class to sign up."""
    username: str
    password1: str
    password2: str


class UserLogin(pydantic.BaseModel):
    """Class to login"""
    username: str
    password: str


class UserProfile(TimeStampModel):
    """Class to describe user info."""
    id: int  # ID needed in some places to avoid joins and more complex queries
    username: str
    rating: int
