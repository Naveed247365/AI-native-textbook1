from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ChatSession(BaseModel):
    id: Optional[str] = None
    user_id: str
    selected_text: str
    question: str
    response: str
    created_at: Optional[datetime] = None
    conversation_history: Optional[List[dict]] = []