import typing

import fastapi

from src import models

from .. import schemas, services
from . import utils

router = fastapi.APIRouter(prefix="/auth", tags=["auth"])

@router.post("/sign-up")
async def sign_up(
    user: schemas.UserSignUp
) -> dict[str, typing.Any]:
    """User sign up."""
    async with services.UserAuthService() as handler:
        tokens = await handler.user_sign_up(user)
    return tokens


@router.post("/login")
async def login(
    user: schemas.UserLogin,
) -> dict[str, typing.Any]:
    """User login."""
    async with services.UserAuthService() as handler:
        tokens = await handler.user_login(user)
    return tokens


@router.get("/profile")
async def profile(
    user: models.User = fastapi.Depends(utils.get_user_profile),
) -> schemas.UserProfile:
    return schemas.UserProfile(**user.__dict__).model_dump()

@router.get("/logout")
async def logout(response: fastapi.Response):
    """User logout."""
    async with services.UserAuthService() as handler:
        await handler.user_logout(response)
    return {
        "message": "Successfully logged out",
    }