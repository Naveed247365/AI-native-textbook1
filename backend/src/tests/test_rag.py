"""
Unit tests for RAG pipeline functionality
"""
import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from typing import List, Dict, Any
from uuid import UUID, uuid4

from ..rag.pipeline import RAGPipeline, query_rag, process_document_for_rag, search_documents


@pytest.mark.asyncio
async def test_rag_pipeline_initialization():
    """Test RAGPipeline initialization"""
    pipeline = RAGPipeline()

    assert pipeline.vector_ops is not None


@pytest.mark.asyncio
async def test_query_rag_basic():
    """Test basic RAG query functionality"""
    # Mock the embedding result
    mock_embedding = [0.1, 0.2, 0.3] + [0.0] * (1536 - 3)  # 1536 dimensions

    # Mock the search results
    mock_search_results = [
        {
            "id": "point_id_1",
            "document_id": str(uuid4()),
            "score": 0.9,
            "payload": {"chunk_text": "This is relevant context.", "user_id": str(uuid4())}
        }
    ]

    # Mock the chat response
    mock_chat_response = "This is a test response based on the context."

    with patch('..embeddings.gemini_client.generate_embedding', return_value=mock_embedding):
        with patch('..qdrant.operations.VectorOperations.search_vectors', return_value=mock_search_results):
            with patch('..embeddings.gemini_client.generate_chat_response', return_value=mock_chat_response):
                user_id = uuid4()
                result = await query_rag(
                    query="Test query?",
                    user_id=user_id,
                    top_k=5
                )

                assert result is not None
                assert "response" in result
                assert "sources" in result
                assert "context_used" in result
                assert result["response"] == mock_chat_response


@pytest.mark.asyncio
async def test_query_rag_no_results():
    """Test RAG query when no results are found"""
    # Mock the embedding result
    mock_embedding = [0.4, 0.5, 0.6] + [0.0] * (1536 - 3)  # 1536 dimensions

    # Mock empty search results
    mock_search_results = []

    # Mock the chat response for when there's no context
    mock_chat_response = "I couldn't find relevant information to answer your question."

    with patch('..embeddings.gemini_client.generate_embedding', return_value=mock_embedding):
        with patch('..qdrant.operations.VectorOperations.search_vectors', return_value=mock_search_results):
            with patch('..embeddings.gemini_client.generate_chat_response', return_value=mock_chat_response):
                user_id = uuid4()
                result = await query_rag(
                    query="Test query with no results?",
                    user_id=user_id,
                    top_k=5
                )

                assert result is not None
                assert "response" in result
                assert result["response"] == mock_chat_response
                assert len(result["sources"]) == 0  # No sources since no results found


@pytest.mark.asyncio
async def test_query_rag_with_conversation_history():
    """Test RAG query with conversation history"""
    # Mock the embedding result
    mock_embedding = [0.7, 0.8, 0.9] + [0.0] * (1536 - 3)  # 1536 dimensions

    # Mock the search results
    mock_search_results = [
        {
            "id": "point_id_1",
            "document_id": str(uuid4()),
            "score": 0.85,
            "payload": {"chunk_text": "Previous conversation context is relevant here.", "user_id": str(uuid4())}
        }
    ]

    # Mock the chat response
    mock_chat_response = "Based on our previous conversation and the provided context, here is the answer."

    conversation_history = [
        {"role": "user", "content": "What did we talk about earlier?"},
        {"role": "assistant", "content": "We talked about AI and RAG systems."}
    ]

    with patch('..embeddings.gemini_client.generate_embedding', return_value=mock_embedding):
        with patch('..qdrant.operations.VectorOperations.search_vectors', return_value=mock_search_results):
            with patch('..embeddings.gemini_client.generate_chat_response', return_value=mock_chat_response):
                user_id = uuid4()
                result = await query_rag(
                    query="Can you elaborate on RAG?",
                    user_id=user_id,
                    top_k=3,
                    conversation_history=conversation_history
                )

                assert result is not None
                assert "response" in result
                assert "sources" in result
                assert result["response"] == mock_chat_response


@pytest.mark.asyncio
async def test_process_document_for_rag():
    """Test processing a document for RAG"""
    # Mock the embedding processor
    with patch('..embeddings.processor.process_document', return_value=True):
        document_id = uuid4()
        user_id = uuid4()

        result = await process_document_for_rag(
            document_id=document_id,
            user_id=user_id,
            content="This is a test document for RAG processing.",
            title="Test Document for RAG"
        )

        assert result is True  # Should return True on success


@pytest.mark.asyncio
async def test_search_documents():
    """Test document search functionality"""
    # Mock the embedding result
    mock_embedding = [0.2, 0.3, 0.4] + [0.0] * (1536 - 3)  # 1536 dimensions

    # Mock the search results
    mock_search_results = [
        {
            "id": "point_id_1",
            "document_id": str(uuid4()),
            "score": 0.92,
            "payload": {"chunk_text": "This is relevant information about the search topic.", "user_id": str(uuid4())}
        },
        {
            "id": "point_id_2",
            "document_id": str(uuid4()),
            "score": 0.87,
            "payload": {"chunk_text": "More context related to the search query.", "user_id": str(uuid4())}
        }
    ]

    with patch('..embeddings.gemini_client.generate_embedding', return_value=mock_embedding):
        with patch('..qdrant.operations.VectorOperations.search_vectors', return_value=mock_search_results):
            user_id = uuid4()
            result = await search_documents(
                query="Test search query",
                user_id=user_id,
                top_k=5
            )

            assert result is not None
            assert len(result) == 2  # Two results returned
            assert all("payload" in r for r in result)  # All results have payloads


@pytest.mark.asyncio
async def test_rag_pipeline_query_method():
    """Test the query method of RAGPipeline class"""
    pipeline = RAGPipeline()

    # Mock the embedding result
    mock_embedding = [0.5, 0.6, 0.7] + [0.0] * (1536 - 3)  # 1536 dimensions

    # Mock the search results
    mock_search_results = [
        {
            "id": "point_id_1",
            "document_id": str(uuid4()),
            "score": 0.95,
            "payload": {"chunk_text": "Specific context for this query.", "user_id": str(uuid4())}
        }
    ]

    # Mock the chat response
    mock_chat_response = "Based on the specific context, here is the detailed answer."

    with patch('..embeddings.gemini_client.generate_embedding', return_value=mock_embedding):
        with patch('..qdrant.operations.VectorOperations.search_vectors', return_value=mock_search_results):
            with patch('..embeddings.gemini_client.generate_chat_response', return_value=mock_chat_response):
                user_id = uuid4()
                result = await pipeline.query_rag(
                    query="Specific query?",
                    user_id=user_id,
                    top_k=3
                )

                assert result is not None
                assert result["response"] == mock_chat_response


@pytest.mark.asyncio
async def test_process_document_method():
    """Test the process_document method of RAGPipeline class"""
    pipeline = RAGPipeline()

    # Mock the embedding processor
    with patch('..embeddings.processor.process_document', return_value=True):
        document_id = uuid4()
        user_id = uuid4()

        result = await pipeline.process_document_for_rag(
            document_id=document_id,
            user_id=user_id,
            content="Content for the document processing test.",
            title="Test Document Processing"
        )

        assert result is True  # Should return True on success


@pytest.mark.asyncio
async def test_delete_user_documents():
    """Test deleting all documents for a user"""
    pipeline = RAGPipeline()

    # Mock the vector operations
    with patch('..qdrant.operations.VectorOperations.delete_vectors_by_user_id', return_value=True):
        user_id = uuid4()
        result = await pipeline.delete_user_documents(user_id)

        assert result is True  # Should return True on success


@pytest.mark.asyncio
async def test_rag_error_handling():
    """Test RAG pipeline error handling"""
    # Mock to simulate an error in embedding generation
    with patch('..embeddings.gemini_client.generate_embedding', return_value=None):
        user_id = uuid4()
        result = await query_rag(
            query="Test query that will fail embedding",
            user_id=user_id
        )

        assert result is None  # Should return None on failure


@pytest.mark.asyncio
async def test_rag_pipeline_search_method():
    """Test the search_documents method of RAGPipeline class"""
    pipeline = RAGPipeline()

    # Mock the embedding result
    mock_embedding = [0.8, 0.9, 1.0] + [0.0] * (1536 - 3)  # 1536 dimensions

    # Mock the search results
    mock_search_results = [
        {
            "id": "point_id_1",
            "document_id": str(uuid4()),
            "score": 0.90,
            "payload": {"chunk_text": "Search result content.", "user_id": str(uuid4())}
        }
    ]

    with patch('..embeddings.gemini_client.generate_embedding', return_value=mock_embedding):
        with patch('..qdrant.operations.VectorOperations.search_vectors', return_value=mock_search_results):
            user_id = uuid4()
            result = await pipeline.search_documents(
                query="Test search",
                user_id=user_id,
                top_k=5
            )

            assert result is not None
            assert len(result) == 1  # One result returned