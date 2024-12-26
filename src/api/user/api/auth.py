import typing

import fastapi

from src import models

from .. import schemas, services
from . import utils

router = fastapi.APIRouter(prefix="/auth", tags=["auth"])

@router.post("/sign-up")
async def sign_up(
    user: schemas.UserSignUp,
    response: fastapi.Response,
) -> dict[str, typing.Any]:
    """User sign up."""
    async with services.UserAuthService() as handler:
        await handler.user_sign_up(user, response)
    return {
        "message": "Successfully signed up and logged in.",
    }


@router.post("/login")
async def login(
    user: schemas.UserLogin,
    response: fastapi.Response
) -> dict[str, typing.Any]:
    """User login."""
    async with services.UserAuthService() as handler:
        await handler.user_login(user, response)

    return {
        "message": "Successfully logged in.",
    }


@router.get("/profile")
async def profile(
    user: models.User = fastapi.Depends(utils.get_user_profile),
) -> schemas.UserProfile:
    return schemas.UserProfile(**user.__dict__).model_dump()
