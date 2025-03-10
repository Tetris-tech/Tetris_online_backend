import datetime

import pydantic


class TimeStampModel(pydantic.BaseModel):
    """Read only model with created and modified fields."""

    model_config = pydantic.ConfigDict(from_attributes=True)

    id: int
    created: datetime.datetime
    modified: datetime.datetime

    @pydantic.field_serializer("created")
    def created_to_str(self, created: datetime.datetime, _info) -> str:
        """Convert created field from datetime to str."""
        return str(created)

    @pydantic.field_serializer("modified")
    def modified_to_str(self, modified: datetime.datetime, _info) -> str:
        """Convert modified field from datetime to str."""
        return str(modified)
