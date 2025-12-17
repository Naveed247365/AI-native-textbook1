"""
Base class for SQLAlchemy models
"""
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, DateTime, func
from sqlalchemy.ext.asyncio import AsyncAttrs
from datetime import datetime
import uuid
from sqlalchemy.dialects.postgresql import UUID


class Base(AsyncAttrs, DeclarativeBase):
    """
    Base class for all SQLAlchemy models
    Includes common columns and configurations
    """
    __abstract__ = True

    # Common columns for all models
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    def __init__(self, *args, **kwargs):
        # Set the id automatically if not provided
        if 'id' not in kwargs and hasattr(self, 'id') and self.id is None:
            # For models that have an id column, set a default UUID if not provided
            pass  # The column default will handle this
        super().__init__(*args, **kwargs)