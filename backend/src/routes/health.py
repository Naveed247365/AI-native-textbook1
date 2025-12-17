"""
Health Check API routes for the AI Backend with RAG + Authentication
Implements health check endpoints for all services
"""
from fastapi import APIRouter, HTTPException, status
import logging
import asyncio
from typing import Dict, Any
from datetime import datetime
import socket
import time

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from ..config.database import get_db_session
from ..config.settings import settings
from ..qdrant.client import qdrant_client
from ..embeddings.gemini_client import generate_embedding

router = APIRouter(tags=["health"])

logger = logging.getLogger(__name__)


@router.get("/")
async def health_check() -> Dict[str, Any]:
    """
    Basic health check endpoint
    """
    return {
        "status": "healthy",
        "service": "AI Backend",
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/detailed")
async def detailed_health_check() -> Dict[str, Any]:
    """
    Detailed health check for all services
    """
    checks = {
        "status": "healthy",
        "service": "AI Backend with RAG + Authentication",
        "timestamp": datetime.utcnow().isoformat(),
        "checks": {
            "database": {
                "status": "unavailable",
                "details": ""
            },
            "vector_store": {
                "status": "unavailable",
                "details": ""
            },
            "ai_service": {
                "status": "unavailable",
                "details": ""
            },
            "server": {
                "status": "healthy",
                "details": "Server is running"
            }
        }
    }

    # Check database connection
    try:
        from ..config.database import engine
        async with engine.begin() as conn:
            result = await conn.execute(text("SELECT 1"))
            _ = result.fetchone()
        checks["checks"]["database"] = {
            "status": "healthy",
            "details": "Database connection established"
        }
    except Exception as e:
        checks["checks"]["database"] = {
            "status": "unhealthy",
            "details": f"Database connection failed: {str(e)}"
        }
        checks["status"] = "unhealthy"

    # Check vector store (Qdrant) connection
    try:
        # Try to get collection list to verify connection
        collections = await qdrant_client.get_collections()
        checks["checks"]["vector_store"] = {
            "status": "healthy",
            "details": f"Qdrant connection established, {len(collections.collections)} collections available"
        }
    except Exception as e:
        checks["checks"]["vector_store"] = {
            "status": "unhealthy",
            "details": f"Vector store connection failed: {str(e)}"
        }
        checks["status"] = "unhealthy"

    # Check AI service (Gemini) connection
    try:
        # Generate a simple embedding to test the API
        test_text = "health check"
        embedding = await generate_embedding(test_text)

        if embedding and len(embedding) > 0:
            checks["checks"]["ai_service"] = {
                "status": "healthy",
                "details": f"Gemini API connection established, embedding dimension: {len(embedding)}"
            }
        else:
            checks["checks"]["ai_service"] = {
                "status": "unhealthy",
                "details": "Gemini API returned empty embedding"
            }
            checks["status"] = "unhealthy"
    except Exception as e:
        checks["checks"]["ai_service"] = {
            "status": "unhealthy",
            "details": f"AI service connection failed: {str(e)}"
        }
        checks["status"] = "unhealthy"

    # Overall status depends on all checks
    if any(check["status"] == "unhealthy" for check in checks["checks"].values()):
        checks["status"] = "unhealthy"

    return checks


@router.get("/ready")
async def readiness_check() -> Dict[str, Any]:
    """
    Readiness check - determines if the service is ready to accept traffic
    """
    # For readiness, we check if all critical services are available
    try:
        # Check database
        from ..config.database import engine
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))

        # Check Qdrant connection
        collections = await qdrant_client.get_collections()

        # If we reach this point, all critical services are available
        return {
            "status": "ready",
            "service": "AI Backend",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Readiness check failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service not ready"
        )


@router.get("/live")
async def liveness_check() -> Dict[str, Any]:
    """
    Liveness check - determines if the service is alive and functioning
    """
    # Basic liveness check - service is running
    return {
        "status": "alive",
        "service": "AI Backend",
        "timestamp": datetime.utcnow().isoformat(),
        "uptime_seconds": time.time() - getattr(router, '_startup_time', time.time())
    }


# Set startup time for liveness check
router._startup_time = time.time()