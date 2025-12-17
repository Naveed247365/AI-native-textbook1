import os
import sys
from dotenv import load_dotenv
from qdrant_client import QdrantClient

# Load environment variables from parent directory
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

def debug_qdrant():
    # Get environment variables
    qdrant_url = os.getenv("QDRANT_URL")
    qdrant_api_key = os.getenv("QDRANT_API_KEY")
    collection_name = os.getenv("QDRANT_COLLECTION", "project_documents")

    print(f"QDRANT_URL: {qdrant_url}")
    print(f"Collection: {collection_name}")

    # Initialize Qdrant client for cloud
    if qdrant_url and qdrant_api_key and "qdrant.io" in qdrant_url:
        qdrant_client = QdrantClient(
            url=qdrant_url.replace(":6333", ""),  # Remove port from URL for cloud
            api_key=qdrant_api_key,
            prefer_grpc=False
        )
    else:
        # Use local Qdrant if cloud not configured
        qdrant_client = QdrantClient(
            host=os.getenv("QDRANT_HOST", "localhost"),
            port=int(os.getenv("QDRANT_PORT", 6333))
        )

    # 1. Check collections
    print("\n1. Available collections:")
    try:
        collections = qdrant_client.get_collections()
        for collection in collections.collections:
            print(f"  - {collection.name}")
    except Exception as e:
        print(f"  Error getting collections: {e}")

    # 2. Try to search for content to verify it exists
    print(f"\n2. Testing search functionality:")
    try:
        # Try to create a simple embedding to test if connection works
        from openai import OpenAI
        openrouter_api_key = os.getenv("OPENAI_API_KEY")
        client = OpenAI(
            api_key=openrouter_api_key,
            base_url="https://openrouter.ai/api/v1"
        )

        response = client.embeddings.create(
            model="text-embedding-3-small",
            input="Artificial Intelligence"
        )
        vector = response.data[0].embedding

        # Now search in Qdrant
        hits = qdrant_client.search(
            collection_name=collection_name,
            query_vector=vector,
            limit=2
        )

        print(f"  Search successful! Found {len(hits)} results")
        if hits:
            for i, hit in enumerate(hits):
                print(f"  Result {i+1}:")
                print(f"    ID: {hit.id}")
                print(f"    Payload keys: {list(hit.payload.keys()) if hit.payload else 'None'}")
                if hit.payload and 'content' in hit.payload:
                    print(f"    Content preview: {hit.payload['content'][:100]}...")
                else:
                    print(f"    Payload content: {hit.payload}")
    except Exception as e:
        print(f"  Error during search test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_qdrant()