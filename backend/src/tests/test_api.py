"""
Unit tests for API endpoints
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import UUID, uuid4
from datetime import datetime

from ..main import app
from ..auth.auth import TokenData
from ..config.database import get_db_session
from ..db import crud


@pytest.fixture
def client():
    """Test client fixture"""
    return TestClient(app)


@pytest.mark.asyncio
async def test_health_endpoint(client):
    """Test health endpoint"""
    # Mock the service health checks
    with patch('..routes.health.test_database_health', return_value=True):
        with patch('..routes.health.test_qdrant_health', return_value=True):
            with patch('..routes.health.test_gemini_health', return_value=True):
                response = client.get("/health/")

                assert response.status_code == 200
                data = response.json()

                assert "status" in data
                assert "services" in data
                assert data["status"] == "healthy"


@pytest.mark.asyncio
async def test_auth_signup_endpoint(client):
    """Test auth signup endpoint"""
    # Mock the database operations
    mock_db = AsyncMock()
    mock_user = MagicMock()
    mock_user.id = uuid4()
    mock_user.email = "test@example.com"
    mock_user.full_name = "Test User"
    mock_user.is_active = True
    mock_user.created_at = datetime.utcnow()

    with patch('..config.database.get_db_session', return_value=mock_db):
        with patch('..db.crud.get_user_by_email', return_value=None):  # User doesn't exist yet
            with patch('..db.crud.create_user', return_value=mock_user):
                with patch('..auth.auth.create_user_token', return_value="fake_jwt_token"):
                    response = client.post("/auth/signup", json={
                        "email": "test@example.com",
                        "password": "testpassword",
                        "full_name": "Test User"
                    })

                    assert response.status_code == 200
                    data = response.json()

                    assert "access_token" in data
                    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_auth_login_endpoint(client):
    """Test auth login endpoint"""
    # Mock the database operations
    mock_db = AsyncMock()
    mock_user = MagicMock()
    mock_user.id = uuid4()
    mock_user.email = "test@example.com"
    mock_user.hashed_password = "hashed_password"
    mock_user.is_active = True

    with patch('..config.database.get_db_session', return_value=mock_db):
        with patch('..db.crud.get_user_by_email', return_value=mock_user):
            with patch('..auth.auth.verify_password', return_value=True):
                with patch('..auth.auth.create_user_token', return_value="fake_jwt_token"):
                    response = client.post("/auth/login", json={
                        "email": "test@example.com",
                        "password": "testpassword"
                    })

                    assert response.status_code == 200
                    data = response.json()

                    assert "access_token" in data
                    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_auth_me_endpoint(client):
    """Test auth me endpoint"""
    # Mock the token decoding
    mock_token_data = TokenData(username="test@example.com", user_id=str(uuid4()))

    # Mock the database operations
    mock_db = AsyncMock()
    mock_user = MagicMock()
    mock_user.id = uuid4()
    mock_user.email = "test@example.com"
    mock_user.full_name = "Test User"
    mock_user.is_active = True
    mock_user.created_at = datetime.utcnow()

    with patch('..config.database.get_db_session', return_value=mock_db):
        with patch('..auth.auth.get_current_user', return_value=mock_token_data):
            with patch('..db.crud.get_user_by_id', return_value=mock_user):
                response = client.get("/auth/me", headers={
                    "Authorization": "Bearer fake_jwt_token"
                })

                assert response.status_code == 200
                data = response.json()

                assert "id" in data
                assert data["email"] == "test@example.com"


@pytest.mark.asyncio
async def test_save_document_endpoint(client):
    """Test save document endpoint"""
    # Mock the token decoding
    mock_token_data = TokenData(username="test@example.com", user_id=str(uuid4()))

    # Mock the database operations
    mock_db = AsyncMock()
    mock_document = MagicMock()
    mock_document.id = uuid4()

    with patch('..config.database.get_db_session', return_value=mock_db):
        with patch('..auth.auth.get_current_user', return_value=mock_token_data):
            with patch('..db.crud.get_document_by_hash', return_value=None):  # Document doesn't exist
                with patch('..db.crud.create_document', return_value=mock_document):
                    with patch('..rag.pipeline.process_document_for_rag', return_value=True):
                        response = client.post("/documents/", json={
                            "title": "Test Document",
                            "content": "This is the content of the test document."
                        }, headers={
                            "Authorization": "Bearer fake_jwt_token"
                        })

                        assert response.status_code == 200
                        data = response.json()

                        assert "document_id" in data
                        assert data["success"] is True


@pytest.mark.asyncio
async def test_search_endpoint(client):
    """Test search endpoint"""
    # Mock the token decoding
    mock_token_data = TokenData(username="test@example.com", user_id=str(uuid4()))

    # Mock the search results
    mock_search_results = [
        {
            "id": "point_id_1",
            "document_id": str(uuid4()),
            "score": 0.95,
            "payload": {"chunk_text": "This is relevant context for the search.", "user_id": str(uuid4())}
        }
    ]

    with patch('..auth.auth.get_current_user', return_value=mock_token_data):
        with patch('..rag.pipeline.search_documents', return_value=mock_search_results):
            response = client.post("/search/", json={
                "query": "Test search query",
                "top_k": 5
            }, headers={
                "Authorization": "Bearer fake_jwt_token"
            })

            assert response.status_code == 200
            data = response.json()

            assert "results" in data
            assert "query" in data
            assert len(data["results"]) >= 0  # May have 0 or more results


@pytest.mark.asyncio
async def test_chat_endpoint(client):
    """Test chat endpoint"""
    # Mock the token decoding
    mock_token_data = TokenData(username="test@example.com", user_id=str(uuid4()))

    # Mock the RAG result
    mock_rag_result = {
        "response": "This is a test response from the AI model.",
        "sources": [{"chunk_text": "Relevant context"}],
        "context_used": [{"chunk_text": "Relevant context"}],
        "query_embedding": [0.1, 0.2, 0.3] + [0.0] * (1536 - 3)
    }

    with patch('..auth.auth.get_current_user', return_value=mock_token_data):
        with patch('..rag.pipeline.query_rag', return_value=mock_rag_result):
            response = client.post("/search/chat", json={
                "query": "Test chat query?",
                "top_k": 5
            }, headers={
                "Authorization": "Bearer fake_jwt_token"
            })

            assert response.status_code == 200
            data = response.json()

            assert "response" in data
            assert "sources" in data
            assert data["response"] == "This is a test response from the AI model."


@pytest.mark.asyncio
async def test_get_chat_history_endpoint(client):
    """Test get chat history endpoint"""
    # Mock the token decoding
    mock_token_data = TokenData(username="test@example.com", user_id=str(uuid4()))

    # Mock the database operations
    mock_db = AsyncMock()
    mock_chat_history = MagicMock()
    mock_chat_history.id = uuid4()
    mock_chat_history.query = "Test query?"
    mock_chat_history.response = "Test response"
    mock_chat_history.created_at = datetime.utcnow()
    mock_chat_history.updated_at = datetime.utcnow()

    with patch('..config.database.get_db_session', return_value=mock_db):
        with patch('..auth.auth.get_current_user', return_value=mock_token_data):
            with patch('..db.crud.get_chat_histories_by_user', return_value=[mock_chat_history]):
                with patch('..db.crud.get_user_chat_history_count', return_value=1):
                    response = client.get("/history/?page=1&limit=20", headers={
                        "Authorization": "Bearer fake_jwt_token"
                    })

                    assert response.status_code == 200
                    data = response.json()

                    assert "history" in data
                    assert "total" in data
                    assert len(data["history"]) >= 0


@pytest.mark.asyncio
async def test_unauthorized_access(client):
    """Test unauthorized access to protected endpoints"""
    response = client.get("/auth/me")  # No authorization header

    # Should return 403 or 401 for unauthorized access
    assert response.status_code in [401, 403]


@pytest.mark.asyncio
async def test_invalid_token_access(client):
    """Test access with invalid token"""
    with patch('..auth.auth.get_current_user', side_effect=Exception("Invalid token")):
        response = client.get("/auth/me", headers={
            "Authorization": "Bearer invalid_token"
        })

        # Should return 401 for invalid token
        assert response.status_code == 401


@pytest.mark.asyncio
async def test_detailed_health_endpoint(client):
    """Test detailed health endpoint"""
    # Mock the service health checks
    with patch('..routes.health.test_database_health', return_value=True):
        with patch('..routes.health.test_qdrant_health', return_value=True):
            with patch('..routes.health.test_gemini_health', return_value=True):
                response = client.get("/health/detailed")

                assert response.status_code == 200
                data = response.json()

                assert "status" in data
                assert "services" in data
                assert "system" in data
                assert data["status"] == "healthy"


@pytest.mark.asyncio
async def test_get_specific_conversation(client):
    """Test getting a specific conversation"""
    # Mock the token decoding
    mock_token_data = TokenData(username="test@example.com", user_id=str(uuid4()))

    # Mock the database operations
    mock_db = AsyncMock()
    mock_chat_history = MagicMock()
    mock_chat_history.id = uuid4()
    mock_chat_history.query = "Test query?"
    mock_chat_history.response = "Test response"
    mock_chat_history.created_at = datetime.utcnow()
    mock_chat_history.updated_at = datetime.utcnow()
    mock_chat_history.user_id = mock_token_data.user_id

    conversation_id = str(mock_chat_history.id)

    with patch('..config.database.get_db_session', return_value=mock_db):
        with patch('..auth.auth.get_current_user', return_value=mock_token_data):
            with patch('..db.crud.get_chat_history_by_id', return_value=mock_chat_history):
                response = client.get(f"/history/{conversation_id}", headers={
                    "Authorization": "Bearer fake_jwt_token"
                })

                assert response.status_code == 200
                data = response.json()

                assert "id" in data
                assert data["query"] == "Test query?"


@pytest.mark.asyncio
async def test_get_document_endpoint(client):
    """Test getting a specific document"""
    # Mock the token decoding
    mock_token_data = TokenData(username="test@example.com", user_id=str(uuid4()))

    # Mock the database operations
    mock_db = AsyncMock()
    mock_document = MagicMock()
    mock_document.id = uuid4()
    mock_document.title = "Test Document"
    mock_document.content = "Test content"
    mock_document.created_at = datetime.utcnow()
    mock_document.updated_at = datetime.utcnow()
    mock_document.user_id = mock_token_data.user_id

    document_id = str(mock_document.id)

    with patch('..config.database.get_db_session', return_value=mock_db):
        with patch('..auth.auth.get_current_user', return_value=mock_token_data):
            with patch('..db.crud.get_document_by_id', return_value=mock_document):
                response = client.get(f"/documents/{document_id}", headers={
                    "Authorization": "Bearer fake_jwt_token"
                })

                assert response.status_code == 200
                data = response.json()

                assert "id" in data
                assert data["title"] == "Test Document"