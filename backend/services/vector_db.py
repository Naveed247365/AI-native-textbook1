from qdrant_client import QdrantClient
from qdrant_client.http import models
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class VectorDBService:
    def __init__(self, host: str = "localhost", port: int = 6333, cloud_client=None):
        self.collection_name = "textbook_content"
        self.is_available = False  # Initialize as False by default

        if cloud_client:
            # Use provided cloud client
            self.client = cloud_client
            try:
                self._init_collection()
                self.is_available = True
            except Exception as e:
                import logging
                logger = logging.getLogger(__name__)
                logger.warning(f"Vector database not available: {str(e)}. Running in fallback mode.")
                self.client = None
        else:
            # Use local client
            try:
                self.client = QdrantClient(host=host, port=port)
                self._init_collection()
                self.is_available = True
            except Exception as e:
                import logging
                logger = logging.getLogger(__name__)
                logger.warning(f"Vector database not available: {str(e)}. Running in fallback mode.")
                self.client = None

    def _init_collection(self):
        """Initialize the Qdrant collection for textbook content"""
        if not self.is_available:
            return

        try:
            # Check if collection exists
            self.client.get_collection(self.collection_name)
        except:
            # Create collection if it doesn't exist
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE),  # Assuming OpenAI embeddings
            )
            logger.info(f"Created collection: {self.collection_name}")

    def add_content(self, content_id: str, content: str, embeddings: List[float], metadata: Dict[str, Any] = None):
        """Add textbook content to the vector database"""
        if not self.is_available:
            logger.warning("Vector database not available, skipping content addition")
            return

        if metadata is None:
            metadata = {}

        self.client.upsert(
            collection_name=self.collection_name,
            points=[
                models.PointStruct(
                    id=content_id,
                    vector=embeddings,
                    payload={
                        "content": content,
                        "metadata": metadata
                    }
                )
            ]
        )
        logger.info(f"Added content to vector DB: {content_id}")

    def search_content(self, query_embeddings: List[float], limit: int = 10) -> List[Dict[str, Any]]:
        """Search for relevant content based on query embeddings"""
        if not self.is_available or self.client is None:
            logger.warning("Vector database not available, returning empty results")
            # Return empty list when database is not available
            return []

        try:
            # Handle different Qdrant client versions
            if hasattr(self.client, 'search'):
                # Newer version of Qdrant client
                results = self.client.search(
                    collection_name=self.collection_name,
                    query_vector=query_embeddings,
                    limit=limit
                )
            else:
                # Older version or different interface
                results = self.client.search(
                    collection_name=self.collection_name,
                    query_vector=query_embeddings,
                    limit=limit
                )
        except AttributeError:
            logger.warning("Qdrant client search method not available, using direct processing")
            return []
        except Exception as e:
            logger.warning(f"Vector database search failed, using direct processing: {str(e)}")
            # Return empty list when search fails
            return []

        return [
            {
                "id": result.id,
                "content": result.payload.get("content"),
                "metadata": result.payload.get("metadata", {}),
                "score": getattr(result, 'score', 0.0)  # Handle different result structures
            }
            for result in results
        ]

    def delete_content(self, content_id: str):
        """Delete content from the vector database"""
        if not self.is_available:
            logger.warning("Vector database not available, skipping content deletion")
            return

        self.client.delete(
            collection_name=self.collection_name,
            points_selector=models.PointIdsList(points=[content_id])
        )
        logger.info(f"Deleted content from vector DB: {content_id}")