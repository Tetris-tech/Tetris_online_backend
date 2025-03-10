import asyncio
import typing

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext import asyncio as sql_asyncio

from config import DATABASE_URL
from src.main import app
from src.user import factories, models

pytestmark = pytest.mark.asyncio(scope="session")


@pytest.fixture(scope="session")
def event_loop() -> typing.Generator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def session() -> typing.AsyncGenerator[sql_asyncio.AsyncSession, None]:
    engine = sql_asyncio.create_async_engine(url=DATABASE_URL, future=True)
    session = sql_asyncio.AsyncSession(
        bind=engine,
    )
    yield session
    await session.close()


@pytest.fixture(scope="session")
async def client() -> AsyncClient:
    """Get api client for testing request."""
    async with AsyncClient(
        transport=(ASGITransport(app=app)), base_url="http://localhost:8000"
    ) as client:
        yield client


@pytest.fixture(scope="session")
async def user(
    session: sql_asyncio.AsyncSession,
) -> typing.AsyncGenerator[models.User, None]:
    """Get user instance."""
    user = await factories.UserFactory.async_create(session=session)
    yield user
    await session.delete(user)
    await session.commit()
