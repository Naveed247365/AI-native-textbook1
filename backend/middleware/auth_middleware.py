from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from typing import Optional
import os

class JWTAuth:
    def __init__(self, secret_key: str = None, algorithm: str = "HS256"):
        self.secret_key = secret_key or os.getenv("JWT_SECRET_KEY", "your-secret-key-here")
        self.algorithm = algorithm
        self.security = HTTPBearer()

    async def __call__(self, request: Request) -> Optional[dict]:
        credentials: HTTPAuthorizationCredentials = await self.security(request)

        if credentials:
            token = credentials.credentials
            try:
                # Decode the JWT token
                payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
                request.state.user = payload
                return payload
            except jwt.ExpiredSignatureError:
                raise HTTPException(status_code=401, detail="Token has expired")
            except jwt.InvalidTokenError:
                raise HTTPException(status_code=401, detail="Invalid token")
        else:
            raise HTTPException(status_code=401, detail="No authorization token provided")

# Example usage in routes:
# @router.get("/protected-route")
# async def protected_route(request: Request, user: dict = Depends(JWTAuth())):
#     return {"message": f"Hello {user.get('email')}, you are authenticated!"}

# For now, we'll create a simple dependency that can be used to require authentication
async def require_auth(request: Request):
    """Simple dependency to require authentication (placeholder for real implementation)"""
    # In a real implementation, this would validate the JWT token
    # For now, we'll just check if there's a mock token in the header
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authorization header missing or invalid")

    # In a real app, you would validate the JWT here
    # For demo purposes, we'll just continue
    pass