"""
ChatHistory model for the AI Backend with RAG + Authentication
"""
from sqlalchemy import Column, String, Text, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from uuid import uuid4
from ...db.base import Base


class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    query = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    context_used = Column(Text, nullable=True)  # JSON string of context snippets used

    # Relationships
    user = relationship("User", back_populates="chat_histories")

    def __repr__(self):
        return f"<ChatHistory(id={self.id}, user_id={self.user_id}, query='{self.query[:30]}...')>"

# Create indexes
Index('idx_chat_history_user_id', 'user_id')
Index('idx_chat_history_created_at', 'created_at')