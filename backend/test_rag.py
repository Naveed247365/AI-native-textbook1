import os
import sys
from dotenv import load_dotenv

# Load environment variables from parent directory
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# Add the backend directory to the path
sys.path.append(os.path.dirname(__file__))

from services.rag_service import RAGService
from qdrant_client import QdrantClient

def test_rag_service():
    # Get environment variables
    openrouter_api_key = os.getenv("OPENAI_API_KEY")
    qdrant_url = os.getenv("QDRANT_URL")
    qdrant_api_key = os.getenv("QDRANT_API_KEY")
    collection_name = os.getenv("QDRANT_COLLECTION", "project_documents")

    # Initialize Qdrant client for cloud
    if qdrant_url and qdrant_api_key and "qdrant.io" in qdrant_url:
        qdrant_client = QdrantClient(
            url=qdrant_url.replace(":6333", ""),  # Remove port from URL for cloud (same as in chat.py)
            api_key=qdrant_api_key,
            prefer_grpc=False
        )
    else:
        # Use local Qdrant if cloud not configured
        qdrant_client = QdrantClient(
            host=os.getenv("QDRANT_HOST", "localhost"),
            port=int(os.getenv("QDRANT_PORT", 6333))
        )

    # Initialize RAG service
    rag_service = RAGService(openrouter_api_key, qdrant_client, collection_name)

    print("Testing RAG Service...")

    # Test search functionality directly
    print("\n1. Testing direct search for 'Artificial Intelligence':")
    try:
        search_result = rag_service.search_qdrant("Artificial Intelligence")
        print(f"Search result: {search_result[:200]}...")  # First 200 chars
    except Exception as e:
        print(f"Search error: {e}")

    # Test RAG query
    print("\n2. Testing RAG query:")
    try:
        rag_result = rag_service.query_rag(
            selected_text="Artificial Intelligence",
            question="What is Artificial Intelligence?"
        )
        print(f"RAG result: {rag_result}")
    except Exception as e:
        print(f"RAG query error: {e}")

    # Test collection existence
    print("\n3. Testing collection info:")
    try:
        collection_info = qdrant_client.get_collection(collection_name)
        print(f"Collection info: {collection_info}")
        print(f"Points count: {collection_info.points_count}")
    except Exception as e:
        print(f"Collection info error: {e}")

if __name__ == "__main__":
    test_rag_service()