import http

import sqlalchemy
from httpx import AsyncClient
from sqlalchemy.ext import asyncio as sql_asyncio

from src.core.db import open_session
from src.user import factories, models


async def test_api(
    client: AsyncClient,
    session: sql_asyncio.AsyncSession,
):
    """Test sign up."""
    user_data = factories.UserFactory.build()
    data = {
        "username": user_data.username,
        "password1": user_data.password,
        "password2": user_data.password,
    }
    response = await client.post(
        url="/auth/sign-up",
        json=data,
    )
    assert response.status_code == http.HTTPStatus.CREATED
    response_data = response.json()

    query = sqlalchemy.select(models.User).where(
        models.User.username == response_data["username"]
    )
    async with open_session(commit=True) as session:
        raw_result = await session.execute(query)
        user: models.user = raw_result.scalar_one_or_none()

        assert user
        assert user.check_password(data["password1"])
        await session.delete(user)


async def test_add_instance_with_existing_username(
    client: AsyncClient,
):
    """Test user with existing username cannot be added."""
    async with open_session(commit=True) as session:
        user: models.User = await factories.UserFactory.async_create(
            session=session
        )
    data = {
        "username": user.username,
        "password1": factories.UserFactory.password,
        "password2": factories.UserFactory.password,
    }
    response = await client.post(
        "/auth/sign-up",
        json=data,
    )
    assert response.status_code == http.HTTPStatus.BAD_REQUEST, response.json()
    assert (
        response.json()["detail"]["username"]
        == "User with the username already exist"
    )

    async with open_session(commit=True) as session:
        await session.delete(instance=user)
