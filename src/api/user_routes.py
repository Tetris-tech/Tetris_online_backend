from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from passlib.context import CryptContext
from datetime import timedelta
from ..config.auth import create_access_token, verify_password, get_current_user
from ..config.database import get_session
from ..config.models import User  # Assuming the User model is in models.py

router = APIRouter(prefix="/users", tags=["Users"])

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Pydantic models for request validation
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate, session: AsyncSession = Depends(get_session)):
    # Hash the password
    hashed_password = pwd_context.hash(user.password)

    # Create the new user
    new_user = User(username=user.username, email=user.email, password=hashed_password)
    
    session.add(new_user)
    await session.commit()
    return {"message": "User created successfully"}

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_session)):
    db_user = await session.execute(select(User).where(User.email == form_data.username))
    db_user = db_user.scalar_one_or_none()
    if not db_user or not pwd_context.verify(form_data.password, db_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    # Генерация JWT токена
    access_token_expires = timedelta(minutes=Settings.JWT_EXPIRE_MINUTES.value)
    access_token = create_access_token(data={"sub": str(db_user.id)}, expires_delta=access_token_expires)
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/reset-password")
async def reset_password(email: str, session: AsyncSession = Depends(get_session)):
    # Implement the logic for password reset (sending email, etc.)
    return {"message": "Password reset link sent"}

@router.post("/logout")
async def logout():
    return {"message": "User logged out"}

@router.get("/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
