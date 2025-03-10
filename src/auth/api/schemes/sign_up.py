import pydantic


class UserSignUp(pydantic.BaseModel):
    """Class to sign up."""

    username: str
    password1: str
    password2: str
