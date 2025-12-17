"""
Unit tests for authentication functionality
"""
import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi.testclient import TestClient
from fastapi import HTTPException
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta

from ..auth.auth import AuthHandler, get_password_hash, verify_password, create_access_token, decode_access_token
from ..auth.schemas import UserCreate, UserLogin, TokenData
from ..config.settings import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@pytest.fixture
def auth_handler():
    """Fixture to create an instance of AuthHandler for testing"""
    return AuthHandler()


@pytest.mark.asyncio
async def test_verify_password():
    """Test password verification"""
    plain_password = "test_password"
    hashed_password = get_password_hash(plain_password)

    # Test correct password
    assert verify_password(plain_password, hashed_password) == True

    # Test incorrect password
    assert verify_password("wrong_password", hashed_password) == False


def test_get_password_hash():
    """Test password hashing"""
    password = "test_password"
    hashed = get_password_hash(password)

    # Verify it's properly hashed
    assert hashed != password
    assert len(hashed) > 0
    assert "$2b$" in hashed  # bcrypt hash identifier


@pytest.mark.asyncio
async def test_create_access_token():
    """Test creating access token"""
    data = {"sub": "test_user", "user_id": "test_id"}
    token = create_access_token(data)

    # Verify token is created
    assert token is not None
    assert isinstance(token, str)
    assert len(token) > 0

    # Decode and verify contents
    decoded = jwt.decode(token, settings.secret_key, algorithms=[settings.jwt_algorithm])
    assert decoded["sub"] == "test_user"
    assert decoded["user_id"] == "test_id"


@pytest.mark.asyncio
async def test_decode_access_token():
    """Test decoding access token"""
    data = {"sub": "test_user", "user_id": "test_id"}
    token = create_access_token(data)

    # Test valid token
    decoded = decode_access_token(token)
    assert decoded is not None
    assert decoded.username == "test_user"
    assert decoded.user_id == "test_id"

    # Test invalid token
    invalid_token = "invalid.token.string"
    decoded_invalid = decode_access_token(invalid_token)
    assert decoded_invalid is None


@pytest.mark.asyncio
async def test_decode_expired_token():
    """Test decoding an expired token"""
    with patch('datetime.datetime') as mock_datetime:
        mock_datetime.utcnow.return_value = datetime.utcnow() - timedelta(days=1)

        data = {"sub": "test_user", "user_id": "test_id"}
        # Create a token that expires immediately
        token = create_access_token(data, expires_delta=timedelta(seconds=-1))

        decoded = decode_access_token(token)
        assert decoded is None


@pytest.mark.asyncio
async def test_auth_handler_creation():
    """Test AuthHandler initialization"""
    auth = AuthHandler()

    assert auth.secret_key == settings.secret_key
    assert auth.algorithm == settings.jwt_algorithm
    assert auth.access_token_expires == timedelta(seconds=settings.jwt_expires_in)


@pytest.mark.asyncio
async def test_get_current_user_dependency():
    """Test the get_current_user dependency function"""
    data = {"sub": "test_user", "user_id": "test_id"}
    token = create_access_token(data)

    # Mock the security dependency
    with patch('fastapi.security.http.HTTPAuthorizationCredentials') as mock_cred:
        mock_cred.credentials = token

        # Test the dependency function (this would normally be used in FastAPI routes)
        # Since we can't easily test the actual dependency injection, we'll test the underlying functionality
        decoded = decode_access_token(token)
        assert decoded is not None
        assert decoded.username == "test_user"


@pytest.mark.asyncio
async def test_password_hash_consistency():
    """Test that password hashing is consistent"""
    password = "consistent_test_password"

    # Hash the same password multiple times
    hash1 = get_password_hash(password)
    hash2 = get_password_hash(password)

    # Different hashes each time (due to salt) but both should verify the same password
    assert hash1 != hash2
    assert verify_password(password, hash1) == True
    assert verify_password(password, hash2) == True