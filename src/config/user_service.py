from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from passlib.context import CryptContext
from datetime import timedelta
from fastapi import HTTPException, status
from .models import User
from .auth import create_access_token, verify_password
from .settings import Settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    @staticmethod
    async def register_user(session: AsyncSession, username: str, email: str, password: str) -> User:
        hashed_password = pwd_context.hash(password)
        new_user = User(username=username, email=email, password=hashed_password)
        session.add(new_user)
        await session.commit()
        return new_user

    @staticmethod
    async def authenticate_user(session: AsyncSession, email: str, password: str) -> str:
        query = select(User).where(User.email == email)
        result = await session.execute(query)
        user = result.scalar_one_or_none()
        
        if not user or not pwd_context.verify(password, user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        access_token_expires = timedelta(minutes=Settings.JWT_EXPIRE_MINUTES.value)
        return create_access_token(data={"sub": str(user.id)}, expires_delta=access_token_expires)

    @staticmethod
    async def reset_password(session: AsyncSession, email: str) -> str:
        # TODO: Implement the actual password reset logic (e.g., sending email)
        # Here, we simply return a message for demonstration purposes
        return "Password reset link sent to " + email

    @staticmethod
    async def get_current_user(session: AsyncSession, user_id: int) -> User:
        query = select(User).where(User.id == user_id)
        result = await session.execute(query)
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user
