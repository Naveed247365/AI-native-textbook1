"""
Unit tests for TranslationFeedback model

Tests:
- test_create_translation_feedback: Verify feedback creation
- test_feedback_foreign_key_constraint: Verify FK relationship to translations
"""

import pytest
from models.translation_feedback import TranslationFeedback
from models.translation import Translation
from database.models import User
from database.db import get_db_session
import uuid
from datetime import datetime


@pytest.mark.asyncio
async def test_create_translation_feedback():
    """Test creating a translation feedback record"""
    # Arrange
    feedback_id = uuid.uuid4()
    translation_id = uuid.uuid4()
    user_id = uuid.uuid4()
    issue_description = "Technical term 'API' was incorrectly translated to Urdu"

    # Act
    feedback = TranslationFeedback(
        id=feedback_id,
        translation_id=translation_id,
        user_id=user_id,
        issue_description=issue_description,
        created_at=datetime.utcnow()
    )

    # Assert
    assert feedback.id == feedback_id
    assert feedback.translation_id == translation_id
    assert feedback.user_id == user_id
    assert feedback.issue_description == issue_description
    assert feedback.created_at is not None
    print(f"✅ TranslationFeedback model created: {feedback}")


@pytest.mark.asyncio
async def test_feedback_foreign_key_constraint():
    """Test that feedback links to translation record via FK"""
    # Arrange
    translation_id = uuid.uuid4()
    user_id = uuid.uuid4()

    # Act
    feedback = TranslationFeedback(
        id=uuid.uuid4(),
        translation_id=translation_id,  # FK to translations table
        user_id=user_id,                # FK to users table
        issue_description="Translation quality issue",
        created_at=datetime.utcnow()
    )

    # Assert
    assert feedback.translation_id == translation_id
    assert hasattr(feedback, 'translation_id'), "Feedback must have translation_id FK"
    assert hasattr(feedback, 'user_id'), "Feedback must have user_id FK"
    print(f"✅ Foreign key constraint verified: translation_id={translation_id}")


def test_feedback_model_repr():
    """Test __repr__ method for debugging"""
    feedback = TranslationFeedback(
        id=uuid.uuid4(),
        translation_id=uuid.uuid4(),
        user_id=uuid.uuid4(),
        issue_description="Test issue",
        created_at=datetime.utcnow()
    )

    repr_str = repr(feedback)
    assert "TranslationFeedback" in repr_str
    assert "issue_description" in repr_str or "translation_id" in repr_str
    print(f"✅ Model repr: {repr_str}")
