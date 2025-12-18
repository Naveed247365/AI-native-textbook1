import os
import sys
from dotenv import load_dotenv

# Load environment variables
project_root = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(project_root, '.env')
load_dotenv(dotenv_path)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from api.chat import router as chat_router
from api.auth import router as auth_router
from api.translation import router as translation_router
from api.personalization import router as personalization_router
from api.rag_search import router as rag_search_router

app = FastAPI(title="AI-native Textbook Platform API - Hugging Face Version")

# Add CORS middleware (more permissive for Hugging Face Spaces)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Hugging Face Spaces may need this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(chat_router, prefix="/api")
app.include_router(auth_router, prefix="/api")
app.include_router(translation_router, prefix="/api")
app.include_router(personalization_router, prefix="/api")
app.include_router(rag_search_router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "AI-native Interactive Textbook Platform for Physical AI & Humanoid Robotics - Running on Hugging Face Spaces"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# For Hugging Face Spaces, use port 7860
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    uvicorn.run(app, host="0.0.0.0", port=port)