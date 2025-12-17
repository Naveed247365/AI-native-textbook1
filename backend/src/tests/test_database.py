"""
Unit tests for database operations
"""
import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine
from uuid import uuid4
from datetime import datetime

from ..db.models.user import User
from ..db.models.chat_history import ChatHistory
from ..db.models.document import Document
from ..db import crud


@pytest.mark.asyncio
async def test_create_user():
    """Test creating a user"""
    # Mock database session
    mock_db = AsyncMock(spec=AsyncSession)

    # Mock the user to be returned
    user_id = uuid4()
    mock_user = User(
        id=user_id,
        email="test@example.com",
        hashed_password="hashed_password",
        full_name="Test User",
        is_active=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    # Configure the mock to return the user when commit and refresh are called
    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.return_value = None

    with patch('..db.crud.User', return_value=mock_user):
        result = await crud.create_user(mock_db, "test@example.com", "hashed_password", "Test User")

        # Verify the database methods were called
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once()

        assert result.email == "test@example.com"
        assert result.full_name == "Test User"


@pytest.mark.asyncio
async def test_get_user_by_id():
    """Test getting a user by ID"""
    mock_db = AsyncMock(spec=AsyncSession)
    user_id = uuid4()

    mock_user = User(
        id=user_id,
        email="test@example.com",
        hashed_password="hashed_password",
        full_name="Test User",
        is_active=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    # Mock the execute method to return the user
    mock_execute_result = MagicMock()
    mock_execute_result.scalar_one_or_none.return_value = mock_user

    with patch.object(mock_db, 'execute', return_value=mock_execute_result):
        result = await crud.get_user_by_id(mock_db, user_id)

        assert result == mock_user
        assert result.email == "test@example.com"


@pytest.mark.asyncio
async def test_get_user_by_email():
    """Test getting a user by email"""
    mock_db = AsyncMock(spec=AsyncSession)
    email = "test@example.com"

    mock_user = User(
        id=uuid4(),
        email=email,
        hashed_password="hashed_password",
        full_name="Test User",
        is_active=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    # Mock the execute method to return the user
    mock_execute_result = MagicMock()
    mock_execute_result.scalar_one_or_none.return_value = mock_user

    with patch.object(mock_db, 'execute', return_value=mock_execute_result):
        result = await crud.get_user_by_email(mock_db, email)

        assert result == mock_user
        assert result.email == email


@pytest.mark.asyncio
async def test_update_user():
    """Test updating a user"""
    mock_db = AsyncMock(spec=AsyncSession)
    user_id = uuid4()

    mock_updated_user = User(
        id=user_id,
        email="updated@example.com",
        hashed_password="new_hashed_password",
        full_name="Updated User",
        is_active=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    # Mock the execute method to return the updated user
    mock_execute_result = MagicMock()
    mock_execute_result.scalar_one_or_none.return_value = mock_updated_user

    with patch.object(mock_db, 'execute', return_value=mock_execute_result):
        result = await crud.update_user(mock_db, user_id, email="updated@example.com", full_name="Updated User")

        assert result == mock_updated_user
        assert result.email == "updated@example.com"
        assert result.full_name == "Updated User"


@pytest.mark.asyncio
async def test_delete_user():
    """Test deleting a user"""
    mock_db = AsyncMock(spec=AsyncSession)
    user_id = uuid4()

    # Mock the execute method to return a result with rowcount
    mock_execute_result = MagicMock()
    mock_execute_result.rowcount = 1  # Simulate 1 row deleted

    with patch.object(mock_db, 'execute', return_value=mock_execute_result):
        result = await crud.delete_user(mock_db, user_id)

        assert result == True  # Should return True when user was deleted


@pytest.mark.asyncio
async def test_create_chat_history():
    """Test creating chat history"""
    mock_db = AsyncMock(spec=AsyncSession)
    user_id = uuid4()

    mock_chat_history = ChatHistory(
        id=uuid4(),
        user_id=user_id,
        query="Test query?",
        response="Test response",
        context_used="Test context",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.return_value = None

    result = await crud.create_chat_history(mock_db, user_id, "Test query?", "Test response", "Test context")

    # Verify the database methods were called
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()


@pytest.mark.asyncio
async def test_get_chat_history_by_id():
    """Test getting chat history by ID"""
    mock_db = AsyncMock(spec=AsyncSession)
    chat_history_id = uuid4()

    mock_chat_history = ChatHistory(
        id=chat_history_id,
        user_id=uuid4(),
        query="Test query?",
        response="Test response",
        context_used="Test context",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    # Mock the execute method to return the chat history
    mock_execute_result = MagicMock()
    mock_execute_result.scalar_one_or_none.return_value = mock_chat_history

    with patch.object(mock_db, 'execute', return_value=mock_execute_result):
        result = await crud.get_chat_history_by_id(mock_db, chat_history_id)

        assert result == mock_chat_history
        assert result.query == "Test query?"


@pytest.mark.asyncio
async def test_create_document():
    """Test creating a document"""
    mock_db = AsyncMock(spec=AsyncSession)
    user_id = uuid4()

    mock_document = Document(
        id=uuid4(),
        user_id=user_id,
        title="Test Document",
        content="Test content",
        content_hash="hash123",
        file_path=None,
        metadata=None,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.return_value = None

    result = await crud.create_document(
        mock_db, user_id, "Test Document", "Test content", "hash123", None, None
    )

    # Verify the database methods were called
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()


@pytest.mark.asyncio
async def test_get_document_by_id():
    """Test getting a document by ID"""
    mock_db = AsyncMock(spec=AsyncSession)
    document_id = uuid4()

    mock_document = Document(
        id=document_id,
        user_id=uuid4(),
        title="Test Document",
        content="Test content",
        content_hash="hash123",
        file_path=None,
        metadata=None,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    # Mock the execute method to return the document
    mock_execute_result = MagicMock()
    mock_execute_result.scalar_one_or_none.return_value = mock_document

    with patch.object(mock_db, 'execute', return_value=mock_execute_result):
        result = await crud.get_document_by_id(mock_db, document_id)

        assert result == mock_document
        assert result.title == "Test Document"


@pytest.mark.asyncio
async def test_get_documents_by_user():
    """Test getting documents by user"""
    mock_db = AsyncMock(spec=AsyncSession)
    user_id = uuid4()

    mock_document = Document(
        id=uuid4(),
        user_id=user_id,
        title="Test Document",
        content="Test content",
        content_hash="hash123",
        file_path=None,
        metadata=None,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    # Mock the execute method to return a list of documents
    mock_execute_result = MagicMock()
    mock_execute_result.scalars.return_value.all.return_value = [mock_document]

    with patch.object(mock_db, 'execute', return_value=mock_execute_result):
        result = await crud.get_documents_by_user(mock_db, user_id)

        assert len(result) == 1
        assert result[0].title == "Test Document"


@pytest.mark.asyncio
async def test_update_document():
    """Test updating a document"""
    mock_db = AsyncMock(spec=AsyncSession)
    document_id = uuid4()

    mock_updated_document = Document(
        id=document_id,
        user_id=uuid4(),
        title="Updated Document",
        content="Updated content",
        content_hash="newhash123",
        file_path=None,
        metadata=None,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    # Mock the execute method to return the updated document
    mock_execute_result = MagicMock()
    mock_execute_result.scalar_one_or_none.return_value = mock_updated_document

    with patch.object(mock_db, 'execute', return_value=mock_execute_result):
        result = await crud.update_document(mock_db, document_id, title="Updated Document")

        assert result == mock_updated_document
        assert result.title == "Updated Document"


@pytest.mark.asyncio
async def test_delete_document():
    """Test deleting a document"""
    mock_db = AsyncMock(spec=AsyncSession)
    document_id = uuid4()

    # Mock the execute method to return a result with rowcount
    mock_execute_result = MagicMock()
    mock_execute_result.rowcount = 1  # Simulate 1 row deleted

    with patch.object(mock_db, 'execute', return_value=mock_execute_result):
        result = await crud.delete_document(mock_db, document_id)

        assert result == True  # Should return True when document was deleted