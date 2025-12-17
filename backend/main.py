import sys
import os
from dotenv import load_dotenv

# Load environment variables from .env file in the project root
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dotenv_path = os.path.join(project_root, '.env')
load_dotenv(dotenv_path)

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from api.chat import router as chat_router
from api.auth import router as auth_router
from api.translation import router as translation_router
from api.personalization import router as personalization_router
from api.rag_search import router as rag_search_router
from api.chat import router as chat_api_router  # New chat API with RAG

app = FastAPI(title="AI-native Textbook Platform API")

# Add CORS middleware to allow requests from the Docusaurus frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://localhost:8000", "*"],  # Allow frontend origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_origin_regex=r"https?://localhost(:[0-9]+)?",
)

# Include API routers
app.include_router(chat_router, prefix="/api")  # Original chat API (for compatibility)
app.include_router(auth_router, prefix="/api")
app.include_router(translation_router, prefix="/api")
app.include_router(personalization_router, prefix="/api")
app.include_router(rag_search_router, prefix="/api")
# New enhanced chat API with RAG is included in the original chat_router

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI-native Interactive Textbook Platform for Physical AI & Humanoid Robotics"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)