import typing

import fastapi

import sqlalchemy

from src.config import BaseService

from src import models

from .. import schemas

class UserCRUDService(BaseService):
    """User CRUD service to execute SQL queries."""

    async def get_list(
        self,
        offset: int,
        size: int,
    ) -> list[models.User]:
        """Get list of User."""

        users_query = (
            sqlalchemy.select(models.User)
            .offset(offset)
            .limit(size)
        )
        total_count_query = (
            sqlalchemy.select(sqlalchemy.func.count("*"))
            .select_from(models.User)
        )
        users = (
            await self.session.execute(users_query)
        )
        total_count = (
            await self.session.execute(total_count_query)
        )
        return {
            "users": [
                schemas.UserProfile.model_validate(record[0]).model_dump()
                for record in users.fetchall()
            ],
            "total_count": total_count.scalar()
        }

    async def get_one(
        self,
        id: int,
    ) -> dict[typing.Any]:
        """Return one user."""
        user = await self.session.get(models.User, id)
        if not user:
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_404_NOT_FOUND,
                detail={
                    "message": "Not Found",
                }
            )

        return schemas.UserProfile.model_validate(user).model_dump()
