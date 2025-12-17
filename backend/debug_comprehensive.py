import os
import sys
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.http import models

# Load environment variables from parent directory
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

def comprehensive_debug():
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

    # 2. Get collection info
    print(f"\n2. Collection info:")
    try:
        collection_info = qdrant_client.get_collection(collection_name)
        print(f"  Points count: {collection_info.points_count}")
        print(f"  Vector size: {collection_info.config.params.vectors.size}")
        print(f"  Distance: {collection_info.config.params.vectors.distance}")
    except Exception as e:
        print(f"  Error getting collection info: {e}")

    # 3. List all points in the collection (up to 10 for debugging)
    print(f"\n3. All points in collection (up to 10):")
    try:
        points = qdrant_client.scroll(
            collection_name=collection_name,
            limit=10
        )

        count = 0
        for point in points[0]:  # points[0] contains the list of points
            count += 1
            print(f"  Point {count}:")
            print(f"    ID: {point.id}")
            print(f"    Payload keys: {list(point.payload.keys()) if point.payload else 'None'}")
            if point.payload and 'content' in point.payload:
                content_preview = point.payload['content'][:100] + "..." if len(point.payload['content']) > 100 else point.payload['content']
                print(f"    Content preview: {content_preview}")
                print(f"    Topic: {point.payload.get('metadata', {}).get('topic', 'Unknown')}")
            print()

        print(f"  Total points found: {count}")
    except Exception as e:
        print(f"  Error listing points: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    comprehensive_debug()