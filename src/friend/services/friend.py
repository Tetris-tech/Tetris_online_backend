import typing

import fastapi
import sqlalchemy
from fastapi import Depends, HTTPException
import fastapi.security

from src.auth.services import UserAuthService
from src.core.db import BaseService
# HACK: Is it correct to import from user package here?
from src.user.api import schemes as user_schemas
from src.auth import services
from src.user import models
OAUTH2_SCHEME = fastapi.security.OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(
        token: str = Depends(OAUTH2_SCHEME),
        service: services.UserAuthService = Depends(UserAuthService),
) -> user_schemas.UserProfile:
    """Dependency to get current user from token."""
    try:
        return await service.get_user_profile(token)
    except Exception as exc:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc


class FriendCRUDService(BaseService):
    async def create_request(
            self,
            sender_id: int,
            recipient_id: int
    ) -> dict[str, typing.Any]:
        """Create friend request."""
        # Check existing request
        existing = await self.session.execute(
            sqlalchemy.select(models.Friend).where(
                (models.Friend.sender_id == sender_id) &
                (models.Friend.recipient_id == recipient_id)

            )
        )
        if existing.scalar():
            return {"message": "Request already exists"}

        request = sqlalchemy.insert(models.Friend).values(
            sender_id=sender_id,
            recipient_id=recipient_id,
            status="pending"
        )
        result = await self.session.execute(request)
        return {"id": result.inserted_primary_key[0]}

    async def update_request_status(
            self,
            request_id: int,
            recipient_id: int,
            new_status: str
    ) -> dict[str, typing.Any]:
        """Update request status."""
        request = await self.session.get(models.Friend, request_id)
        if not request or request.recipient_id != recipient_id:
            raise fastapi.HTTPException(
                status_code=404,
                detail={"message": "Request not found"}
            )

        await self.session.execute(
            sqlalchemy.update(models.Friend)
            .where(models.Friend.id == request_id)
            .values(status=new_status)
        )
        return {"message": "Status updated"}

    async def get_pending_requests(
            self,
            user_id: int
    ) -> typing.List[dict[str, typing.Any]]:
        """Get pending requests for user."""
        result = await self.session.execute(
            sqlalchemy.where(
                (models.Friend.recipient_id == user_id) &
                (models.Friend.status == "pending")
            )
        )
        return [dict(row) for row in result]

    # Alternative way
    # async def get_friends(
    #         self,
    #         user_id: int
    # ) -> typing.List[dict[str, typing.Any]]:
    #     """Get accepted friends for user."""
    #     result = await self.session.execute(
    #         sqlalchemy.select(models.Friend).where(
    #             ((models.Friend.sender_id == user_id) |
    #              (models.Friend.recipient_id == user_id)) &
    #             (models.Friend.status == "accepted")
    #         )
    #     )
    #     return [dict(row) for row in result]

    async def get_friends(
            self,
            user_id: int
    ) -> typing.List[dict[str, typing.Any]]:
        """Get accepted friends using SQLAlchemy relationships."""
        user = await self.session.get(
            models.User,
            user_id,
            options=[
                sqlalchemy.orm.selectinload(models.User.friends),
                sqlalchemy.orm.selectinload(models.User.added_by)
            ]
        )

        if not user:
            return []

        # Combine both directions of relationships
        friends = []

        # Friends user initiated
        for friend_request in user.friends:
            if friend_request.status == "accepted":
                friends.append({
                    "friend_id": friend_request.recipient_id,
                    "status": friend_request.status
                })

        # Friends who initiated with this user
        for friend_request in user.added_by:
            if friend_request.status == "accepted":
                friends.append({
                    "friend_id": friend_request.sender_id,
                    "status": friend_request.status
                })

        return friends

