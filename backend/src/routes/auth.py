"""
Authentication API routes for the AI Backend with RAG + Authentication
Implements signup, login, and user profile endpoints
"""
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPBearer
import logging
from typing import Optional
from uuid import UUID
import re

from ..auth.auth import AuthHandler
from ..models.auth import UserCreate, UserLogin, Token
from ..config.settings import settings
from ..config.database import get_db_session
from ..db import crud
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/auth", tags=["authentication"])

logger = logging.getLogger(__name__)

# Initialize auth handler
auth_handler = AuthHandler()


@router.post("/signup", response_model=Token)
async def signup(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db_session)
):
    """
    Register a new user
    """
    try:
        # Validate email format
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, user_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid email format"
            )

        # Check if user already exists
        existing_user = await crud.get_user_by_email(db, user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists"
            )

        # Create new user with hashed password
        hashed_password = auth_handler.get_password_hash(user_data.password)
        db_user = await crud.create_user(
            db,
            email=user_data.email,
            hashed_password=hashed_password,
            full_name=user_data.full_name
        )

        # Create access token
        access_token = auth_handler.create_access_token(str(db_user.id))

        logger.info(f"New user registered: {user_data.email}")

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during user registration: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during registration"
        )


@router.post("/login", response_model=Token)
async def login(
    user_credentials: UserLogin,
    db: AsyncSession = Depends(get_db_session)
):
    """
    Authenticate user and return access token
    """
    try:
        # Find user by email
        user = await crud.get_user_by_email(db, user_credentials.email)

        if not user or not auth_handler.verify_password(user_credentials.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Inactive user",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Create access token
        access_token = auth_handler.create_access_token(str(user.id))

        logger.info(f"User logged in: {user_credentials.email}")

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during user login: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during login"
        )


@router.get("/me")
async def get_current_user(
    current_user_id: str = Depends(auth_handler.get_current_user),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Get current user profile
    """
    try:
        user = await crud.get_user_by_id(db, UUID(current_user_id))

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        return {
            "id": str(user.id),
            "email": user.email,
            "full_name": user.full_name,
            "is_active": user.is_active,
            "created_at": user.created_at
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving user profile: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving user profile"
        )