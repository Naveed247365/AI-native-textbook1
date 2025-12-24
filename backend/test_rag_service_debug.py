"""
Debug the RAG service to see what's happening
"""
import os
import sys
import logging
from dotenv import load_dotenv
from qdrant_client import QdrantClient

# Setup logging
logging.basicConfig(level=logging.DEBUG)

# Load environment
load_dotenv()

# Import RAG service
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from services.rag_service import RAGService

# Initialize
api_key = os.getenv("OPENAI_API_KEY")
qdrant_url = os.getenv("QDRANT_URL")
qdrant_api_key = os.getenv("QDRANT_API_KEY")
collection_name = os.getenv("QDRANT_COLLECTION", "project_documents")

print(f"API Key: {api_key[:20]}..." if api_key else "No API key")
print(f"Qdrant URL: {qdrant_url}")
print(f"Collection: {collection_name}")

# Initialize Qdrant client
qdrant_host = os.getenv("QDRANT_HOST")
if qdrant_api_key and qdrant_host and "qdrant.io" in qdrant_host:
    print("\n✅ Using Qdrant Cloud")
    qdrant_client = QdrantClient(
        url=qdrant_host,
        api_key=qdrant_api_key,
        prefer_grpc=False
    )
else:
    print("\n✅ Using Local Qdrant (without Qdrant for testing)")
    # Don't initialize Qdrant for now - test without it
    qdrant_client = None
    print("⚠️ Qdrant disabled for testing - will use selected text only")

# Initialize RAG service
rag_service = RAGService(api_key, qdrant_client, collection_name)

# Test query
selected_text = """
Physical AI refers to artificial intelligence systems that interact with the physical world.
These systems use sensors to perceive their environment and actuators to take actions.
Examples include robots, self-driving cars, and drones.
"""

question = "What is Physical AI?"

print("\n=== Testing RAG Service ===")
print(f"Selected Text Length: {len(selected_text)} chars")
print(f"Question: {question}")

try:
    answer = rag_service.query_rag(selected_text, question)
    print(f"\n✅ Answer received:")
    print(f"Length: {len(answer)} chars")
    print(f"Content: {answer}")

    if "Is sawal ka jawab provided data me mojood nahi hai" in answer:
        print("\n❌ ERROR: Getting fallback message!")
        print("This means the RAG logic is failing somewhere.")
except Exception as e:
    print(f"\n❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()
