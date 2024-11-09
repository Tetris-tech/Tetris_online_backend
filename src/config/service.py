from sqlalchemy.ext.asyncio import AsyncSession

from .database import async_session


class BaseService:
    """Base service class for db connection."""
    async def __aenter__(self, *args, **kwargs):
        async with async_session() as session:
            self.session: AsyncSession = session
            return self

    async def __aexit__(self, *args, **kwargs):
        await self.session.close()
