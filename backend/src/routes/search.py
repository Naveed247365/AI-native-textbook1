"""
Search API routes for the AI Backend with RAG + Authentication
Implements search functionality with RAG integration
"""
from fastapi import APIRouter, HTTPException, status, Depends
import logging
from typing import Optional, List, Dict, Any
from uuid import UUID

from ..auth.auth import get_current_user
from ..models.search import SearchRequest, SearchResponse, ChatRequest, ChatResponse
from ..rag.pipeline import query_rag, search_documents
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/search", tags=["search"])

logger = logging.getLogger(__name__)


@router.post("/", response_model=SearchResponse)
async def search(
    search_request: SearchRequest,
    current_user: TokenData = Depends(get_current_user)
):
    """
    Perform similarity search with user isolation
    """
    try:
        # Validate search request
        if not search_request.query or not search_request.query.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Search query is required"
            )

        # Set default values
        top_k = search_request.top_k or 5
        if top_k > 20:  # Limit maximum results for performance
            top_k = 20

        # Perform search with user isolation
        search_results = await search_documents(
            query=search_request.query,
            user_id=UUID(current_user.user_id),
            top_k=top_k
        )

        if search_results is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Search failed"
            )

        # Format results
        formatted_results = []
        for result in search_results:
            formatted_results.append({
                "id": result["id"],
                "document_id": result["document_id"],
                "score": result["score"],
                "payload": result["payload"]
            })

        logger.info(f"Search completed for user {current_user.user_id}, found {len(formatted_results)} results")

        return SearchResponse(
            results=formatted_results,
            query=search_request.query,
            total_results=len(formatted_results)
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in search endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during search"
        )


@router.post("/chat", response_model=ChatResponse)
async def chat(
    chat_request: ChatRequest,
    current_user: TokenData = Depends(get_current_user)
):
    """
    Chat endpoint that combines search and response generation
    """
    try:
        # Validate chat request
        if not chat_request.query or not chat_request.query.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Chat query is required"
            )

        # Set default values
        top_k = chat_request.top_k or 5
        if top_k > 10:  # Limit maximum context for performance
            top_k = 10

        # Execute RAG pipeline
        rag_result = await query_rag(
            query=chat_request.query,
            user_id=UUID(current_user.user_id),
            top_k=top_k,
            conversation_history=chat_request.conversation_history
        )

        if not rag_result:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Chat generation failed"
            )

        logger.info(f"Chat completed for user {current_user.user_id}")

        return ChatResponse(
            response=rag_result["response"],
            sources=rag_result["sources"],
            context_used=rag_result["context_used"]
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during chat generation"
        )