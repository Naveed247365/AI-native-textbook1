import os
import sys
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from openai import OpenAI

# Load environment variables from parent directory
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

def debug_search():
    # Initialize services
    openrouter_api_key = os.getenv("OPENAI_API_KEY")
    qdrant_url = os.getenv("QDRANT_URL")
    qdrant_api_key = os.getenv("QDRANT_API_KEY")
    collection_name = os.getenv("QDRANT_COLLECTION", "project_documents")

    client = OpenAI(
        api_key=openrouter_api_key,
        base_url="https://openrouter.ai/api/v1"
    )

    if qdrant_url and qdrant_api_key and "qdrant.io" in qdrant_url:
        qdrant_client = QdrantClient(
            url=qdrant_url.replace(":6333", ""),
            api_key=qdrant_api_key,
            prefer_grpc=False
        )
    else:
        qdrant_client = QdrantClient(
            host=os.getenv("QDRANT_HOST", "localhost"),
            port=int(os.getenv("QDRANT_PORT", 6333))
        )

    print("🔍 Debugging the search functionality")
    print("=" * 60)

    # Test 1: Search with short query (the problematic one)
    print("Test 1: Search with short query")
    query1 = "Introduction to Physical AI & Humanoid Robotics"
    print(f"  Query: '{query1}'")

    try:
        response1 = client.embeddings.create(
            model="text-embedding-3-small",
            input=query1
        )
        vector1 = response1.data[0].embedding

        hits1 = qdrant_client.search(
            collection_name=collection_name,
            query_vector=vector1,
            limit=5
        )

        print(f"  Found {len(hits1)} results:")
        for i, hit in enumerate(hits1):
            print(f"    Result {i+1}: Score={hit.score}, Content='{hit.payload['content'][:50]}...'")

        if len(hits1) == 0 or hits1[0].score < 0.7:  # Assuming low score means poor match
            print("  ⚠️  Low similarity scores - this might be the issue")
        else:
            print("  ✅ Good similarity scores found")
    except Exception as e:
        print(f"  ❌ Error: {e}")
    print()

    # Test 2: Search with longer, more descriptive query
    print("Test 2: Search with longer, more descriptive query")
    query2 = "Introduction to Physical AI & Humanoid Robotics: Embodied Intelligence represents the convergence of artificial intelligence with physical systems."
    print(f"  Query: '{query2[:50]}...'")

    try:
        response2 = client.embeddings.create(
            model="text-embedding-3-small",
            input=query2
        )
        vector2 = response2.data[0].embedding

        hits2 = qdrant_client.search(
            collection_name=collection_name,
            query_vector=vector2,
            limit=5
        )

        print(f"  Found {len(hits2)} results:")
        for i, hit in enumerate(hits2):
            print(f"    Result {i+1}: Score={hit.score}, Content='{hit.payload['content'][:50]}...'")

        if len(hits2) == 0 or hits2[0].score < 0.7:
            print("  ⚠️  Low similarity scores")
        else:
            print("  ✅ Good similarity scores found")
    except Exception as e:
        print(f"  ❌ Error: {e}")
    print()

    # Test 3: Search with question format
    print("Test 3: Search with question format")
    query3 = "What is embodied intelligence?"
    print(f"  Query: '{query3}'")

    try:
        response3 = client.embeddings.create(
            model="text-embedding-3-small",
            input=query3
        )
        vector3 = response3.data[0].embedding

        hits3 = qdrant_client.search(
            collection_name=collection_name,
            query_vector=vector3,
            limit=5
        )

        print(f"  Found {len(hits3)} results:")
        for i, hit in enumerate(hits3):
            print(f"    Result {i+1}: Score={hit.score}, Content='{hit.payload['content'][:50]}...'")

        if len(hits3) == 0 or hits3[0].score < 0.7:
            print("  ⚠️  Low similarity scores")
        else:
            print("  ✅ Good similarity scores found")
    except Exception as e:
        print(f"  ❌ Error: {e}")
    print()

    print("=" * 60)
    print("🔍 ANALYSIS:")
    print("The issue is likely that short titles don't embed well")
    print("compared to longer, more descriptive text or questions.")
    print("This causes the vector similarity search to return poor matches.")

if __name__ == "__main__":
    debug_search()