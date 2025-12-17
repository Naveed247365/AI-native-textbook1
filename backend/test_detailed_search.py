import os
import sys
from dotenv import load_dotenv

# Load environment variables from parent directory
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# Add the backend directory to the path
sys.path.append(os.path.dirname(__file__))

from services.rag_service import RAGService
from qdrant_client import QdrantClient

def test_detailed_search():
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

    print("Testing detailed search functionality...")

    # Test the exact text that was returned from the search
    robotics_text = "Robotics is an interdisciplinary field that combines mechanical engineering, electrical engineering, and computer science to design, construct, and operate robots. Modern robots can perform complex tasks in manufacturing, healthcare, exploration, and service industries. They often incorporate AI to"

    print(f"\nTesting with the exact text from search result (length: {len(robotics_text)}):")

    # Test direct search with this text
    try:
        search_result = rag_service.search_qdrant(robotics_text)
        print(f"Direct search result: {search_result[:100]}...")
        print(f"Result length: {len(search_result)}")
    except Exception as e:
        print(f"Direct search error: {e}")

    # Test RAG query with this text
    try:
        rag_result = rag_service.query_rag(robotics_text, "What is robotics?")
        print(f"RAG query result: {rag_result[:200]}...")
    except Exception as e:
        print(f"RAG query error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_detailed_search()