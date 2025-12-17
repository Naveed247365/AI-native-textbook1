"""
Qdrant client setup for the AI Backend with RAG + Authentication
Implements Qdrant client initialization and connection management
"""
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.exceptions import UnexpectedResponse
from typing import Optional
import logging

from ..config.settings import settings

logger = logging.getLogger(__name__)

# Vector dimensions for Gemini text-embedding-004 model
VECTOR_DIMENSIONS = 1536  # Standard for text-embedding-004

class QdrantService:
    """
    Service class to manage Qdrant client and operations
    """

    def __init__(self):
        self.client: Optional[QdrantClient] = None
        self._initialize_client()

    def _initialize_client(self):
        """Initialize the Qdrant client with settings from configuration"""
        try:
            if settings.qdrant_api_key:
                if settings.qdrant_url.startswith('https://'):
                    # For cloud instances, use the URL directly with API key
                    self.client = QdrantClient(
                        url=settings.qdrant_url,
                        api_key=settings.qdrant_api_key,
                        timeout=10.0  # 10 second timeout
                    )
                else:
                    # For local instances
                    self.client = QdrantClient(
                        url=settings.qdrant_url,
                        api_key=settings.qdrant_api_key,
                        timeout=10.0  # 10 second timeout
                    )
            else:
                # If no API key is provided, connect without authentication
                self.client = QdrantClient(
                    url=settings.qdrant_url,
                    timeout=10.0  # 10 second timeout
                )

            logger.info("Qdrant client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Qdrant client: {e}")
            raise

    async def health_check(self) -> bool:
        """Check if Qdrant server is accessible"""
        try:
            # Try to get cluster info as a health check
            if self.client:
                cluster_info = self.client.get_cluster_info()
                logger.info(f"Qdrant health check passed. Cluster: {cluster_info}")
                return True
            return False
        except Exception as e:
            logger.error(f"Qdrant health check failed: {e}")
            return False

    def get_client(self) -> QdrantClient:
        """Get the initialized Qdrant client"""
        if self.client is None:
            raise RuntimeError("Qdrant client not initialized")
        return self.client


# Global instance of QdrantService
qdrant_service = QdrantService()


def get_qdrant_client() -> QdrantClient:
    """Get the Qdrant client instance"""
    return qdrant_service.get_client()


async def initialize_qdrant_collections():
    """Initialize required collections in Qdrant"""
    try:
        client = get_qdrant_client()

        # Check if the documents collection already exists
        collections = client.get_collections()
        collection_names = [collection.name for collection in collections.collections]

        if "documents" not in collection_names:
            # Create the documents collection with proper vector configuration
            client.create_collection(
                collection_name="documents",
                vectors_config=models.VectorParams(
                    size=VECTOR_DIMENSIONS,
                    distance=models.Distance.COSINE  # Cosine distance is good for embeddings
                )
            )
            logger.info("Created 'documents' collection in Qdrant")
        else:
            logger.info("Collection 'documents' already exists in Qdrant")

        # Verify the collection has the correct configuration
        collection_info = client.get_collection(collection_name="documents")
        vector_config = collection_info.config.params.vectors
        if hasattr(vector_config, 'size'):
            actual_size = vector_config.size
        else:
            # Handle the case where vector_config is a dictionary
            actual_size = vector_config['size'] if isinstance(vector_config, dict) else vector_config

        if actual_size != VECTOR_DIMENSIONS:
            logger.warning(f"Collection vector size is {actual_size}, expected {VECTOR_DIMENSIONS}")
        else:
            logger.info(f"Collection 'documents' has correct vector size: {VECTOR_DIMENSIONS}")

        return True

    except UnexpectedResponse as e:
        logger.error(f"Qdrant API error during collection initialization: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error during collection initialization: {e}")
        return False


# Initialize collections on module import
async def setup_qdrant():
    """Setup function to initialize Qdrant collections"""
    success = await initialize_qdrant_collections()
    if success:
        logger.info("Qdrant setup completed successfully")
    else:
        logger.error("Qdrant setup failed")
    return success