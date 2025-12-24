"""
Translation Feedback API

Endpoint: POST /api/translate/feedback
Purpose: Allow users to report translation quality issues
"""

from fastapi import APIRouter, Depends, HTTPException, Header
from pydantic import BaseModel, Field
from auth.jwt_utils import get_current_user_id_from_token
from database.db import get_db
from models.translation_feedback import TranslationFeedback
from sqlalchemy import select
from database.models import Translation
import uuid
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


# JWT verification dependency
def verify_jwt_token(authorization: str = Header(None)) -> dict:
    """Verify JWT token from Authorization header"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization format")

    token = authorization[7:]  # Remove "Bearer " prefix
    user_id = get_current_user_id_from_token(token)

    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return {"user_id": user_id}


class FeedbackRequest(BaseModel):
    """Request model for submitting translation feedback"""
    translation_id: str = Field(..., description="UUID of the translation being reported")
    issue_description: str = Field(..., min_length=10, max_length=2000, description="Description of the translation issue")


class FeedbackResponse(BaseModel):
    """Response model for feedback submission"""
    feedback_id: str
    message: str


@router.post("/api/translate/feedback", response_model=FeedbackResponse, status_code=201)
def submit_translation_feedback(
    request: FeedbackRequest,
    user_data: dict = Depends(verify_jwt_token),
    db = Depends(get_db)
):
    """
    Submit feedback on translation quality

    **Authentication**: JWT token required

    **Request Body**:
    - translation_id: UUID of the translation
    - issue_description: Description of the issue (10-2000 characters)

    **Response**: 201 Created with feedback_id
    """
    user_id = user_data["user_id"]

    try:
        # Validate translation_id is a valid UUID
        translation_uuid = uuid.UUID(request.translation_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid translation_id format. Must be a valid UUID.")

    try:
        # Optional: Verify translation exists (can skip for better performance)
        # result = await db.execute(select(Translation).where(Translation.id == translation_uuid))
        # translation = result.scalar_one_or_none()
        # if not translation:
        #     raise HTTPException(status_code=404, detail="Translation not found")

        # Create feedback record
        feedback = TranslationFeedback(
            id=uuid.uuid4(),
            translation_id=translation_uuid,
            user_id=uuid.UUID(user_id),
            issue_description=request.issue_description.strip()
        )

        db.add(feedback)
        db.commit()
        db.refresh(feedback)

        logger.info(f"Feedback submitted: feedback_id={feedback.id}, translation_id={translation_uuid}, user_id={user_id}")

        return FeedbackResponse(
            feedback_id=str(feedback.id),
            message="Thank you for your feedback! We'll review the translation quality issue."
        )

    except Exception as e:
        logger.error(f"Failed to submit feedback: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to submit feedback: {str(e)}")
