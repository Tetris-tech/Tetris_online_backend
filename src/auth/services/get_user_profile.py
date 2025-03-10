import fastapi

from src.user import models

from .auth import OAUTH2_SCHEME, UserAuthService


async def get_user_profile(
    token: str = fastapi.Depends(OAUTH2_SCHEME),
) -> models.User:
    """Return user by jwt token."""
    async with UserAuthService() as service:
        user = await service.get_user_profile(token)
    return user
