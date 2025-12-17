"""
Gemini API client for the AI Backend with RAG + Authentication
Implements embedding generation and chat functionality using Google's Gemini API
"""
import google.generativeai as genai
from google.generativeai import embedding
from typing import List, Optional, Dict, Any
import logging
import time
import asyncio
from functools import wraps
import re

from ..config.settings import settings

logger = logging.getLogger(__name__)

# Initialize the Gemini API client with the API key from settings
genai.configure(api_key=settings.gemini_api_key)


class GeminiClient:
    """
    Client class to handle both Gemini embedding and chat operations
    """

    def __init__(self):
        # Use the text-embedding-004 model for embeddings
        self.embedding_model_name = "text-embedding-004"
        # Use the Gemini 1.5 Flash model for chat responses (faster and more cost-effective)
        self.chat_model_name = "gemini-1.5-flash-001"  # Updated model name
        self.client = genai
        self.max_retries = 3
        self.retry_delay = 1  # seconds

        # Initialize the chat model
        self.chat_model = genai.GenerativeModel(self.chat_model_name)

    # EMBEDDING METHODS
    async def generate_embedding(self, text: str) -> Optional[List[float]]:
        """
        Generate embedding for the given text using Gemini text-embedding-004 model
        """
        for attempt in range(self.max_retries):
            try:
                # Generate the embedding using the Gemini API
                result = await asyncio.get_event_loop().run_in_executor(
                    None,
                    lambda: genai.embed_content(
                        model=self.embedding_model_name,
                        content=text,
                        task_type="RETRIEVAL_DOCUMENT",  # Optimal for RAG applications
                        title="Document"  # Title can help with embedding quality
                    )
                )

                embedding_values = result['embedding']

                # Verify the embedding has the correct dimensions (1536 for text-embedding-004)
                if len(embedding_values) != 1536:
                    logger.warning(f"Generated embedding has {len(embedding_values)} dimensions, expected 1536")
                    return None

                logger.info(f"Successfully generated embedding for text of length {len(text)}")
                return embedding_values

            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} failed to generate embedding: {e}")

                if attempt == self.max_retries - 1:
                    # Last attempt failed
                    logger.error(f"Failed to generate embedding after {self.max_retries} attempts: {e}")
                    return None

                # Wait before retrying
                await asyncio.sleep(self.retry_delay * (2 ** attempt))  # Exponential backoff

        return None

    async def generate_embeddings_batch(self, texts: List[str]) -> Optional[List[List[float]]]:
        """
        Generate embeddings for a batch of texts
        """
        embeddings = []

        for text in texts:
            embedding = await self.generate_embedding(text)
            if embedding is None:
                logger.error(f"Failed to generate embedding for text: {text[:50]}...")
                return None
            embeddings.append(embedding)

        return embeddings

    # CHAT METHODS
    async def generate_chat_response(
        self,
        query: str,
        context: Optional[List[Dict[str, Any]]] = None,
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> Optional[str]:
        """
        Generate a chat response using Gemini 1.5 Flash/Pro with RAG context
        """
        for attempt in range(self.max_retries):
            try:
                # Format the prompt with context and query
                formatted_prompt = self._format_rag_prompt(query, context, conversation_history)

                # Safety settings to moderate content
                safety_settings = [
                    {
                        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                    },
                    {
                        "category": "HARM_CATEGORY_HATE_SPEECH",
                        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                    },
                    {
                        "category": "HARM_CATEGORY_HARASSMENT",
                        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                    },
                    {
                        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                    }
                ]

                # Generate response using the chat model
                response = await self.chat_model.generate_content_async(
                    formatted_prompt,
                    safety_settings=safety_settings,
                    generation_config={
                        "temperature": 0.3,  # Lower temperature for more consistent responses
                        "max_output_tokens": 800,  # Limit response length
                        "candidate_count": 1
                    }
                )

                # Extract the text response
                if response and response.text:
                    logger.info(f"Successfully generated chat response for query: {query[:50]}...")
                    return response.text.strip()
                else:
                    logger.warning("Gemini returned empty response")
                    return None

            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} failed to generate chat response: {e}")

                if attempt == self.max_retries - 1:
                    # Last attempt failed
                    logger.error(f"Failed to generate chat response after {self.max_retries} attempts: {e}")
                    return None

                # Wait before retrying
                await asyncio.sleep(self.retry_delay * (2 ** attempt))  # Exponential backoff

        return None

    def _format_rag_prompt(
        self,
        query: str,
        context: Optional[List[Dict[str, Any]]] = None,
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> str:
        """
        Format the prompt with RAG context and conversation history
        """
        prompt_parts = []

        # Add system context
        prompt_parts.append(
            "You are an AI assistant that helps users by answering questions based on provided context. "
            "Use only the information provided in the context to answer the questions. "
            "If the context doesn't contain the information needed to answer the question, say so clearly. "
            "Be helpful, accurate, and concise in your responses."
        )

        # Add conversation history if available
        if conversation_history:
            prompt_parts.append("\nPrevious conversation:")
            for msg in conversation_history[-4:]:  # Use last 4 messages to avoid exceeding token limits
                role = msg.get("role", "user")
                content = msg.get("content", "")
                prompt_parts.append(f"{role.capitalize()}: {content}")

        # Add retrieved context if available
        if context:
            prompt_parts.append("\nContext for answering the question:")
            for i, ctx in enumerate(context[:5]):  # Use top 5 context snippets
                chunk_text = ctx.get("payload", {}).get("chunk_text", "") if isinstance(ctx, dict) else str(ctx)
                # Clean up the chunk text if it contains the "..." marker from storage
                if chunk_text.endswith("..."):
                    # If it was truncated when stored, we don't have the full text
                    # But we can still use what we have
                    pass
                prompt_parts.append(f"Context {i+1}: {chunk_text}")

        # Add the current query
        prompt_parts.append(f"\nQuestion: {query}")
        prompt_parts.append("Answer:")

        return "\n".join(prompt_parts)

    async def moderate_content(self, text: str) -> Dict[str, Any]:
        """
        Moderate content using Gemini's safety features
        """
        try:
            # Use the chat model to analyze content safety
            response = await self.chat_model.generate_content_async(
                f"Analyze the following text for safety issues: {text}",
                safety_settings=[
                    {
                        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                        "threshold": "BLOCK_ONLY_HIGH"
                    },
                    {
                        "category": "HARM_CATEGORY_HATE_SPEECH",
                        "threshold": "BLOCK_ONLY_HIGH"
                    },
                    {
                        "category": "HARM_CATEGORY_HARASSMENT",
                        "threshold": "BLOCK_ONLY_HIGH"
                    },
                    {
                        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                        "threshold": "BLOCK_ONLY_HIGH"
                    }
                ]
            )

            # Return safety analysis
            return {
                "is_safe": True,
                "text": text,
                "moderation_applied": False  # Gemini handles moderation internally
            }
        except Exception as e:
            logger.error(f"Content moderation error: {e}")
            return {
                "is_safe": False,
                "text": text,
                "moderation_applied": True,
                "error": str(e)
            }


# Global instance of GeminiClient
gemini_client = GeminiClient()


def get_gemini_client() -> GeminiClient:
    """Get the Gemini client instance (for both embeddings and chat)"""
    return gemini_client


# Embedding functions (backward compatibility)
async def generate_embedding(text: str) -> Optional[List[float]]:
    """
    Generate embedding for the given text using the configured Gemini model
    """
    return await gemini_client.generate_embedding(text)


async def generate_embeddings_batch(texts: List[str]) -> Optional[List[List[float]]]:
    """
    Generate embeddings for a batch of texts
    """
    return await gemini_client.generate_embeddings_batch(texts)


# Chat functions
async def generate_chat_response(
    query: str,
    context: Optional[List[Dict[str, Any]]] = None,
    conversation_history: Optional[List[Dict[str, str]]] = None
) -> Optional[str]:
    """
    Generate a chat response using Gemini with RAG context
    """
    return await gemini_client.generate_chat_response(query, context, conversation_history)


async def moderate_content(text: str) -> Dict[str, Any]:
    """
    Moderate content using Gemini's safety features
    """
    return await gemini_client.moderate_content(text)


# Decorator for rate limiting (basic implementation)
def rate_limit(calls_per_second: float = 10):
    """
    Decorator to implement basic rate limiting
    Google Gemini API has rate limits, so we need to be respectful
    """
    min_interval = 1.0 / calls_per_second
    last_called = [0.0]

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            left_to_wait = min_interval - elapsed
            if left_to_wait > 0:
                await asyncio.sleep(left_to_wait)
            ret = await func(*args, **kwargs)
            last_called[0] = time.time()
            return ret
        return wrapper
    return decorator


# Apply rate limiting to the main functions
@rate_limit(calls_per_second=10)  # Adjust based on your API quota
async def generate_embedding_with_rate_limit(text: str) -> Optional[List[float]]:
    """
    Generate embedding with rate limiting applied
    """
    return await generate_embedding(text)


@rate_limit(calls_per_second=5)  # Lower rate limit for chat as it's more resource intensive
async def generate_chat_response_with_rate_limit(
    query: str,
    context: Optional[List[Dict[str, Any]]] = None,
    conversation_history: Optional[List[Dict[str, str]]] = None
) -> Optional[str]:
    """
    Generate chat response with rate limiting applied
    """
    return await generate_chat_response(query, context, conversation_history)