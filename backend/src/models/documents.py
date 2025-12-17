"""
Document models for the AI Backend with RAG + Authentication
Pydantic models for document-related request/response validation
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from uuid import UUID
from datetime import datetime


class DocumentCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, description="Document title")
    content: str = Field(..., min_length=1, description="Document content")
    file_path: Optional[str] = Field(None, max_length=500, description="Path if uploaded file")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class DocumentResponse(BaseModel):
    document_id: UUID
    success: bool
    message: str


class DocumentUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    content: Optional[str] = Field(None, min_length=1)
    metadata: Optional[Dict[str, Any]] = None


class DocumentListResponse(BaseModel):
    documents: list
    total: int