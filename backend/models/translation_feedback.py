"""
TranslationFeedback Model

Purpose: Store user feedback on translation quality for improvement
"""

from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from database.db import Base


class TranslationFeedback(Base):
    __tablename__ = "translation_feedback"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    translation_id = Column(
        UUID(as_uuid=True),
        ForeignKey("translations.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    issue_description = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<TranslationFeedback(translation_id={self.translation_id}, user_id={self.user_id}, issue='{self.issue_description[:50]}...')>"
