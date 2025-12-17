# AI-native Textbook Platform - Setup Instructions

## API Configuration

To use the AI features (chatbot, translation, personalization), you need to configure the following API keys:

### Gemini API Key
1. Get a Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Add it to the `.env` file:
   ```
   GEMINI_API_KEY=your_actual_gemini_api_key_here
   ```

### Neon Database Configuration
1. Create a Neon account at [Neon](https://neon.tech/)
2. Create a new project and get the connection string
3. Add it to the `.env` file:
   ```
   NEON_DB_URL=your_neon_connection_string_here
   ```

### Qdrant Vector Database
For local development:
1. Install Docker if not already installed
2. Run Qdrant locally:
   ```bash
   docker run -d --name qdrant-container -p 6333:6333 qdrant/qdrant
   ```
3. Add Qdrant configuration to the `.env` file:
   ```
   QDRANT_URL=http://localhost:6333
   QDRANT_API_KEY=your_qdrant_api_key_here  # Optional for local
   ```

## Processing Content PDF

To process your `content.pdf` file for embeddings and vector search:

1. **Install required dependencies**:
   ```bash
   pip install pypdf
   ```

2. **Create a PDF processing script** (or use existing tools in the project):
   ```python
   # Example script to process PDF and store in Qdrant
   import asyncio
   from pypdf import PdfReader
   from qdrant_client import QdrantClient
   from qdrant_client.http import models
   import google.generativeai as genai
   import hashlib

   def extract_text_from_pdf(pdf_path):
       """Extract text from PDF file"""
       reader = PdfReader(pdf_path)
       text = ""
       for page in reader.pages:
           text += page.extract_text() + "\n"
       return text

   def get_embeddings(text, api_key):
       """Get embeddings using Gemini (simulated)"""
       genai.configure(api_key=api_key)
       # For now, using hash-based embeddings (in production, use actual embedding API)
       hash_object = hashlib.md5(text.encode())
       hex_dig = hash_object.hexdigest()

       embedding = []
       for i in range(0, len(hex_dig), 2):
           embedding.append(int(hex_dig[i:i+2], 16) / 255.0)

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

       # Store the content
       qdrant_client.upsert(
           collection_name="documents",
           points=[
               models.PointStruct(
                   id=hashlib.md5(text.encode()).hexdigest(),
                   vector=embeddings,
                   payload={
                       "content": text,
                       "metadata": {"source": "content.pdf", "type": "document"}
                   }
               )
           ]
       )
   ```

## Running the Application

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Run database migrations
python src/scripts/migrate_neon.py

# Run the backend server
python main.py
```

### Frontend
```bash
cd frontend
npm install
npm start
```

## Troubleshooting

### Chatbot Returns Fallback Response
- Check that you have a valid Gemini API key in the `.env` file
- Verify the backend server is running on port 8001
- Ensure Qdrant is running if you want vector search capabilities

### API Endpoints Return 404
- Ensure the backend server is running on the correct port (8001)
- Check the proxy configuration in `docusaurus.config.js`

### Database Connection Issues
- Verify your Neon database connection string is correct
- Run the migration script: `python src/scripts/migrate_neon.py`
- Check that your database credentials are properly set in `.env`

### Qdrant Connection Issues
- Make sure Qdrant is running on localhost:6333
- Check that QDRANT_URL is set correctly in `.env`
- For local Qdrant, no API key is needed

## Database Schema

The system includes the following tables:
- `users`: Stores user account information
- `chat_history`: Stores chat history with context for each user
- Additional tables for document management and authentication