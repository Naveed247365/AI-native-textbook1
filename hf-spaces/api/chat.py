import os
import sys
from fastapi import APIRouter
import logging
from qdrant_client import QdrantClient

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.rag_service import RAGService

router = APIRouter()

# Configure OpenRouter and RAG service
openrouter_api_key = os.getenv("OPENAI_API_KEY")
qdrant_url = os.getenv("QDRANT_URL")
qdrant_api_key = os.getenv("QDRANT_API_KEY")
collection_name = os.getenv("QDRANT_COLLECTION", "project_documents")

if openrouter_api_key and openrouter_api_key != "your_openrouter_api_key_here":
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

    # Initialize RAG service with OpenRouter
    rag_service = RAGService(openrouter_api_key, qdrant_client, collection_name)
else:
    rag_service = None

logger = logging.getLogger(__name__)

@router.post("/chat")
async def chat(payload: dict):
    user_msg = payload["message"]
    selected_text = payload.get("selected_text", "")

    # If selected text is provided, try to use RAG service to answer based only on that text
    if selected_text and rag_service:
        try:
            # Use the RAG service to answer based on selected text only (with OpenRouter)
            answer = rag_service.query_rag(selected_text, user_msg)
            return {"answer": answer}
        except Exception as e:
            logger.error(f"RAG service failed: {str(e)}")
            # Fall through to fallback response below
    elif selected_text and not rag_service:
        logger.warning("RAG service not available, using fallback")

    # Fallback response when API is unavailable or not configured
    fallback_responses = {
        "hello": "Hello! I'm your AI textbook assistant. Feel free to ask questions about the content you're studying!",
        "hi": "Hi there! I'm here to help you understand the AI and robotics concepts in your textbook. What would you like to know?",
        "help": "I can help explain concepts from your AI and robotics textbook! Please select some text and ask questions about it.",
        "default": f"I'm currently unable to process your request about '{user_msg}'. This might be because the AI service is temporarily unavailable or needs to be configured with a valid API key. The system is working properly but requires a valid OPENROUTER_API_KEY to provide AI-generated responses."
    }

    response_text = fallback_responses.get(user_msg.lower().strip(), fallback_responses["default"])

    result = {"answer": response_text}
    if not rag_service:
        result["setup_needed"] = "Please configure a valid OPENROUTER_API_KEY in the .env file to enable AI responses"

    return result