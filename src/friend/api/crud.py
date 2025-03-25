import typing
from typing import List

from fastapi import APIRouter, HTTPException, status, Depends
from ..services.friend import get_current_user
from .. import services
from src.user.api import schemes as schemas # Todo: Schemes is a typo?
router = APIRouter(prefix="/friends", tags=["friends"])


@router.post("/requests")
async def send_friend_request(
    recipient_id: int,
    current_user: schemas.UserProfile = Depends(get_current_user)
) -> dict:
    """Send friend request."""
    async with services.FriendCRUDService() as service:
        sender_id = current_user.id
        if sender_id == recipient_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"message": "Cannot add yourself"}
            )
        return await service.create_request(sender_id, recipient_id)


@router.get("/requests")
async def list_pending_requests(
        user_id: int
) -> List[dict[str, typing.Any]]:
    # TODO:// Add pagination
    """List pending friend requests."""
    async with services.FriendCRUDService() as service:
        return await service.get_pending_requests(user_id)


@router.patch("/requests/{request_id}")
async def respond_to_request(
        request_id: int,
        user_id: int,
        new_status: str
) -> dict[str, typing.Any]:
    """Respond to friend request."""
    async with services.FriendCRUDService() as service:
        return await service.update_request_status(
            request_id,
            user_id,
            new_status
        )



@router.get("")
async def list_friends(
    current_user: schemas.UserProfile = Depends(get_current_user),
) -> List[dict[str, typing.Any]]:
    # TODO:// Add pagination
    """List accepted friends for the current user."""
    async with services.FriendCRUDService() as service:
        return await service.get_friends(current_user.id)

@router.get("/{user_id}")
async def list_friends_by_user(user_id: int) -> dict[str, typing.Any]:
    """List accepted friends by user using user ID."""
    # TODO:// Add privacy controls, i.e. checks for visibility of one's friends based on the person's privacy settings

    async with services.FriendCRUDService() as service:
        return await service.get_friends(user_id)

@router.delete("/{friend_id}")
async def remove_friend(
    friend_id: int,
    current_user: schemas.UserProfile = Depends(get_current_user)
):
    async with services.FriendCRUDService() as service:
        return await service.delete_friend(friend_id, current_user)

# TODO:// Add webhooks to track friendship status change and notifications