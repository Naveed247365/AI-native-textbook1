"""
RAG Pipeline for the AI Backend with RAG + Authentication
Implements the complete Retrieval-Augmented Generation workflow
"""
from typing import List, Optional, Dict, Any
import logging
from uuid import UUID

from ..embeddings.gemini_client import generate_embedding, generate_chat_response
from ..qdrant.operations import get_vector_operations
from ..config.settings import settings

logger = logging.getLogger(__name__)


class RAGPipeline:
    """
    Main RAG pipeline class that orchestrates the complete workflow:
    1. Query embedding
    2. Vector search with user isolation
    3. Context retrieval and formatting
    4. Response generation using Gemini
    """

    def __init__(self):
        self.vector_ops = get_vector_operations()

    async def query_rag(
        self,
        query: str,
        user_id: UUID,
        top_k: int = 5,
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Execute the complete RAG pipeline
        """
        try:
            logger.info(f"Starting RAG query for user {user_id}: {query[:50]}...")

            # Step 1: Generate embedding for the query
            query_embedding = await generate_embedding(query)
            if not query_embedding:
                logger.error("Failed to generate query embedding")
                return None

            # Step 2: Search for relevant documents in Qdrant with user_id filtering
            search_results = await self.vector_ops.search_vectors(
                query_embedding=query_embedding,
                user_id=user_id,  # Ensure user isolation
                top_k=top_k
            )

            if not search_results:
                logger.info(f"No relevant documents found for query from user {user_id}")
                # Even if no results found, we can still try to generate a response
                # using the chat model without context
                response = await generate_chat_response(
                    query=query,
                    context=None,
                    conversation_history=conversation_history
                )
                return {
                    "response": response,
                    "sources": [],
                    "query_embedding": query_embedding,
                    "context_used": []
                }

            logger.info(f"Found {len(search_results)} relevant results for user {user_id}")

            # Step 3: Format context from search results
            context = []
            for result in search_results:
                context.append({
                    "id": result["id"],
                    "document_id": result["document_id"],
                    "score": result["score"],
                    "payload": result["payload"]
                })

            # Step 4: Generate response using Gemini with context
            response = await generate_chat_response(
                query=query,
                context=context,
                conversation_history=conversation_history
            )

            if not response:
                logger.error("Failed to generate response from Gemini")
                return None

            logger.info(f"RAG query completed successfully for user {user_id}")

            # Return response with metadata
            return {
                "response": response,
                "sources": [c["payload"] for c in context],  # Source documents
                "query_embedding": query_embedding,
                "context_used": [c["payload"] for c in context]  # Context used for response
            }

        except Exception as e:
            logger.error(f"Error in RAG pipeline: {e}")
            return None

    async def process_document_for_rag(
        self,
        document_id: UUID,
        user_id: UUID,
        content: str,
        title: Optional[str] = None,
        metadata: Optional[Dict] = None
    ) -> bool:
        """
        Process a document for RAG by generating embeddings and storing in Qdrant
        """
        try:
            logger.info(f"Processing document {document_id} for user {user_id} for RAG")

            # Import the embedding processor here to avoid circular imports
            from ..embeddings.processor import process_document as process_doc
            success = await process_doc(document_id, user_id, content, title, metadata)

            if success:
                logger.info(f"Document {document_id} processed successfully for RAG")
                return True
            else:
                logger.error(f"Failed to process document {document_id} for RAG")
                return False

        except Exception as e:
            logger.error(f"Error processing document for RAG: {e}")
            return False

    async def search_documents(
        self,
        query: str,
        user_id: UUID,
        top_k: int = 5
    ) -> Optional[List[Dict[str, Any]]]:
        """
        Search for documents relevant to the query with user isolation
        """
        try:
            # Generate embedding for the query
            query_embedding = await generate_embedding(query)
            if not query_embedding:
                logger.error("Failed to generate query embedding for search")
                return None

            # Search in Qdrant with user_id filtering
            search_results = await self.vector_ops.search_vectors(
                query_embedding=query_embedding,
                user_id=user_id,  # Ensure user isolation
                top_k=top_k
            )

            logger.info(f"Search completed for user {user_id}, found {len(search_results)} results")

            return search_results

        except Exception as e:
            logger.error(f"Error in document search: {e}")
            return None

    async def delete_vectors_by_user_id(self, user_id: UUID) -> bool:
        """
        Delete all vectors for a user (helper function for user deletion)
        This function needs to be added to vector operations as well
        """
        try:
            success = await self.vector_ops.delete_vectors_by_user_id(user_id)
            return success
        except Exception as e:
            logger.error(f"Error deleting vectors for user {user_id}: {e}")
            return False

    async def delete_user_documents(self, user_id: UUID) -> bool:
        """
        Delete all documents for a user (used when user is deleted)
        """
        try:
            success = await self.vector_ops.delete_vectors_by_user_id(user_id)
            if success:
                logger.info(f"Successfully deleted all documents for user {user_id}")
            else:
                logger.error(f"Failed to delete documents for user {user_id}")
            return success

        except Exception as e:
            logger.error(f"Error deleting user documents: {e}")
            return False


# Global instance of RAGPipeline
rag_pipeline = RAGPipeline()


def get_rag_pipeline() -> RAGPipeline:
    """Get the RAG pipeline instance"""
    return rag_pipeline


async def query_rag(
    query: str,
    user_id: UUID,
    top_k: int = 5,
    conversation_history: Optional[List[Dict[str, str]]] = None
) -> Optional[Dict[str, Any]]:
    """
    Execute the complete RAG pipeline
    """
    return await rag_pipeline.query_rag(query, user_id, top_k, conversation_history)


async def process_document_for_rag(
    document_id: UUID,
    user_id: UUID,
    content: str,
    title: Optional[str] = None,
    metadata: Optional[Dict] = None
) -> bool:
    """
    Process a document for RAG by generating embeddings and storing in Qdrant
    """
    return await rag_pipeline.process_document_for_rag(document_id, user_id, content, title, metadata)


async def search_documents(
    query: str,
    user_id: UUID,
    top_k: int = 5
) -> Optional[List[Dict[str, Any]]]:
    """
    Search for documents relevant to the query with user isolation
    """
    return await rag_pipeline.search_documents(query, user_id, top_k)