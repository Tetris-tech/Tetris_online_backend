import pydantic

class UserLogin(pydantic.BaseModel):
    """Class to login"""
    username: str
    password: str
