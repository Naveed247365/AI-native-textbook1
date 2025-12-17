"""
Authentication module for the AI Backend with RAG + Authentication
Implements JWT-based authentication with password hashing
"""
from datetime import datetime, timedelta
from typing import Optional, Union
import jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import logging

from ..config.settings import settings

logger = logging.getLogger(__name__)

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT security scheme
security = HTTPBearer()

class TokenData(BaseModel):
    username: Optional[str] = None
    user_id: Optional[str] = None


class AuthHandler:
    def __init__(self):
        self.secret_key = settings.secret_key
        self.algorithm = settings.jwt_algorithm
        self.access_token_expires = timedelta(minutes=settings.jwt_expires_in // 60)  # Convert seconds to minutes

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verify a plain password against a hashed password
        """
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        """
        Generate a hash for a plain password
        """
        return pwd_context.hash(password)

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """
        Create a JWT access token with optional expiration time
        """
        to_encode = data.copy()

        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + self.access_token_expires

        to_encode.update({"exp": expire, "iat": datetime.utcnow()})

        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def decode_access_token(self, token: str) -> Optional[TokenData]:
        """
        Decode a JWT token and return token data
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            username: str = payload.get("sub")
            user_id: str = payload.get("user_id")

            if username is None:
                return None

            token_data = TokenData(username=username, user_id=user_id)
            return token_data
        except jwt.exceptions.ExpiredSignatureError:
            logger.warning("Expired token attempted to be decoded")
            return None
        except jwt.exceptions.InvalidTokenError:
            logger.warning("Invalid token attempted to be decoded")
            return None

    async def get_current_user(self, token: str = Depends(security)) -> TokenData:
        """
        Get the current user from the provided JWT token
        This function can be used as a dependency in route handlers
        """
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            token_data = self.decode_access_token(token.credentials)
            if token_data is None:
                raise credentials_exception
            return token_data
        except Exception as e:
            logger.error(f"Error getting current user: {e}")
            raise credentials_exception


# Create a global instance of AuthHandler
auth_handler = AuthHandler()

# Convenience functions for use in other modules
def get_password_hash(password: str) -> str:
    """Generate a hash for a plain password"""
    return auth_handler.get_password_hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password"""
    return auth_handler.verify_password(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token"""
    return auth_handler.create_access_token(data, expires_delta)

def decode_access_token(token: str) -> Optional[TokenData]:
    """Decode a JWT token and return token data"""
    return auth_handler.decode_access_token(token)

async def get_current_user(token: str = Depends(security)) -> TokenData:
    """Get the current user from the provided JWT token"""
    return await auth_handler.get_current_user(token)

def create_user_token(user_id: str, username: str) -> str:
    """Create a token specifically for a user"""
    data = {"sub": username, "user_id": user_id}
    return create_access_token(data)