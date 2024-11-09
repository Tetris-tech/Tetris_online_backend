import fastapi
import sqlalchemy

from src.config.database import async_session
from src import models

from ..schemas import UserProfile
from . import UserService

OAUTH2_SCHEME = fastapi.security.OAuth2PasswordBearer(tokenUrl="token")

async def get_user_profile(
    token: str = fastapi.Depends(OAUTH2_SCHEME),
) -> UserProfile:
    """Get user info."""
    payload = UserService().verify_token(token)
    user_id = payload.get("user_id")
    query = (
        sqlalchemy.Select(models.User)
        .where(models.User.id == user_id)
    )
    result = await async_session().execute(query)
    db_user = result.scalar_one_or_none()
    return db_user
