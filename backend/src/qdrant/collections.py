"""
Qdrant collection management for the AI Backend with RAG + Authentication
Implements collection creation and management functions
"""
from qdrant_client import QdrantClient
from qdrant_client.http import models
from typing import Optional
import logging

from ..config.settings import settings
from .client import get_qdrant_client, VECTOR_DIMENSIONS

logger = logging.getLogger(__name__)


class CollectionManager:
    """
    Manager class to handle Qdrant collection operations
    """

    def __init__(self):
        self.client: QdrantClient = get_qdrant_client()

    def create_documents_collection(self) -> bool:
        """
        Create the documents collection with proper schema for RAG
        """
        try:
            # Check if collection already exists
            collections = self.client.get_collections()
            collection_names = [collection.name for collection in collections.collections]

            if "documents" in collection_names:
                logger.info("Documents collection already exists")
                # Verify the existing collection has correct configuration
                collection_info = self.client.get_collection(collection_name="documents")
                vector_config = collection_info.config.params.vectors
                if hasattr(vector_config, 'size'):
                    actual_size = vector_config.size
                else:
                    # Handle different API versions
                    actual_size = vector_config.get('size', 0) if isinstance(vector_config, dict) else 0

                if actual_size != VECTOR_DIMENSIONS:
                    logger.error(f"Existing collection has wrong vector size: {actual_size}, expected: {VECTOR_DIMENSIONS}")
                    return False
                else:
                    logger.info(f"Existing documents collection has correct vector size: {VECTOR_DIMENSIONS}")
                return True

            # Create the documents collection with proper configuration
            self.client.create_collection(
                collection_name="documents",
                vectors_config=models.VectorParams(
                    size=VECTOR_DIMENSIONS,
                    distance=models.Distance.COSINE  # Cosine distance is optimal for embeddings
                ),
                # Set up HNSW index for efficient similarity search
                hnsw_config=models.HnswConfigDiff(
                    m=16,  # Defines how many neighbors for each vector
                    ef_construct=100,  # Number of vectors to consider during index construction
                    full_scan_threshold=10000,  # Use plain index for small collections
                ),
                # Set up quantization for memory optimization
                quantization_config=models.ScalarQuantization(
                    type=models.QuantizationType.INT8,
                    always_ram=True  # Keep quantized vectors in RAM for faster search
                )
            )

            # Create payload index for user_id to enable efficient filtering
            self.client.create_payload_index(
                collection_name="documents",
                field_name="user_id",
                field_schema=models.PayloadSchemaType.KEYWORD
            )

            logger.info(f"Created 'documents' collection with vector size {VECTOR_DIMENSIONS}")
            return True

        except Exception as e:
            logger.error(f"Error creating documents collection: {e}")
            return False

    def collection_exists(self, collection_name: str) -> bool:
        """
        Check if a collection exists
        """
        try:
            collections = self.client.get_collections()
            collection_names = [collection.name for collection in collections.collections]
            return collection_name in collection_names
        except Exception as e:
            logger.error(f"Error checking if collection exists: {e}")
            return False

    def get_collection_info(self, collection_name: str) -> Optional[models.CollectionInfo]:
        """
        Get information about a specific collection
        """
        try:
            return self.client.get_collection(collection_name)
        except Exception as e:
            logger.error(f"Error getting collection info: {e}")
            return None

    def recreate_collection(self, collection_name: str) -> bool:
        """
        Recreate a collection (useful for development)
        """
        try:
            # Delete the collection if it exists
            if self.collection_exists(collection_name):
                self.client.delete_collection(collection_name)
                logger.info(f"Deleted collection: {collection_name}")

            # Create the collection with proper configuration
            if collection_name == "documents":
                return self.create_documents_collection()
            else:
                logger.error(f"Unknown collection name: {collection_name}")
                return False

        except Exception as e:
            logger.error(f"Error recreating collection {collection_name}: {e}")
            return False

    def drop_collection(self, collection_name: str) -> bool:
        """
        Drop a collection
        """
        try:
            if self.collection_exists(collection_name):
                self.client.delete_collection(collection_name)
                logger.info(f"Dropped collection: {collection_name}")
                return True
            else:
                logger.warning(f"Collection {collection_name} does not exist")
                return False
        except Exception as e:
            logger.error(f"Error dropping collection {collection_name}: {e}")
            return False


# Global instance of CollectionManager
collection_manager = CollectionManager()


def get_collection_manager() -> CollectionManager:
    """Get the collection manager instance"""
    return collection_manager


def initialize_collections() -> bool:
    """
    Initialize all required collections
    """
    logger.info("Initializing Qdrant collections...")

    # Create the documents collection
    success = collection_manager.create_documents_collection()

    if success:
        logger.info("All Qdrant collections initialized successfully")
        return True
    else:
        logger.error("Failed to initialize Qdrant collections")
        return False