"""
Translation model for storing Urdu translations with caching
"""
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, UniqueConstraint, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from database.db import Base


class Translation(Base):
    __tablename__ = "translations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chapter_id = Column(String(255), nullable=False, index=True)
    content_hash = Column(String(64), nullable=False, index=True)
    source_language = Column(String(10), nullable=False, default="english")
    target_language = Column(String(10), nullable=False, index=True)
    original_content = Column(Text, nullable=False)
    translated_content = Column(Text, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Composite unique constraint: one translation per (chapter_id, content_hash, target_language)
    # This ensures we don't duplicate translations when content is the same
    __table_args__ = (
        UniqueConstraint('chapter_id', 'content_hash', 'target_language', name='uq_chapter_hash_language'),
        # Composite index for fast cache lookups
        Index('idx_translations_lookup', 'chapter_id', 'content_hash', 'target_language'),
    )

    def __repr__(self):
        return f"<Translation(chapter_id={self.chapter_id}, target_language={self.target_language}, cached=True)>"
