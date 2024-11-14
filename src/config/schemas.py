import typing

import pydantic


class TimeStampModel(pydantic.BaseModel):
    """Read only model with created and modified fields."""

    model_config = pydantic.ConfigDict(from_attributes=True)

    id: int
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
