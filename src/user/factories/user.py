import uuid

import factory

from config import session_factory
from src.core.factories import AsyncFactoryBoy

from .. import models


class UserFactory(AsyncFactoryBoy):
    """Factory for User model."""

    username = factory.LazyAttribute(function=lambda user: uuid.uuid4().hex)
    password = "New password!"
    rating = factory.Faker(
        "pyint",
        min_value=100,
        max_value=1000,
    )
    is_active = True

    class Meta:
        model = models.User
        sqlalchemy_session_factory = session_factory
