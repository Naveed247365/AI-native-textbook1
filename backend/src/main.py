from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# Import settings - this will validate environment variables on startup
from .config.settings import settings

app = FastAPI(
    title="AI Backend with RAG + Authentication",
    description="A scalable backend featuring authentication, RAG capabilities, and integration with external services",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "AI Backend with RAG + Authentication is running!"}


# Include all routes
from .routes import auth, search, history, documents, health

app.include_router(auth.router, prefix="/auth", tags=["authentication"])
app.include_router(search.router, prefix="/search", tags=["search"])
app.include_router(history.router, prefix="/history", tags=["history"])
app.include_router(documents.router, prefix="/documents", tags=["documents"])
app.include_router(health.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.server_host, port=settings.server_port)