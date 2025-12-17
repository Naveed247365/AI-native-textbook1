#!/usr/bin/env python3
"""
Test script to check if Qdrant is running and accessible
"""
from qdrant_client import QdrantClient

def test_qdrant_connection():
    try:
        # Try to connect to Qdrant
        client = QdrantClient(host="localhost", port=6333)

        # Test connection by getting collections
        collections = client.get_collections()
        print("✅ Qdrant is running and accessible!")
        print(f"Available collections: {collections}")
        return True
    except Exception as e:
        print(f"❌ Qdrant is not running or accessible: {e}")
        print("💡 To run Qdrant locally, you can use Docker:")
        print("   docker run -d --name qdrant-container -p 6333:6333 qdrant/qdrant")
        return False

if __name__ == "__main__":
    test_qdrant_connection()