from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserProfile(BaseModel):
    id: Optional[str] = None
    user_id: str
    software_background: Optional[str] = None  # Software Engineer, Beginner, etc.
    hardware_background: Optional[str] = None  # Hardware Engineer, Beginner, etc.
    experience_level: Optional[str] = None  # Beginner, Intermediate, Advanced
    personalization_settings: Optional[dict] = {}
    learning_progress: Optional[dict] = {}
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None