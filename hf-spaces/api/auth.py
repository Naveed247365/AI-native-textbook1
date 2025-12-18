from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from models.user import User
from models.user_profile import UserProfile
import os
import bcrypt

router = APIRouter()

class SignupRequest(BaseModel):
    email: str
    password: str
    software_background: Optional[str] = None
    hardware_background: Optional[str] = None
    experience_level: Optional[str] = None

class LoginRequest(BaseModel):
    email: str
    password: str

class AuthResponse(BaseModel):
    user_id: str
    email: str
    access_token: str
    refresh_token: str

@router.post("/auth/signup", response_model=AuthResponse)
async def signup(request: SignupRequest):
    """Handle user registration with background information"""
    try:
        # In a real implementation, you would hash the password and store user in DB
        # For now, we'll simulate the process

        # Hash the password
        hashed_password = bcrypt.hashpw(request.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Create user object
        user = User(
            email=request.email,
            password=hashed_password,  # In real app, don't return the hash
            software_background=request.software_background,
            hardware_background=request.hardware_background,
            experience_level=request.experience_level
        )

        # Create user profile
        user_profile = UserProfile(
            user_id="temp_user_id",  # In real app, this would be the actual user ID
            software_background=request.software_background,
            hardware_background=request.hardware_background,
            experience_level=request.experience_level
        )

        # In a real implementation, you would store these in the database
        # and generate proper JWT tokens

        # For now, return a mock response
        return AuthResponse(
            user_id="temp_user_id",
            email=request.email,
            access_token="mock_access_token",
            refresh_token="mock_refresh_token"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during signup: {str(e)}")

@router.post("/auth/login", response_model=AuthResponse)
async def login(request: LoginRequest):
    """Handle user login"""
    try:
        # In a real implementation, you would verify credentials against DB
        # For now, we'll simulate the process

        # For demo purposes, we'll just return a mock response
        # In a real app, you'd verify the password and generate tokens
        return AuthResponse(
            user_id="temp_user_id",
            email=request.email,
            access_token="mock_access_token",
            refresh_token="mock_refresh_token"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during login: {str(e)}")

@router.get("/auth/profile")
async def get_profile():
    """Get user profile information"""
    try:
        # In a real implementation, you would retrieve from DB based on auth token
        profile = UserProfile(
            user_id="temp_user_id",
            software_background="Software Engineer",
            hardware_background="Beginner",
            experience_level="Intermediate"
        )

        return profile

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving profile: {str(e)}")

@router.get("/auth/health")
async def auth_health():
    """Health check for auth service"""
    return {"status": "auth service is running"}