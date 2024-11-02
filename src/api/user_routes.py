from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from ..config.auth import get_current_user
from ..config.database import get_session
from ..config.user_service import UserService
from ..config.models import User

router = APIRouter(prefix="/users", tags=["Users"])

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate, session: AsyncSession = Depends(get_session)):
    new_user = await UserService.register_user(
        session=session,
        username=user.username,
        email=user.email,
        password=user.password
    )
    return {"message": "User created successfully", "user_id": new_user.id}

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_session)):
    access_token = await UserService.authenticate_user(
        session=session,
        email=form_data.username,
        password=form_data.password
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/reset-password")
async def reset_password(email: str, session: AsyncSession = Depends(get_session)):
    message = await UserService.reset_password(session=session, email=email)
    return {"message": message}

@router.post("/logout")
async def logout():
    return {"message": "User logged out"}

@router.get("/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
