from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class User(BaseModel):
    id: Optional[str] = None
    email: str
    password: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    software_background: Optional[str] = None  # Software Engineer, Beginner, etc.
    hardware_background: Optional[str] = None  # Hardware Engineer, Beginner, etc.
    experience_level: Optional[str] = None  # Beginner, Intermediate, Advanced