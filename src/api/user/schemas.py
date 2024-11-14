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
    username: str
    rating: int
