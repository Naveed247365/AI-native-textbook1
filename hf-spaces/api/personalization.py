from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, Dict, Any
import os
import logging
from services.personalization_service import PersonalizationService
from services.content_adaptation import ContentAdaptationService

logger = logging.getLogger(__name__)

router = APIRouter()

class PersonalizationRequest(BaseModel):
    content: str
    user_profile: Dict[str, Any]
    chapter_id: str

class PersonalizationResponse(BaseModel):
    personalized_content: str
    adaptation_details: Dict[str, Any]

@router.post("/personalization/adapt", response_model=PersonalizationResponse)
async def adapt_content(request: PersonalizationRequest):
    """Adapt content based on user profile and background"""
    try:
        # Initialize content adaptation service
        content_adaptation_service = ContentAdaptationService(
            gemini_api_key=os.getenv("GEMINI_API_KEY", "your-gemini-key-here")
        )

        # Initialize personalization service with content adaptation service
        personalization_service = PersonalizationService(content_adaptation_service)

        # Adapt the content based on user profile
        adapted_content = personalization_service.get_personalized_content(
            content=request.content,
            user_profile=request.user_profile,
            chapter_id=request.chapter_id
        )

        # Prepare adaptation details
        adaptation_details = {
            "status": "success",
            "user_software_background": request.user_profile.get('software_background', 'General'),
            "user_hardware_background": request.user_profile.get('hardware_background', 'General'),
            "user_experience_level": request.user_profile.get('experience_level', 'Intermediate'),
            "chapter_id": request.chapter_id,
            "adaptation_method": "AI-driven personalization"
        }

        return PersonalizationResponse(
            personalized_content=adapted_content,
            adaptation_details=adaptation_details
        )

    except Exception as e:
        logger.error(f"Error adapting content: {str(e)}")
        # Return original content if personalization fails, but still provide a response
        return PersonalizationResponse(
            personalized_content=request.content,
            adaptation_details={
                "status": "fallback",
                "message": "Content personalization is temporarily unavailable. Showing original content.",
                "original_chapter_id": request.chapter_id
            }
        )

@router.get("/personalization/health")
async def personalization_health():
    """Health check for personalization service"""
    return {"status": "personalization service is running"}