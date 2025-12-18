from typing import List, Dict, Any
import logging
import os
from openai import OpenAI
from qdrant_client import QdrantClient
import json

logger = logging.getLogger(__name__)

class RAGService:
    def __init__(self, openrouter_api_key: str, vector_db_service: QdrantClient, collection_name: str = "project_documents"):
        # Initialize OpenRouter client
        self.client = OpenAI(
            api_key=openrouter_api_key,
            base_url="https://openrouter.ai/api/v1"
        )
        self.qdrant = vector_db_service
        self.collection_name = collection_name

    def get_embedding(self, text: str) -> List[float]:
        """Get embeddings for text using OpenAI's embedding API"""
        try:
            response = self.client.embeddings.create(
                model="text-embedding-3-small",
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"Error getting embeddings: {str(e)}")
            raise e

    def search_qdrant(self, query: str) -> str:
        """Search Qdrant for relevant content based on query"""
        try:
            vector = self.get_embedding(query)

            hits = self.qdrant.search(
                collection_name=self.collection_name,
                query_vector=vector,
                limit=5
            )

            return "\n\n".join(hit.payload["content"] for hit in hits if "content" in hit.payload)
        except Exception as e:
            logger.error(f"Error searching Qdrant: {str(e)}")
            return ""

    def query_rag(self, selected_text: str, question: str) -> str:
        """Process a RAG query using OpenRouter with context from Qdrant"""
        # Validate inputs
        if not selected_text or len(selected_text.strip()) == 0:
            # Check length (as per requirement TC-002: max 5000 characters)
            if len(selected_text) > 5000:
                logger.warning(f"Selected text exceeds 5000 character limit: {len(selected_text)} characters")
                return "Selected text exceeds the 5000 character limit. Please select a shorter text."

        SYSTEM_PROMPT = """You are a RAG-based AI agent.

RULES:
- Answer ONLY from the retrieved context.
- If the answer is not found, say:
  "Is sawal ka jawab provided data me mojood nahi hai."""

        try:
            # Search Qdrant using the selected_text to get relevant context
            context = self.search_qdrant(selected_text)

            # If we found context, generate the final answer using the context
            if context.strip():
                final_response = self.client.chat.completions.create(
                    model="openai/gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "assistant", "content": f"Here is the relevant context: {context}"},
                        {"role": "user", "content": question}
                    ],
                    temperature=0
                )
                return final_response.choices[0].message.content
            else:
                # If no context was found, return the fallback message
                return "Is sawal ka jawab provided data me mojood nahi hai."

        except Exception as e:
            logger.error(f"Error in RAG query: {str(e)}")
            # Check if the error is related to API key validity
            error_str = str(e).lower()
            if "api key" in error_str or "quota" in error_str or "billing" in error_str or "permission" in error_str or "401" in str(e) or "403" in str(e):
                # Return a more specific message about API configuration
                return f"I'm currently unable to process your request about '{question}'. The AI service may be temporarily unavailable due to API key issues or quota limits. Please check that your OPENROUTER_API_KEY is properly configured in the .env file and has sufficient quota available."
            else:
                # Return a general fallback response
                return f"I apologize, but I'm currently unable to process your request about '{question}'. The AI service may be temporarily unavailable. Please try again later or contact support if the issue persists."

    def index_content(self, content_id: str, content: str, metadata: Dict[str, Any] = None):
        """Index textbook content for RAG retrieval"""
        if metadata is None:
            metadata = {}

        # Get embeddings for the content
        embeddings = self.get_embedding(content)

        # Store in vector database
        self.qdrant.upsert(
            collection_name=self.collection_name,
            points=[
                {
                    "id": content_id,
                    "vector": embeddings,
                    "payload": {
                        "content": content,
                        "metadata": metadata
                    }
                }
            ]
        )

        logger.info(f"Indexed content: {content_id}")