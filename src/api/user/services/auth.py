import datetime
import hashlib

import fastapi.security
import requests
import sqlalchemy
import fastapi
from jose import JWTError, jwt
from pydantic import BaseModel
from fastapi import Response

from src import models
from src.config import BaseService, Settings
from src.models import RevokedToken
from .. import schemas

SECRET_KEY = Settings.SECRET_JWY_KEY.value
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_UNITS = 30

OAUTH2_SCHEME = fastapi.security.OAuth2PasswordBearer(tokenUrl="token")



class UserAuthService(BaseService):
    """Handle authentication service."""

    async def user_sign_up(self, user: BaseModel,response: Response)->None:
        """Create user and return one."""
        query = sqlalchemy.select(models.User).where(
            models.User.username == user.username
        )
        result = await self.session.execute(query)
        result = result.scalar_one_or_none()

        if result:
            raise fastapi.HTTPException(
                status_code=requests.codes.BAD_REQUEST,
                detail={
                    "username": "User with the username already exist",
                }
            )

        if user.password1 != user.password2:
            raise fastapi.HTTPException(
                status_code=requests.codes.BAD_REQUEST,
                detail={
                    "password": "passwords don't match.",
                }
            )

        user = user.model_dump()
        password = self.hash_password(
            password1=user.pop("password1", None),
            password2=user.pop("password2", None),
        )
        user["password"] = password
        user = models.User(**user)
        self.session.add(user)

        await self.session.commit()
        await self.session.refresh(user)

        refresh_token = self.generate_jwt_token(
            data={"user_id": user.id},
            is_refresh=True,
        )
        access_token = self.generate_jwt_token(data={"user_id": user.id})

        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            max_age=2592000
        )
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,
            max_age=ACCESS_TOKEN_EXPIRE_UNITS * 60
        )

    async def user_login(
        self,
        user: BaseModel,
        response: Response
    ) -> None:
        """Check credentials for login and return tokens for this."""
        query = (
            sqlalchemy.Select(models.User)
            .where(models.User.username == user.username)
        )
        result = await self.session.execute(query)
        db_user = result.scalar_one_or_none()
        password_right = self.check_password(
            user.password,
            db_user,
        )
        if not (db_user and password_right):
            raise fastapi.HTTPException(
                status_code=requests.codes.BAD_REQUEST,
                detail={
                    "message": "Incorrect username or password",
                },
            )

        refresh_token = self.generate_jwt_token(
            data={"user_id": db_user.id},
            is_refresh=True,
        )
        access_token = self.generate_jwt_token(
            data={"user_id": db_user.id},
        )
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True, # Can't be accessed by js
            secure=True, # Only sent over https
            max_age=2592000 # 30 days
        )
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly = True, # Can't be accessed by js
            secure = True, # Only sent over https
            max_age = ACCESS_TOKEN_EXPIRE_UNITS*60 # 30 minutes
        )

    async def get_user_profile(
        self,
        token: str,
    ) -> schemas.UserProfile:
        """Return User instance by jwt token."""
        payload = self.verify_token(token)
        user_id = payload.get("user_id")
        query = (
            sqlalchemy.Select(models.User)
            .where(models.User.id == user_id)
        )
        result = await self.session.execute(query)
        db_user = result.scalar_one_or_none()
        return db_user


    def check_password(
        self,
        password: str,
        user: models.User,
    ) -> bool:
        """Check password from cred are equal to password from db."""
        hash_session = hashlib.sha256()
        hash_session.update(
            bytes(password, encoding="utf-8"),
        )
        hash_password = hash_session.hexdigest()
        return hash_password == getattr(user, "password", None)

    def hash_password(
        self,
        password1: str,
        password2: str,
    ) -> str:
        """Hash password."""
        if (
            password1
            and password1 != password2
        ):
            raise fastapi.HTTPException(
                status_code=400,
                detail={
                    "password": "passwords don't match.",
                }
            )
        hash_session = hashlib.sha256()
        hash_session.update(
            bytes(password1, encoding="utf-8"),
        )
        return hash_session.hexdigest()

    def generate_jwt_token(
            self,
            data: dict,
            is_refresh: bool = True,
    ) -> str:
        """Return jwt token generated by user metadata."""
        to_encode = data.copy()
        time_type = "minuets"
        if is_refresh:
            time_type="days"

        expiring_time = datetime.timedelta(
            **{time_type: ACCESS_TOKEN_EXPIRE_UNITS},
        )
        expire = datetime.datetime.utcnow() + expiring_time
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    def verify_token(self, token: str):
        """Verify token."""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except JWTError:
            raise fastapi.HTTPException(
                status_code=401,
                detail="Could not validate credentials",
            )

    async def revoke_token(self, refresh_token: str):
        """Revoke a refresh token and store its expiration time."""
        try:
            # Decode the refresh token to get its expiration time
            expiration = self.extract_expiration_from_token(refresh_token)

            # Check if the token is already revoked
            query = sqlalchemy.select(models.RevokedToken).filter(RevokedToken.refresh_token == refresh_token)
            result = await self.session.execute(query)
            revoked_token = result.scalars().first()

            if revoked_token:
                # Token has already been revoked
                raise fastapi.HTTPException(
                    status_code=400,  # BAD_REQUEST
                    detail="Token has already been revoked",
                )

            # If the token is not revoked, revoke it by adding it to the revoked tokens table
            new_revoked_token = models.RevokedToken(
                refresh_token=refresh_token,
                expires_at=expiration  # Store the same expiration time from the JWT
            )
            self.session.add(new_revoked_token)
            await self.session.commit()

            return {"message": "Token revoked successfully"}

        except Exception as e:
            # Catch any other exceptions (database issues, etc.)
            raise fastapi.HTTPException(
                status_code=500,  # Internal Server Error
                detail="An error occurred while revoking the token",
            )

    def extract_expiration_from_token(self, token: str) -> datetime.datetime:
        """Decode the JWT and extract the expiration time."""
        try:
            # Decode the JWT token to get the payload (claims)
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

            # Extract the 'exp' claim (expiration time)
            expiration_timestamp = decoded_token.get("exp")

            if expiration_timestamp:
                # Convert the Unix timestamp to a datetime object
                expiration_time = datetime.datetime.fromtimestamp(expiration_timestamp,datetime. UTC)
                return expiration_time
            else:
                raise ValueError("Expiration ('exp') not found in the token")

        except JWTError as e:
            raise ValueError(f"Invalid token: {e}")
