"""
Search models for the AI Backend with RAG + Authentication
Pydantic models for search-related request/response validation
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from uuid import UUID


class SearchRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=1000, description="Search query")
    top_k: Optional[int] = Field(default=5, ge=1, le=20, description="Number of results to return")
    filters: Optional[Dict[str, Any]] = Field(None, description="Additional filters for search")


class SearchResult(BaseModel):
    id: str
    document_id: str
    score: float
    payload: Dict[str, Any]


class SearchResponse(BaseModel):
    results: List[SearchResult]
    query: str
    total_results: int


class Message(BaseModel):
    role: str = Field(..., pattern=r"^(user|assistant|system)$", description="Role of the message sender")
    content: str = Field(..., min_length=1, description="Content of the message")


class ChatRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=1000, description="Chat query")
    top_k: Optional[int] = Field(default=5, ge=1, le=10, description="Number of context results to retrieve")
    conversation_history: Optional[List[Message]] = Field(None, description="Previous conversation messages")


class ChatResponse(BaseModel):
    response: str
    sources: List[Dict[str, Any]]
    context_used: List[Dict[str, Any]]