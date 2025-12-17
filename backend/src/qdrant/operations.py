"""
Vector operations for the AI Backend with RAG + Authentication
Implements upsert, search, and management functions for vector storage
"""
from typing import List, Optional, Dict, Any
from uuid import UUID
import logging
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.exceptions import UnexpectedResponse
from qdrant_client.conversions import common_types
from qdrant_client.local.qdrant_local import QdrantLocal
import uuid

from ..config.settings import settings
from .client import get_qdrant_client, VECTOR_DIMENSIONS

logger = logging.getLogger(__name__)


class VectorOperations:
    """
    Service class to manage vector operations in Qdrant
    """

    def __init__(self):
        self.client: QdrantClient = get_qdrant_client()
        self.collection_name = "documents"

    def upsert_vectors(
        self,
        user_id: UUID,
        document_id: UUID,
        embeddings: List[float],
        payload: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Upsert vectors with user_id metadata
        """
        try:
            # Validate embedding dimensions
            if len(embeddings) != VECTOR_DIMENSIONS:
                logger.error(f"Embedding vector has wrong dimensions: {len(embeddings)}, expected: {VECTOR_DIMENSIONS}")
                return False

            # Prepare payload with user_id and document_id metadata
            full_payload = {
                "user_id": str(user_id),
                "document_id": str(document_id),
                "created_at": "NOW"  # Will be set by Qdrant
            }

            if payload:
                full_payload.update(payload)

            # Prepare points for upsert
            points = [
                models.PointStruct(
                    id=str(uuid.uuid4()),  # Generate a unique point ID
                    vector=embeddings,
                    payload=full_payload
                )
            ]

            # Upsert the vector
            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )

            logger.info(f"Successfully upserted vector for user {user_id} and document {document_id}")
            return True

        except UnexpectedResponse as e:
            logger.error(f"Qdrant API error during upsert: {e}")
            return False
        except Exception as e:
            logger.error(f"Error during upsert operation: {e}")
            return False

    def search_vectors(
        self,
        query_embedding: List[float],
        user_id: Optional[UUID] = None,
        top_k: int = 5,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Perform similarity search with user_id filtering
        """
        try:
            # Validate embedding dimensions
            if len(query_embedding) != VECTOR_DIMENSIONS:
                logger.error(f"Query embedding has wrong dimensions: {len(query_embedding)}, expected: {VECTOR_DIMENSIONS}")
                return []

            # Prepare filters
            search_filter = None
            if user_id or filters:
                conditions = []

                if user_id:
                    conditions.append(
                        models.FieldCondition(
                            key="user_id",
                            match=models.MatchValue(value=str(user_id))
                        )
                    )

                if filters:
                    for key, value in filters.items():
                        conditions.append(
                            models.FieldCondition(
                                key=key,
                                match=models.MatchValue(value=value)
                            )
                        )

                if conditions:
                    search_filter = models.Filter(
                        must=conditions
                    )

            # Perform search
            search_results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                query_filter=search_filter,
                limit=top_k,
                with_payload=True,
                with_vectors=False  # Don't return vectors to save bandwidth
            )

            # Format results
            formatted_results = []
            for result in search_results:
                formatted_result = {
                    "id": result.id,
                    "document_id": result.payload.get("document_id"),
                    "user_id": result.payload.get("user_id"),
                    "score": result.score,
                    "payload": result.payload
                }
                formatted_results.append(formatted_result)

            logger.info(f"Search completed, found {len(formatted_results)} results for user {user_id}")
            return formatted_results

        except UnexpectedResponse as e:
            logger.error(f"Qdrant API error during search: {e}")
            return []
        except Exception as e:
            logger.error(f"Error during search operation: {e}")
            return []

    def delete_vectors_by_document_id(self, document_id: UUID) -> bool:
        """
        Delete vectors associated with a specific document
        """
        try:
            # Create filter to find points with specific document_id
            search_filter = models.Filter(
                must=[
                    models.FieldCondition(
                        key="document_id",
                        match=models.MatchValue(value=str(document_id))
                    )
                ]
            )

            # Find points to delete
            search_results = self.client.search(
                collection_name=self.collection_name,
                query_vector=[0.0] * VECTOR_DIMENSIONS,  # Dummy vector for filtering only
                query_filter=search_filter,
                limit=1000,  # Max points to delete in one operation
                with_payload=False,
                with_vectors=False
            )

            if not search_results:
                logger.info(f"No vectors found for document {document_id}")
                return True

            # Extract point IDs to delete
            point_ids = [result.id for result in search_results]

            # Delete the points
            self.client.delete(
                collection_name=self.collection_name,
                points_selector=models.PointIdsList(
                    points=point_ids
                )
            )

            logger.info(f"Successfully deleted {len(point_ids)} vectors for document {document_id}")
            return True

        except UnexpectedResponse as e:
            logger.error(f"Qdrant API error during delete: {e}")
            return False
        except Exception as e:
            logger.error(f"Error during delete operation: {e}")
            return False

    def delete_vectors_by_user_id(self, user_id: UUID) -> bool:
        """
        Delete all vectors for a specific user (used when deleting user)
        """
        try:
            # Create filter to find points with specific user_id
            search_filter = models.Filter(
                must=[
                    models.FieldCondition(
                        key="user_id",
                        match=models.MatchValue(value=str(user_id))
                    )
                ]
            )

            # Find points to delete
            search_results = self.client.search(
                collection_name=self.collection_name,
                query_vector=[0.0] * VECTOR_DIMENSIONS,  # Dummy vector for filtering only
                query_filter=search_filter,
                limit=10000,  # Max points to delete in one operation
                with_payload=False,
                with_vectors=False
            )

            if not search_results:
                logger.info(f"No vectors found for user {user_id}")
                return True

            # Extract point IDs to delete
            point_ids = [result.id for result in search_results]

            # Delete the points
            self.client.delete(
                collection_name=self.collection_name,
                points_selector=models.PointIdsList(
                    points=point_ids
                )
            )

            logger.info(f"Successfully deleted {len(point_ids)} vectors for user {user_id}")
            return True

        except UnexpectedResponse as e:
            logger.error(f"Qdrant API error during user vector delete: {e}")
            return False
        except Exception as e:
            logger.error(f"Error during user vector delete operation: {e}")
            return False

    def update_vector_payload(self, point_id: str, payload: Dict[str, Any]) -> bool:
        """
        Update the payload of an existing vector
        """
        try:
            self.client.set_payload(
                collection_name=self.collection_name,
                payload=payload,
                points_selector=models.PointIdsList(
                    points=[point_id]
                )
            )

            logger.info(f"Successfully updated payload for point {point_id}")
            return True

        except UnexpectedResponse as e:
            logger.error(f"Qdrant API error during payload update: {e}")
            return False
        except Exception as e:
            logger.error(f"Error during payload update operation: {e}")
            return False

    def batch_upsert_vectors(
        self,
        user_id: UUID,
        document_id: UUID,
        embeddings_list: List[List[float]],
        payloads_list: Optional[List[Dict[str, Any]]] = None
    ) -> bool:
        """
        Batch upsert multiple vectors at once
        """
        try:
            points = []

            for i, embedding in enumerate(embeddings_list):
                # Validate embedding dimensions
                if len(embedding) != VECTOR_DIMENSIONS:
                    logger.error(f"Embedding {i} has wrong dimensions: {len(embedding)}, expected: {VECTOR_DIMENSIONS}")
                    return False

                # Prepare payload
                payload = {
                    "user_id": str(user_id),
                    "document_id": str(document_id),
                    "chunk_index": i  # For multi-chunk documents
                }

                if payloads_list and i < len(payloads_list):
                    payload.update(payloads_list[i])

                # Create point
                point = models.PointStruct(
                    id=str(uuid.uuid4()),
                    vector=embedding,
                    payload=payload
                )
                points.append(point)

            # Batch upsert
            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )

            logger.info(f"Successfully batch upserted {len(points)} vectors for user {user_id} and document {document_id}")
            return True

        except UnexpectedResponse as e:
            logger.error(f"Qdrant API error during batch upsert: {e}")
            return False
        except Exception as e:
            logger.error(f"Error during batch upsert operation: {e}")
            return False

    def get_vector_count(self, user_id: Optional[UUID] = None) -> int:
        """
        Get the count of vectors, optionally filtered by user_id
        """
        try:
            search_filter = None
            if user_id:
                search_filter = models.Filter(
                    must=[
                        models.FieldCondition(
                            key="user_id",
                            match=models.MatchValue(value=str(user_id))
                        )
                    ]
                )

            count_result = self.client.count(
                collection_name=self.collection_name,
                count_filter=search_filter
            )

            return count_result.count

        except UnexpectedResponse as e:
            logger.error(f"Qdrant API error during count: {e}")
            return 0
        except Exception as e:
            logger.error(f"Error during count operation: {e}")
            return 0


# Global instance of VectorOperations
vector_operations = VectorOperations()


def get_vector_operations() -> VectorOperations:
    """Get the vector operations instance"""
    return vector_operations