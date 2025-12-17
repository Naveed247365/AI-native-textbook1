"""
Embedding processor for the AI Backend with RAG + Authentication
Implements text preprocessing, caching, and document chunking for embeddings
"""
import hashlib
import asyncio
from typing import List, Optional, Tuple, Dict
import logging
from uuid import UUID

from ..config.settings import settings
from .gemini_client import generate_embedding, generate_embeddings_batch
from ..qdrant.operations import get_vector_operations
from ..db import crud
from ..config.database import get_db_session

logger = logging.getLogger(__name__)

# Maximum characters per chunk (Gemini has token limits)
MAX_CHUNK_SIZE = 2000
OVERLAP_SIZE = 200  # Overlap between chunks to maintain context


class EmbeddingProcessor:
    """
    Processor class to handle embedding workflows including preprocessing,
    caching, and document chunking
    """

    def __init__(self):
        self.vector_ops = get_vector_operations()
        # Simple in-memory cache (in production, use Redis or similar)
        self.cache: Dict[str, List[float]] = {}

    def _generate_content_hash(self, content: str) -> str:
        """
        Generate a hash for content to use for caching and deduplication
        """
        return hashlib.sha256(content.encode('utf-8')).hexdigest()

    def _preprocess_text(self, text: str) -> str:
        """
        Preprocess text by cleaning and normalizing
        """
        if not text or not isinstance(text, str):
            raise ValueError("Input text must be a non-empty string")

        # Remove extra whitespace
        text = ' '.join(text.split())

        # Validate text length
        if len(text) > 1000000:  # 1M characters max
            logger.warning(f"Text is very long ({len(text)} chars), consider pre-processing")

        return text.strip()

    def _chunk_text(self, text: str, chunk_size: int = MAX_CHUNK_SIZE, overlap: int = OVERLAP_SIZE) -> List[str]:
        """
        Split text into overlapping chunks to maintain context
        """
        if len(text) <= chunk_size:
            return [text]

        chunks = []
        start = 0

        while start < len(text):
            end = start + chunk_size

            # If we're near the end, include the rest
            if end > len(text):
                end = len(text)
                start = max(0, end - chunk_size)

            chunk = text[start:end]

            # If this isn't the last chunk, try to break at sentence boundary
            if end < len(text):
                # Look for sentence endings to break at
                sentence_end = max(
                    chunk.rfind('.'),
                    chunk.rfind('!'),
                    chunk.rfind('?'),
                    chunk.rfind('\n')
                )

                if sentence_end > chunk_size // 2:  # Only if it's not too early
                    end = start + sentence_end + 1
                    chunk = text[start:end]

            chunks.append(chunk)
            start = end - overlap

        return chunks

    async def _get_from_cache(self, content_hash: str) -> Optional[List[float]]:
        """
        Get embedding from cache if available
        """
        return self.cache.get(content_hash)

    async def _save_to_cache(self, content_hash: str, embedding: List[float]):
        """
        Save embedding to cache
        """
        self.cache[content_hash] = embedding

    async def process_single_text(self, text: str, user_id: UUID) -> Optional[List[float]]:
        """
        Process a single text for embedding with caching
        """
        try:
            # Preprocess the text
            processed_text = self._preprocess_text(text)

            if not processed_text:
                logger.warning("Text preprocessing resulted in empty string")
                return None

            # Generate content hash for caching
            content_hash = self._generate_content_hash(processed_text)

            # Check cache first
            cached_embedding = await self._get_from_cache(content_hash)
            if cached_embedding:
                logger.info(f"Found embedding in cache for text of length {len(processed_text)}")
                return cached_embedding

            # Generate embedding using Gemini
            embedding = await generate_embedding(processed_text)
            if embedding is None:
                logger.error(f"Failed to generate embedding for text of length {len(processed_text)}")
                return None

            # Save to cache
            await self._save_to_cache(content_hash, embedding)

            logger.info(f"Successfully processed embedding for text of length {len(processed_text)}")
            return embedding

        except Exception as e:
            logger.error(f"Error processing single text: {e}")
            return None

    async def process_document(
        self,
        document_id: UUID,
        user_id: UUID,
        content: str,
        title: Optional[str] = None,
        metadata: Optional[Dict] = None
    ) -> bool:
        """
        Process a document for embedding, including chunking and storage
        """
        try:
            # Preprocess the content
            processed_content = self._preprocess_text(content)

            if not processed_content:
                logger.warning("Document content preprocessing resulted in empty string")
                return False

            # Chunk the document if it's large
            if len(processed_content) > MAX_CHUNK_SIZE:
                chunks = self._chunk_text(processed_content)
                logger.info(f"Document chunked into {len(chunks)} parts")
            else:
                chunks = [processed_content]

            # Process each chunk
            all_embeddings = []
            chunk_payloads = []

            for i, chunk in enumerate(chunks):
                # Generate content hash for caching
                content_hash = self._generate_content_hash(chunk)

                # Check cache first
                embedding = await self._get_from_cache(content_hash)
                if embedding is None:
                    # Generate embedding using Gemini
                    embedding = await generate_embedding(chunk)
                    if embedding is None:
                        logger.error(f"Failed to generate embedding for chunk {i}")
                        continue

                    # Save to cache
                    await self._save_to_cache(content_hash, embedding)

                all_embeddings.append(embedding)

                # Create payload for this chunk
                chunk_payload = {
                    "chunk_index": i,
                    "chunk_text": chunk[:100] + "..." if len(chunk) > 100 else chunk,  # Store first 100 chars as reference
                    "document_id": str(document_id),
                    "user_id": str(user_id),
                    "title": title or "Untitled Document",
                    "total_chunks": len(chunks)
                }

                if metadata:
                    chunk_payload.update(metadata)

                chunk_payloads.append(chunk_payload)

            # Store embeddings in Qdrant
            if all_embeddings:
                success = await self.vector_ops.batch_upsert_vectors(
                    user_id=user_id,
                    document_id=document_id,
                    embeddings_list=all_embeddings,
                    payloads_list=chunk_payloads
                )

                if success:
                    logger.info(f"Successfully stored {len(all_embeddings)} embeddings for document {document_id}")
                    return True
                else:
                    logger.error(f"Failed to store embeddings in Qdrant for document {document_id}")
                    return False
            else:
                logger.warning("No embeddings were generated for the document")
                return False

        except Exception as e:
            logger.error(f"Error processing document {document_id}: {e}")
            return False

    async def process_texts_batch(
        self,
        texts: List[str],
        user_id: UUID
    ) -> Optional[List[List[float]]]:
        """
        Process a batch of texts for embedding with caching
        """
        try:
            embeddings = []

            for text in texts:
                embedding = await self.process_single_text(text, user_id)
                if embedding is None:
                    logger.error(f"Failed to process text: {text[:50]}...")
                    return None
                embeddings.append(embedding)

            logger.info(f"Successfully processed batch of {len(texts)} texts")
            return embeddings

        except Exception as e:
            logger.error(f"Error processing text batch: {e}")
            return None

    async def invalidate_cache_for_document(self, document_id: UUID):
        """
        Remove cached embeddings associated with a document
        In a real implementation with Redis, this would be more sophisticated
        """
        # In our simple in-memory cache, we can't easily identify which cache entries
        # belong to a specific document, so we'd need to implement a more sophisticated
        # cache structure. For now, we'll just log the action.
        logger.info(f"Cache invalidation requested for document {document_id} (not implemented in simple cache)")


# Global instance of EmbeddingProcessor
embedding_processor = EmbeddingProcessor()


def get_embedding_processor() -> EmbeddingProcessor:
    """Get the embedding processor instance"""
    return embedding_processor


async def process_single_text(text: str, user_id: UUID) -> Optional[List[float]]:
    """
    Process a single text for embedding with caching
    """
    return await embedding_processor.process_single_text(text, user_id)


async def process_document(
    document_id: UUID,
    user_id: UUID,
    content: str,
    title: Optional[str] = None,
    metadata: Optional[Dict] = None
) -> bool:
    """
    Process a document for embedding, including chunking and storage
    """
    return await embedding_processor.process_document(document_id, user_id, content, title, metadata)


async def process_texts_batch(
    texts: List[str],
    user_id: UUID
) -> Optional[List[List[float]]]:
    """
    Process a batch of texts for embedding with caching
    """
    return await embedding_processor.process_texts_batch(texts, user_id)