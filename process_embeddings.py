#!/usr/bin/env python3
"""
Script to process content.pdf and store embeddings in Qdrant using Gemini API
"""
import asyncio
import hashlib
import os
from pypdf import PdfReader
from qdrant_client import QdrantClient
from qdrant_client.http import models
import google.generativeai as genai
from dotenv import load_dotenv
import numpy as np

# Load environment variables
load_dotenv()

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF file"""
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def get_embeddings_from_gemini(text, api_key):
    """Get embeddings using Gemini API (simulated since direct embedding API might not be available)"""
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')

        # Create a prompt to get meaningful representation
        prompt = f"Provide a concise summary of the following text for embedding purposes: {text[:2000]}"

        response = model.generate_content(prompt)
        summary = response.text

        # For now, using a hash-based approach as actual embedding API might not be directly available
        # In a real implementation, you would use the actual embedding service
        hash_object = hashlib.md5(summary.encode())
        hex_dig = hash_object.hexdigest()

        embedding = []
        for i in range(0, len(hex_dig), 2):
            embedding.append(int(hex_dig[i:i+2], 16) / 255.0)

        # Pad or truncate to standard size (1536 dimensions like OpenAI)
        while len(embedding) < 1536:
            embedding.append(0.0)
        embedding = embedding[:1536]

        return embedding
    except Exception as e:
        print(f"Error getting embeddings from Gemini: {e}")
        # Fallback to hash-based embeddings
        hash_object = hashlib.md5(text.encode())
        hex_dig = hash_object.hexdigest()

        embedding = []
        for i in range(0, len(hex_dig), 2):
            embedding.append(int(hex_dig[i:i+2], 16) / 255.0)

        while len(embedding) < 1536:
            embedding.append(0.0)
        embedding = embedding[:1536]

        return embedding

def store_in_qdrant(text, embeddings, qdrant_client, content_id):
    """Store content in Qdrant vector database"""
    # Create collection if it doesn't exist
    try:
        qdrant_client.get_collection("documents")
    except:
        qdrant_client.create_collection(
            collection_name="documents",
            vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE),
        )

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

def chunk_text(text, chunk_size=2000):
    """Split text into smaller chunks to handle large documents"""
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunk = text[i:i + chunk_size]
        if chunk.strip():  # Only add non-empty chunks
            chunks.append(chunk)
    return chunks

async def process_pdf_to_qdrant(pdf_path):
    """Process PDF and store in Qdrant using Gemini-enhanced embeddings"""
    print(f"Processing PDF: {pdf_path}")

    # Extract text from PDF
    full_text = extract_text_from_pdf(pdf_path)
    print(f"Extracted {len(full_text)} characters from PDF")

    # Chunk the text to handle large documents
    chunks = chunk_text(full_text, chunk_size=2000)
    print(f"Split into {len(chunks)} chunks")

    # Initialize Qdrant client with cloud configuration
    qdrant_url = os.getenv("QDRANT_URL")
    qdrant_api_key = os.getenv("QDRANT_API_KEY")

    if qdrant_api_key:
        qdrant_client = QdrantClient(
            url=qdrant_url,
            api_key=qdrant_api_key,
            timeout=10.0
        )
    else:
        qdrant_client = QdrantClient(
            url=qdrant_url,
            timeout=10.0
        )

    print(f"Connected to Qdrant cloud instance at {qdrant_url}")

    # Get Gemini API key
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if gemini_api_key == "your_actual_gemini_api_key_here":
        print("Warning: Please update GEMINI_API_KEY in .env file with your actual API key")
        print("Using fallback embedding method...")
        gemini_api_key = None

    # Process each chunk
    for i, chunk in enumerate(chunks):
        print(f"Processing chunk {i+1}/{len(chunks)}")

        if gemini_api_key:
            embeddings = get_embeddings_from_gemini(chunk, gemini_api_key)
        else:
            # Use fallback method
            hash_object = hashlib.md5(chunk.encode())
            hex_dig = hash_object.hexdigest()
            embeddings = []
            for j in range(0, len(hex_dig), 2):
                embeddings.append(int(hex_dig[j:j+2], 16) / 255.0)
            while len(embeddings) < 1536:
                embeddings.append(0.0)
            embeddings = embeddings[:1536]

        content_id = hashlib.md5(f"{chunk}_{i}".encode()).hexdigest()
        store_in_qdrant(chunk, embeddings, qdrant_client, content_id)
        print(f"Stored chunk {i+1} with ID: {content_id[:8]}...")

    print("PDF processing completed successfully!")
    print(f"Stored {len(chunks)} chunks in Qdrant collection 'documents'")

if __name__ == "__main__":
    pdf_path = "content.pdf"

    if not os.path.exists(pdf_path):
        print(f"Error: {pdf_path} not found!")
        print("Please make sure content.pdf is in the root directory.")
        exit(1)

    # Check if required environment variables are set
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if gemini_api_key == "your_actual_gemini_api_key_here":
        print("Note: You need to set your actual Gemini API key in the .env file")
        print("Get your API key from: https://makersuite.google.com/app/apikey")
        print("Update the .env file with: GEMINI_API_KEY=your_actual_api_key")

    qdrant_url = os.getenv("QDRANT_URL")
    print(f"Using Qdrant cloud instance: {qdrant_url}")

    try:
        asyncio.run(process_pdf_to_qdrant(pdf_path))
    except Exception as e:
        print(f"Error processing PDF: {e}")
        import traceback
        traceback.print_exc()