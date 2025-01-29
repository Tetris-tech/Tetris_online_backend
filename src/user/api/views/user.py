import typing

import fastapi

from ... import db_services

router = fastapi.APIRouter(prefix="/users", tags=["users"])

@router.get("")
async def get_list(
    offset: int = fastapi.Query(0, ge=0),
    size: int = fastapi.Query(25, ge=1, le=25),
) -> dict[str, typing.Any]:
    """Return list of users."""
    async with db_services.UserCRUDService() as service:
        result = await service.get_list(offset, size)

    return result


@router.get("/{id}")
async def get_one(
    id: int,
) -> dict[str, typing.Any]:
    "Return user by id."
    async with db_services.UserCRUDService() as service:
        result = await service.get_one(id)
    return result
