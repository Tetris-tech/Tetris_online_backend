from src.core.api.schemes import TimeStampModel

class UserProfile(TimeStampModel):
    """Class to describe user info."""
    username: str
    rating: int
