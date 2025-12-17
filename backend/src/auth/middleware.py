"""
Authentication middleware for the AI Backend with RAG + Authentication
Provides utilities for protecting routes with JWT authentication
"""
from fastapi import HTTPException, status, Request
from typing import Optional
import logging

from .auth import auth_handler, TokenData

logger = logging.getLogger(__name__)

class AuthMiddleware:
    """
    Authentication middleware class to protect routes
    """

    @staticmethod
    async def verify_token(request: Request) -> Optional[TokenData]:
        """
        Verify the JWT token in the request headers
        """
        # Get authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authorization header missing or invalid format",
                headers={"WWW-Authenticate": "Bearer"},
            )

        token = auth_header[7:]  # Remove "Bearer " prefix
        token_data = auth_handler.decode_access_token(token)

        if token_data is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Add user info to request state for use in route handlers
        request.state.user = token_data
        return token_data

    @staticmethod
    async def require_auth(request: Request) -> TokenData:
        """
        Require authentication for a route
        This can be used as a dependency in route handlers
        """
        return await AuthMiddleware.verify_token(request)

    @staticmethod
    async def optional_auth(request: Request) -> Optional[TokenData]:
        """
        Optionally authenticate a user (returns None if no valid token)
        This can be used as a dependency in route handlers
        """
        try:
            return await AuthMiddleware.verify_token(request)
        except HTTPException:
            # If token is invalid or missing, return None instead of raising error
            return None


# Convenience functions for use in route handlers
async def require_auth(request: Request) -> TokenData:
    """Require authentication for a route"""
    return await AuthMiddleware.require_auth(request)

async def optional_auth(request: Request) -> Optional[TokenData]:
    """Optionally authenticate a user"""
    return await AuthMiddleware.optional_auth(request)