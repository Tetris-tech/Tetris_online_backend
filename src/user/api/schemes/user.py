from src.core.api.schemes import TimeStampModel


class UserProfile(TimeStampModel):
    """Class to describe user info."""
    id: int  # ID needed in some places to avoid joins and more complex queries
    username: str
    rating: int