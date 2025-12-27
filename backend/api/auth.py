from fastapi import APIRouter, HTTPException, Depends, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from typing import Optional
import logging

logger = logging.getLogger(__name__)
router = APIRouter()
security = HTTPBearer(auto_error=False)

# Import database utilities
try:
    from database.db import get_db
    from database.models import User as DBUser
    from auth.jwt_utils import hash_password, verify_password, create_access_token, get_current_user_id_from_token
    from sqlalchemy.orm import Session
    from sqlalchemy.exc import IntegrityError
    DB_ENABLED = True
except ImportError:
    DB_ENABLED = False
    get_db = None
    logging.warning("Database modules not available. Auth will use mock mode.")

class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    software_background: Optional[str] = None
    hardware_background: Optional[str] = None
    experience_level: Optional[str] = "Intermediate"

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class AuthResponse(BaseModel):
    user_id: str
    email: str
    access_token: str
    token_type: str = "bearer"

class UserProfileResponse(BaseModel):
    user_id: str
    email: str
    software_background: Optional[str]
    hardware_background: Optional[str]
    experience_level: Optional[str]


def get_db_session():
    """Get database session or None if DB not enabled"""
    if DB_ENABLED and get_db:
        return Depends(get_db)
    return None


@router.post("/auth/signup", response_model=AuthResponse)
async def signup(request: SignupRequest):
    """Handle user registration with background information"""
    try:
        if not DB_ENABLED:
            # Mock mode for testing without database
            return AuthResponse(
                user_id="mock_user_id",
                email=request.email,
                access_token="mock_access_token",
                token_type="bearer"
            )

        # Get database session
        from database.db import SessionLocal
        db = SessionLocal()

        try:
            # Validate password strength
            if len(request.password) < 8:
                raise HTTPException(status_code=400, detail="Password must be at least 8 characters long")

            # Validate background fields
            if request.software_background and len(request.software_background) < 10:
                raise HTTPException(status_code=400, detail="Software background must be at least 10 characters")
            if request.hardware_background and len(request.hardware_background) < 10:
                raise HTTPException(status_code=400, detail="Hardware background must be at least 10 characters")

            # Hash the password
            hashed_password = hash_password(request.password)

            # Create new user in database
            db_user = DBUser(
                email=request.email,
                password_hash=hashed_password,
                software_background=request.software_background,
                hardware_background=request.hardware_background,
                experience_level=request.experience_level or "Intermediate"
            )

            db.add(db_user)
            db.commit()
            db.refresh(db_user)

            # Generate JWT token
            access_token = create_access_token(data={
                "sub": str(db_user.id),
                "email": db_user.email
            })

            return AuthResponse(
                user_id=str(db_user.id),
                email=db_user.email,
                access_token=access_token,
                token_type="bearer"
            )

        except IntegrityError:
            db.rollback()
            raise HTTPException(status_code=400, detail="Email already registered")
        finally:
            db.close()

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during signup: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error during signup: {str(e)}")


@router.post("/auth/login", response_model=AuthResponse)
async def login(request: LoginRequest):
    """Handle user login"""
    try:
        if not DB_ENABLED:
            # Mock mode for testing without database
            return AuthResponse(
                user_id="mock_user_id",
                email=request.email,
                access_token="mock_access_token",
                token_type="bearer"
            )

        # Get database session
        from database.db import SessionLocal
        db = SessionLocal()

        try:
            # Find user by email
            user = db.query(DBUser).filter(DBUser.email == request.email).first()
            if not user:
                raise HTTPException(status_code=401, detail="Invalid credentials")

            # Verify password
            if not verify_password(request.password, user.password_hash):
                raise HTTPException(status_code=401, detail="Invalid credentials")

            # Generate JWT token
            access_token = create_access_token(data={
                "sub": str(user.id),
                "email": user.email
            })

            return AuthResponse(
                user_id=str(user.id),
                email=user.email,
                access_token=access_token,
                token_type="bearer"
            )

        finally:
            db.close()

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during login: {str(e)}")
        raise HTTPException(status_code=500, detail="Error during login")


@router.get("/auth/profile", response_model=UserProfileResponse)
async def get_profile(
    authorization: Optional[str] = Header(None),
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
):
    """Get user profile information"""
    try:
        if not DB_ENABLED:
            # Mock mode for testing without database
            return UserProfileResponse(
                user_id="mock_user_id",
                email="mock@example.com",
                software_background="Python, JavaScript",
                hardware_background="Arduino, Raspberry Pi",
                experience_level="Intermediate"
            )

        # Get token from Authorization header or credentials
        token = None
        if credentials:
            token = credentials.credentials
        elif authorization and authorization.startswith("Bearer "):
            token = authorization.replace("Bearer ", "")

        if not token:
            raise HTTPException(status_code=401, detail="Authorization token required")

        # Decode token and get user ID
        user_id = get_current_user_id_from_token(token)
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid or expired token")

        # Get database session
        from database.db import SessionLocal
        db = SessionLocal()

        try:
            # Get user from database
            user = db.query(DBUser).filter(DBUser.id == user_id).first()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            return UserProfileResponse(
                user_id=str(user.id),
                email=user.email,
                software_background=user.software_background,
                hardware_background=user.hardware_background,
                experience_level=user.experience_level
            )
        finally:
            db.close()

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving profile: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving profile")


@router.get("/auth/health")
async def auth_health():
    """Health check for auth service"""
    return {
        "status": "auth service is running",
        "database_enabled": DB_ENABLED
    }
