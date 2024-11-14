import fastapi

from .. import services

from src import models

async def get_user_profile(
    token: str = fastapi.Depends(services.OAUTH2_SCHEME)
) -> models.User:
    """Return user by jwt token."""
    async with services.UserAuthService() as service:
        user = await service.get_user_profile(token)
    return user
