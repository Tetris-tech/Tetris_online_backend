import typing
from contextlib import asynccontextmanager

from sqlalchemy.ext import asyncio as sql_asyncio

from config import engine


@asynccontextmanager
async def open_session(
    commit: bool = False,
    flush: bool = False,
) -> typing.AsyncGenerator[sql_asyncio.AsyncSession, None]:
    """Handle opening and closing db session."""
    try:
        session = sql_asyncio.AsyncSession(bind=engine)
        yield session
    finally:
        if commit:
            await session.commit()
        if flush:
            await session.flush()
        await session.close()


class BaseService:
    """Base service class for db connection."""

    # async def __aenter__(self, *args, **kwargs) -> AsyncSession:
    #     async with config.async_sessionmaker() as session:
    #         yield session

    # async def __aexit__(self, *args, **kwargs):
    #     await self.session.close()
