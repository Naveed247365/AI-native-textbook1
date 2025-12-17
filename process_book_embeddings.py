#!/usr/bin/env python3
"""
Script to process all textbook documentation content and store embeddings in Qdrant
This will index all the textbook content for comprehensive RAG functionality using OpenRouter
"""
import os
import uuid
import re
from pathlib import Path
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from openai import OpenAI

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

def chunk_text(text, max_chunk_size=1000, overlap=100):
    """
    Split text into overlapping chunks to preserve context
    """
    if len(text) <= max_chunk_size:
        return [text]

    chunks = []
    start = 0

    while start < len(text):
        end = start + max_chunk_size

        # Try to break at sentence boundary if possible
        if end < len(text):
            # Look for sentence endings near the boundary
            sentence_end = text.rfind('.', start, end)
            if sentence_end > start + max_chunk_size // 2:  # Only if it's reasonably close
                end = sentence_end + 1
            else:
                # Look for paragraph breaks
                para_end = text.rfind('\n\n', start, end)
                if para_end > start + max_chunk_size // 2:
                    end = para_end

        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        start = end - overlap  # Overlap to maintain context

    return chunks

def extract_content_from_md(file_path):
    """
    Extract content from markdown file, removing frontmatter
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove frontmatter if present (between --- markers)
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            content = parts[2]

    return content.strip()

def process_all_docs():
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

    # Get all markdown files from the docs directory
    docs_dir = Path("frontend/docs")
    md_files = list(docs_dir.rglob("*.md"))

    print(f"Found {len(md_files)} markdown files to process")

    total_chunks = 0
    processed_files = 0

    for md_file in md_files:
        print(f"Processing: {md_file}")

        try:
            # Extract content from markdown file
            content = extract_content_from_md(md_file)

            # Skip if content is too short
            if len(content.strip()) < 50:
                print(f"  Skipping {md_file} - content too short")
                continue

            # Create chunks
            chunks = chunk_text(content, max_chunk_size=1000, overlap=100)

            print(f"  Created {len(chunks)} chunks")

            # Process each chunk
            for i, chunk in enumerate(chunks):
                if chunk.strip():  # Only process non-empty chunks
                    try:
                        # Create embedding
                        response = client.embeddings.create(
                            model="text-embedding-3-small",
                            input=chunk
                        )
                        embedding = response.data[0].embedding

                        # Create unique ID for this chunk
                        chunk_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{md_file}_{i}_{len(chunk)}"))

                        # Store in Qdrant
                        qdrant_client.upsert(
                            collection_name=collection_name,
                            points=[
                                {
                                    "id": chunk_id,
                                    "vector": embedding,
                                    "payload": {
                                        "content": chunk,
                                        "source_file": str(md_file),
                                        "chunk_index": i,
                                        "chunk_size": len(chunk),
                                        "metadata": {
                                            "source": str(md_file.name),
                                            "section": str(md_file.parent.name),
                                            "full_path": str(md_file)
                                        }
                                    }
                                }
                            ]
                        )

                        total_chunks += 1

                    except Exception as e:
                        print(f"  Error processing chunk {i}: {e}")

            processed_files += 1

        except Exception as e:
            print(f"  Error processing {md_file}: {e}")

    print(f"\n✅ Successfully processed {processed_files} files")
    print(f"✅ Created embeddings for {total_chunks} content chunks")
    print(f"✅ All content indexed in Qdrant collection: {collection_name}")

if __name__ == "__main__":
    process_all_docs()