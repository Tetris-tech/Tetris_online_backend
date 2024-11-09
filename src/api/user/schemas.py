import pydantic

class UserSignUp(pydantic.BaseModel):
    """Class to sign up."""
    username: str
    password1: str
    password2: str


class UserLogin(pydantic.BaseModel):
    """Class to login"""
    username: str
    password: str


class UserProfile(pydantic.BaseModel):
    """Class to describe user info."""
    id: int
    username: str
    rating: int
    created: str
    modified: str

    @pydantic.validator("created", pre=True)
    def created_to_str(cls, value) -> str:
        """Convert created field from datetime to str."""
        return str(value)

    @pydantic.validator("modified", pre=True)
    def modified_to_str(cls, value) -> str:
        """Convert modified field from datetime to str."""
        return str(value)
