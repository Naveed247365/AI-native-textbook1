import os
import sys
from dotenv import load_dotenv

# Load environment variables from parent directory
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# Add the backend directory to the path
sys.path.append(os.path.dirname(__file__))

from services.rag_service import RAGService
from qdrant_client import QdrantClient

def test_rag_detailed():
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

    print("Testing RAG Service in detail...")

    # Test 1: Direct search
    print("\n1. Testing direct search for 'Artificial Intelligence':")
    try:
        search_result = rag_service.search_qdrant("Artificial Intelligence")
        print(f"Direct search result: {search_result[:200]}...")
    except Exception as e:
        print(f"Direct search error: {e}")

    # Test 2: RAG query with selected text that should match content
    print("\n2. Testing RAG query with matching selected text:")
    selected_text = "Artificial Intelligence is a branch of computer science that aims to create software or machines that exhibit human-like intelligence. This can include learning from experience, understanding natural language, solving problems, and recognizing patterns."
    question = "What is Artificial Intelligence?"

    try:
        rag_result = rag_service.query_rag(selected_text, question)
        print(f"RAG query result: {rag_result}")
    except Exception as e:
        print(f"RAG query error: {e}")
        import traceback
        traceback.print_exc()

    # Test 3: RAG query with non-matching text
    print("\n3. Testing RAG query with non-matching selected text:")
    selected_text_no_match = "This is completely unrelated text that should not match anything in the database."
    question = "What is Artificial Intelligence?"

    try:
        rag_result = rag_service.query_rag(selected_text_no_match, question)
        print(f"RAG query result: {rag_result}")
    except Exception as e:
        print(f"RAG query error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_rag_detailed()