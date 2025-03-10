import typing

import factory
from sqlalchemy.ext import asyncio as sql_asyncio

from config import Base


class AsyncFactoryBoy(factory.alchemy.SQLAlchemyModelFactory):
    """Async factory boy."""

    class Meta:
        abstract = True

    @classmethod
    async def async_create(
        self,
        session: sql_asyncio.AsyncSession,
        will_close: bool = False,
        **kwargs,
    ) -> typing.Awaitable[Base]:
        """Return instance with id."""
        instance = self.build(**kwargs)
        session = (
            session
            if session is not None
            else self._meta.sqlalchemy_session_factory()
        )
        session.add(instance)
        await session.commit()
        await session.refresh(instance)
        session.expunge(instance=instance)

        return instance
