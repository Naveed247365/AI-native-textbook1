"""
Document model for the AI Backend with RAG + Authentication
"""
from sqlalchemy import Column, String, Text, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID, JSON
from sqlalchemy.orm import relationship
from uuid import uuid4
from ...db.base import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    content_hash = Column(String(255), nullable=False, index=True)  # For deduplication
    file_path = Column(String(500), nullable=True)  # Path if uploaded file
    metadata = Column(JSON, nullable=True)  # Additional metadata as JSON

    # Relationships
    user = relationship("User", back_populates="documents")

    def __repr__(self):
        return f"<Document(id={self.id}, user_id={self.user_id}, title='{self.title}')>"

# Create indexes
Index('idx_document_user_id', 'user_id')
Index('idx_document_content_hash', 'content_hash')
Index('idx_document_title', 'title')