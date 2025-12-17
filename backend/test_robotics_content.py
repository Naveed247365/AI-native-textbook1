import os
import sys
from dotenv import load_dotenv

# Load environment variables from parent directory
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# Add the backend directory to the path
sys.path.append(os.path.dirname(__file__))

from services.rag_service import RAGService
from qdrant_client import QdrantClient

def test_robotics_content():
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

    print("Testing content related to robotics...")

    # Test 1: Search for robotics content
    print("\n1. Testing search for 'robotics':")
    try:
        search_result = rag_service.search_qdrant("robotics")
        print(f"Robotics search result: {search_result[:300]}...")
    except Exception as e:
        print(f"Robotics search error: {e}")

    # Test 2: Search for "Humanoid Robotics"
    print("\n2. Testing search for 'Humanoid Robotics':")
    try:
        search_result = rag_service.search_qdrant("Humanoid Robotics")
        print(f"Humanoid Robotics search result: {search_result[:300]}...")
    except Exception as e:
        print(f"Humanoid Robotics search error: {e}")

    # Test 3: Search for "Physical AI"
    print("\n3. Testing search for 'Physical AI':")
    try:
        search_result = rag_service.search_qdrant("Physical AI")
        print(f"Physical AI search result: {search_result[:300]}...")
    except Exception as e:
        print(f"Physical AI search error: {e}")

if __name__ == "__main__":
    test_robotics_content()