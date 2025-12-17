#!/usr/bin/env python3
"""
Script to process content.pdf and store embeddings in Qdrant
"""
import asyncio
import hashlib
import os
from pypdf import PdfReader
from qdrant_client import QdrantClient
from qdrant_client.http import models
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF file"""
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def get_embeddings(text):
    """Get embeddings using hash-based approach (simulated for now)"""
    # Using hash-based embeddings since we may not have a real embedding API
    hash_object = hashlib.md5(text.encode())
    hex_dig = hash_object.hexdigest()

    embedding = []
    for i in range(0, len(hex_dig), 2):
        embedding.append(int(hex_dig[i:i+2], 16) / 255.0)

    # Pad or truncate to standard size (1536 dimensions like OpenAI)
    while len(embedding) < 1536:
        embedding.append(0.0)
    embedding = embedding[:1536]

    return embedding

def store_in_qdrant(text, embeddings, qdrant_client):
    """Store content in Qdrant vector database"""
    # Create collection if it doesn't exist
    try:
        qdrant_client.get_collection("documents")
    except:
        qdrant_client.create_collection(
            collection_name="documents",
            vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE),
        )

    # Generate a unique ID for the content
    content_id = hashlib.md5(text.encode()).hexdigest()

    # Store the content
    qdrant_client.upsert(
        collection_name="documents",
        points=[
            models.PointStruct(
                id=content_id,
                vector=embeddings,
                payload={
                    "content": text,
                    "metadata": {"source": "content.pdf", "type": "document", "chunk_id": content_id}
                }
            )
        ]
    )

    print(f"Stored content chunk with ID: {content_id}")
    return content_id

def chunk_text(text, chunk_size=1000):
    """Split text into smaller chunks to handle large documents"""
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunk = text[i:i + chunk_size]
        if chunk.strip():  # Only add non-empty chunks
            chunks.append(chunk)
    return chunks

async def process_pdf_to_qdrant(pdf_path):
    """Process PDF and store in Qdrant"""
    print(f"Processing PDF: {pdf_path}")

    # Extract text from PDF
    full_text = extract_text_from_pdf(pdf_path)
    print(f"Extracted {len(full_text)} characters from PDF")

    # Chunk the text to handle large documents
    chunks = chunk_text(full_text, chunk_size=1000)
    print(f"Split into {len(chunks)} chunks")

    # Initialize Qdrant client
    qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333")
    qdrant_api_key = os.getenv("QDRANT_API_KEY")

    if qdrant_api_key:
        qdrant_client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key, timeout=10.0)
    else:
        qdrant_client = QdrantClient(url=qdrant_url, timeout=10.0)

    print(f"Connected to Qdrant at {qdrant_url}")

    # Process each chunk
    for i, chunk in enumerate(chunks):
        print(f"Processing chunk {i+1}/{len(chunks)}")
        embeddings = get_embeddings(chunk)
        content_id = store_in_qdrant(chunk, embeddings, qdrant_client)
        print(f"Stored chunk {i+1} with ID: {content_id[:8]}...")

    print("PDF processing completed successfully!")

if __name__ == "__main__":
    pdf_path = "content.pdf"

    if not os.path.exists(pdf_path):
        print(f"Error: {pdf_path} not found!")
        print("Please make sure content.pdf is in the root directory.")
        exit(1)

    # Check if required environment variables are set
    gemini_api_key = os.getenv("GEMINI_API_KEY", "your-gemini-key-here")
    if gemini_api_key == "your-gemini-key-here":
        print("Warning: GEMINI_API_KEY is not set in .env file")
        print("Please set it to use the full AI capabilities.")

    try:
        asyncio.run(process_pdf_to_qdrant(pdf_path))
    except Exception as e:
        print(f"Error processing PDF: {e}")
        import traceback
        traceback.print_exc()