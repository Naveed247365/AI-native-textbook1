from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from services.translation_service import TranslationService
import os

router = APIRouter()

class TranslationRequest(BaseModel):
    text: str
    source_lang: str = "en"
    target_lang: str = "ur"

class TranslationResponse(BaseModel):
    original_text: str
    translated_text: str
    source_lang: str
    target_lang: str

@router.post("/translation/translate", response_model=TranslationResponse)
async def translate_text(request: TranslationRequest):
    """Translate text between languages (currently English to Urdu)"""
    try:
        # Initialize translation service
        translation_service = TranslationService(
            gemini_api_key=os.getenv("GEMINI_API_KEY", "your-gemini-key-here")
        )

        if request.source_lang == "en" and request.target_lang == "ur":
            # Translate English to Urdu
            translated_text = translation_service.translate_to_urdu(request.text)
        elif request.source_lang == "ur" and request.target_lang == "en":
            # Translate Urdu to English
            translated_text = translation_service.translate_to_english(request.text)
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported language pair: {request.source_lang} to {request.target_lang}. Currently supported: en-ur"
            )

        return TranslationResponse(
            original_text=request.text,
            translated_text=translated_text,
            source_lang=request.source_lang,
            target_lang=request.target_lang
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during translation: {str(e)}")

@router.get("/translation/health")
async def translation_health():
    """Health check for translation service"""
    return {"status": "translation service is running"}

@router.post("/translation/clear-cache")
async def clear_translation_cache():
    """Clear the translation cache"""
    try:
        translation_service = TranslationService(
            gemini_api_key=os.getenv("GEMINI_API_KEY", "your-gemini-key-here")
        )
        translation_service.clear_cache()
        return {"status": "translation cache cleared"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing cache: {str(e)}")