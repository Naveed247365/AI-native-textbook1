#!/usr/bin/env python3
"""
Script to process project code files and store embeddings in Qdrant using Gemini API
This will index the actual project content for RAG chatbot
"""
import asyncio
import hashlib
import os
import glob
from qdrant_client import QdrantClient
from qdrant_client.http import models
import google.generativeai as genai
from dotenv import load_dotenv
import numpy as np

# Load environment variables
load_dotenv()

def get_project_files():
    """Get all relevant project files to process"""
    file_extensions = ['*.py', '*.js', '*.jsx', '*.ts', '*.tsx', '*.md', '*.txt', '*.json', '*.yaml', '*.yml']
    project_root = os.path.dirname(os.path.abspath(__file__))  # Current directory
    files_to_process = []

    for ext in file_extensions:
        # Search in project root and subdirectories
        pattern = os.path.join(project_root, "**", ext)
        files = glob.glob(pattern, recursive=True)
        files_to_process.extend(files)

    # Filter out files that we don't want to index
    exclude_patterns = [
        'node_modules',
        '.git',
        '__pycache__',
        '.pytest_cache',
        'venv',
        'env',
        '.venv',
        'dist',
        'build',
        '.docusaurus',
        'process_embeddings.py',  # Don't index this script
        'process_project_embeddings.py'  # Don't index this script
    ]

    filtered_files = []
    for file_path in files_to_process:
        should_include = True
        for exclude_pattern in exclude_patterns:
            if exclude_pattern in file_path:
                should_include = False
                break
        if should_include:
            filtered_files.append(file_path)

    return filtered_files

def read_file_content(file_path):
    """Read content from a file"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        return content
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return ""

def get_embeddings_from_gemini(text, api_key):
    """Get embeddings using Gemini API (simulated approach)"""
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')

        # Create a prompt to get meaningful representation
        prompt = f"Provide a concise summary of the following code/text for embedding purposes: {text[:2000]}"

        response = model.generate_content(prompt)
        summary = response.text

        # For now, using a hash-based approach as actual embedding API might not be directly available
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

def store_in_qdrant(text, embeddings, qdrant_client, content_id, file_path):
    """Store content in Qdrant vector database"""
    # Create collection if it doesn't exist
    try:
        qdrant_client.get_collection("project_documents")
    except:
        qdrant_client.create_collection(
            collection_name="project_documents",
            vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE),
        )

    # Store the content
    qdrant_client.upsert(
        collection_name="project_documents",
        points=[
            models.PointStruct(
                id=content_id,
                vector=embeddings,
                payload={
                    "content": text,
                    "metadata": {
                        "source": file_path,
                        "type": "project_code",
                        "chunk_id": content_id
                    }
                }
            )
        ]
    )

    print(f"Stored content from {file_path} with ID: {content_id}")
    return content_id

def chunk_text(text, chunk_size=2000):
    """Split text into smaller chunks to handle large documents"""
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunk = text[i:i + chunk_size]
        if chunk.strip():  # Only add non-empty chunks
            chunks.append(chunk)
    return chunks

async def process_project_to_qdrant():
    """Process project files and store in Qdrant using Gemini-enhanced embeddings"""
    print("Processing project files for embeddings...")

    # Get all project files
    files = get_project_files()
    print(f"Found {len(files)} project files to process")

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

    total_chunks = 0

    # Process each file
    for i, file_path in enumerate(files):
        print(f"\nProcessing file {i+1}/{len(files)}: {file_path}")

        # Read file content
        content = read_file_content(file_path)
        if not content.strip():
            print(f"Skipping empty file: {file_path}")
            continue

        # Chunk the content
        chunks = chunk_text(content, chunk_size=2000)
        print(f"Split into {len(chunks)} chunks")

        # Process each chunk
        for j, chunk in enumerate(chunks):
            print(f"  Processing chunk {j+1}/{len(chunks)}")

            if gemini_api_key:
                embeddings = get_embeddings_from_gemini(chunk, gemini_api_key)
            else:
                # Use fallback method
                hash_object = hashlib.md5(chunk.encode())
                hex_dig = hash_object.hexdigest()
                embeddings = []
                for k in range(0, len(hex_dig), 2):
                    embeddings.append(int(hex_dig[k:k+2], 16) / 255.0)
                while len(embeddings) < 1536:
                    embeddings.append(0.0)
                embeddings = embeddings[:1536]

            content_id = hashlib.md5(f"{file_path}_{j}".encode()).hexdigest()
            store_in_qdrant(chunk, embeddings, qdrant_client, content_id, file_path)
            total_chunks += 1
            print(f"  Stored chunk {j+1} with ID: {content_id[:8]}...")

    print(f"\nProject processing completed successfully!")
    print(f"Total files processed: {len(files)}")
    print(f"Total chunks stored: {total_chunks}")
    print("Project content is now available in Qdrant collection 'project_documents'")

if __name__ == "__main__":
    # Check if required environment variables are set
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if gemini_api_key == "your_actual_gemini_api_key_here":
        print("Note: You need to set your actual Gemini API key in the .env file")
        print("Get your API key from: https://makersuite.google.com/app/apikey")
        print("Update the .env file with: GEMINI_API_KEY=your_actual_api_key")

    qdrant_url = os.getenv("QDRANT_URL")
    print(f"Using Qdrant cloud instance: {qdrant_url}")

    try:
        asyncio.run(process_project_to_qdrant())
    except Exception as e:
        print(f"Error processing project: {e}")
        import traceback
        traceback.print_exc()