import http
import typing

import fastapi

from src.user.api.schemes import UserProfile

from ... import services
from .. import schemes

router = fastapi.APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/sign-up",
    status_code=http.HTTPStatus.CREATED,
)
async def sign_up(
    user: schemes.UserSignUp,
    response: fastapi.Response,
) -> dict[str, typing.Any]:
    """User sign up."""
    user = await services.UserAuthService().user_sign_up(
        user,
        response=response,
    )
    return UserProfile.model_validate(user).model_dump()


# @router.post("/login")
# async def login(
#     user: schemes.UserLogin,
#     response: fastapi.Response
# ) -> dict[str, typing.Any]:
#     """User login."""
#     async with services.UserAuthService() as handler:
#         await handler.user_login(user, response)

#     return {
#         "message": "Successfully logged in.",
#     }


# @router.get("/profile")
# async def profile(
#     user: models.User = fastapi.Depends(services.get_user_profile),
# ) -> UserProfile:
#     return UserProfile(**user.__dict__).model_dump()
