from sqlalchemy.ext.asyncio import AsyncSession

import config


class BaseService:
    """Base service class for db connection."""
    async def __aenter__(self, *args, **kwargs) -> AsyncSession:
        async with config.async_session() as session:
            yield session

    async def __aexit__(self, *args, **kwargs):
        await self.session.close()
