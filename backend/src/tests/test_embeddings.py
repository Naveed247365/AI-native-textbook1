"""
Unit tests for embedding functionality
"""
import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from typing import List

from ..embeddings.gemini_client import GeminiClient, generate_embedding, generate_embeddings_batch
from ..embeddings.processor import EmbeddingProcessor, process_single_text, process_document


@pytest.mark.asyncio
async def test_generate_embedding():
    """Test generating a single embedding"""
    # Mock the Gemini API response
    mock_embedding_result = {
        'embedding': [0.1, 0.2, 0.3] + [0.0] * (1536 - 3)  # 1536 dimensions
    }

    with patch('google.generativeai.embed_content', return_value=mock_embedding_result):
        text = "Test text for embedding"
        result = await generate_embedding(text)

        assert result is not None
        assert len(result) == 1536  # Expected dimensions for text-embedding-004
        assert isinstance(result, list)
        assert all(isinstance(val, float) for val in result)


@pytest.mark.asyncio
async def test_generate_embeddings_batch():
    """Test generating embeddings for a batch of texts"""
    # Mock the Gemini API response
    mock_embedding_result = {
        'embedding': [0.1, 0.2, 0.3] + [0.0] * (1536 - 3)  # 1536 dimensions
    }

    with patch('google.generativeai.embed_content', return_value=mock_embedding_result):
        texts = ["Test text 1", "Test text 2", "Test text 3"]
        result = await generate_embeddings_batch(texts)

        assert result is not None
        assert len(result) == 3  # Same number as input texts
        assert all(len(embedding) == 1536 for embedding in result)  # All have correct dimensions
        assert all(isinstance(embedding, list) for embedding in result)


@pytest.mark.asyncio
async def test_generate_embedding_with_retry():
    """Test embedding generation with retry logic"""
    # Mock the Gemini API to fail initially, then succeed
    mock_embedding_result = {
        'embedding': [0.5] * 1536  # 1536 dimensions
    }

    # Mock to fail once, then succeed
    mock_embed_content = MagicMock(side_effect=[
        Exception("API Error"),
        mock_embedding_result
    ])

    with patch('google.generativeai.embed_content', mock_embed_content):
        text = "Test text for embedding with retry"
        result = await generate_embedding(text)

        assert result is not None
        assert len(result) == 1536  # Correct dimensions
        assert mock_embed_content.call_count == 2  # Called twice (once failed, once succeeded)


@pytest.mark.asyncio
async def test_generate_embedding_failure():
    """Test embedding generation failure handling"""
    # Mock the Gemini API to always fail
    with patch('google.generativeai.embed_content', side_effect=Exception("API Error")):
        text = "Test text for embedding failure"
        result = await generate_embedding(text)

        assert result is None  # Should return None on failure


@pytest.mark.asyncio
async def test_process_single_text():
    """Test processing a single text for embedding"""
    # Mock the embedding result
    mock_embedding = [0.1, 0.2, 0.3] + [0.0] * (1536 - 3)  # 1536 dimensions

    with patch('..embeddings.gemini_client.generate_embedding', return_value=mock_embedding):
        from uuid import uuid4
        user_id = uuid4()
        result = await process_single_text("Test text for processing", user_id)

        assert result == mock_embedding  # Should return the embedding
        assert len(result) == 1536  # Correct dimensions


@pytest.mark.asyncio
async def test_process_single_text_with_caching():
    """Test processing a single text with caching"""
    # Create an EmbeddingProcessor instance
    processor = EmbeddingProcessor()

    # Mock the embedding result
    mock_embedding = [0.4, 0.5, 0.6] + [0.0] * (1536 - 3)  # 1536 dimensions

    with patch('..embeddings.gemini_client.generate_embedding', return_value=mock_embedding):
        from uuid import uuid4
        user_id = uuid4()

        # Process the same text twice
        result1 = await processor.process_single_text("Test text for caching", user_id)
        result2 = await processor.process_single_text("Test text for caching", user_id)  # Should use cache

        # Both results should be the same
        assert result1 == result2
        assert result1 == mock_embedding


@pytest.mark.asyncio
async def test_process_document():
    """Test processing a document for embedding"""
    # Mock the embedding result
    mock_embedding = [0.7, 0.8, 0.9] + [0.0] * (1536 - 3)  # 1536 dimensions

    with patch('..embeddings.gemini_client.generate_embedding', return_value=mock_embedding):
        from uuid import uuid4
        document_id = uuid4()
        user_id = uuid4()

        # Mock the vector operations
        with patch('..qdrant.operations.VectorOperations.batch_upsert_vectors', return_value=True):
            result = await process_document(
                document_id=document_id,
                user_id=user_id,
                content="This is a test document content for processing.",
                title="Test Document"
            )

            assert result == True  # Should return True on success


@pytest.mark.asyncio
async def test_process_large_document_chunking():
    """Test processing a large document that requires chunking"""
    # Create a large text that exceeds the chunk size
    large_text = "This is a test sentence. " * 1000  # Much larger than MAX_CHUNK_SIZE

    # Mock the embedding result
    mock_embedding = [0.1] * 1536  # 1536 dimensions

    with patch('..embeddings.gemini_client.generate_embedding', return_value=mock_embedding):
        from uuid import uuid4
        document_id = uuid4()
        user_id = uuid4()

        # Mock the vector operations
        with patch('..qdrant.operations.VectorOperations.batch_upsert_vectors', return_value=True):
            result = await process_document(
                document_id=document_id,
                user_id=user_id,
                content=large_text,
                title="Large Test Document"
            )

            assert result == True  # Should return True on success


@pytest.mark.asyncio
async def test_embedding_processor_initialization():
    """Test EmbeddingProcessor initialization"""
    processor = EmbeddingProcessor()

    assert processor.vector_ops is not None
    assert isinstance(processor.cache, dict)


@pytest.mark.asyncio
async def test_preprocess_text():
    """Test text preprocessing functionality"""
    processor = EmbeddingProcessor()

    # Test normal text
    result = processor._preprocess_text("  This is a test text with extra spaces.  ")
    assert result == "This is a test text with extra spaces."

    # Test empty text (should raise an error)
    try:
        processor._preprocess_text("")
        assert False, "Should have raised an error for empty text"
    except ValueError:
        pass  # Expected

    # Test non-string input (should raise an error)
    try:
        processor._preprocess_text(None)
        assert False, "Should have raised an error for None input"
    except ValueError:
        pass  # Expected


@pytest.mark.asyncio
async def test_chunk_text():
    """Test text chunking functionality"""
    processor = EmbeddingProcessor()

    # Test text that needs to be chunked
    long_text = "This is a sentence. " * 100  # Create a long text
    chunks = processor._chunk_text(long_text, chunk_size=100, overlap=10)

    assert len(chunks) > 1  # Should be split into multiple chunks
    assert all(isinstance(chunk, str) for chunk in chunks)

    # Test short text (should not be chunked)
    short_text = "Short text."
    chunks = processor._chunk_text(short_text, chunk_size=100, overlap=10)

    assert len(chunks) == 1
    assert chunks[0] == short_text


@pytest.mark.asyncio
async def test_generate_chat_response():
    """Test generating chat responses with context"""
    from ..embeddings.gemini_client import generate_chat_response

    # Mock the chat model response
    mock_response = MagicMock()
    mock_response.text = "This is a test response from the model."

    mock_chat_model = MagicMock()
    mock_chat_model.generate_content_async = AsyncMock(return_value=mock_response)

    with patch('..embeddings.gemini_client.genai.GenerativeModel', return_value=mock_chat_model):
        result = await generate_chat_response(
            query="Test query?",
            context=[{"payload": {"chunk_text": "This is relevant context."}}]
        )

        assert result == "This is a test response from the model."


@pytest.mark.asyncio
async def test_moderate_content():
    """Test content moderation functionality"""
    from ..embeddings.gemini_client import moderate_content

    # Mock the chat model response
    mock_response = MagicMock()
    mock_response.text = "Content is safe"

    mock_chat_model = MagicMock()
    mock_chat_model.generate_content_async = AsyncMock(return_value=mock_response)

    with patch('..embeddings.gemini_client.genai.GenerativeModel', return_value=mock_chat_model):
        result = await moderate_content("Test content for moderation")

        assert result is not None
        assert "text" in result