"""
Chat History API routes for the AI Backend with RAG + Authentication
Implements chat history storage and retrieval with user isolation
"""
from fastapi import APIRouter, HTTPException, status, Depends
import logging
from typing import Optional, List
from uuid import UUID

from ..auth.auth import get_current_user
from ..models.history import HistoryResponse, HistoryEntry
from ..config.database import get_db_session
from ..db import crud
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/history", tags=["history"])

logger = logging.getLogger(__name__)


@router.get("/", response_model=HistoryResponse)
async def get_chat_history(
    skip: int = 0,
    limit: int = 20,
    current_user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Retrieve chat history for the current user with pagination
    """
    try:
        # Validate parameters
        if skip < 0:
            skip = 0
        if limit < 1 or limit > 100:  # Set reasonable limits
            limit = 20

        # Get user's chat history from database with pagination
        chat_histories = await crud.get_chat_histories_by_user(
            db,
            user_id=UUID(current_user.user_id),
            skip=skip,
            limit=limit
        )

        # Get total count for pagination info
        total_count = await crud.get_user_chat_history_count(db, UUID(current_user.user_id))

        # Format the history entries
        history_entries = []
        for chat_history in chat_histories:
            history_entries.append(HistoryEntry(
                id=str(chat_history.id),
                query=chat_history.query,
                response=chat_history.response,
                context_used=chat_history.context_used,
                timestamp=chat_history.created_at
            ))

        logger.info(f"Retrieved {len(history_entries)} chat history items for user {current_user.user_id}")

        return HistoryResponse(
            history=history_entries,
            total=total_count,
            skip=skip,
            limit=limit
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving chat history: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving chat history"
        )


@router.get("/{conversation_id}")
async def get_conversation_detail(
    conversation_id: str,
    current_user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Get specific conversation details
    """
    try:
        # Validate conversation ID
        try:
            conv_uuid = UUID(conversation_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid conversation ID format"
            )

        # Get the specific chat history
        chat_history = await crud.get_chat_history_by_id(db, conv_uuid)

        if not chat_history:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )

        # Verify that the conversation belongs to the current user
        if str(chat_history.user_id) != current_user.user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: You don't have permission to access this conversation"
            )

        logger.info(f"Retrieved conversation {conversation_id} for user {current_user.user_id}")

        return HistoryEntry(
            id=str(chat_history.id),
            query=chat_history.query,
            response=chat_history.response,
            context_used=chat_history.context_used,
            timestamp=chat_history.created_at
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving conversation detail: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving conversation"
        )


@router.delete("/{conversation_id}")
async def delete_conversation(
    conversation_id: str,
    current_user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Delete a specific conversation
    """
    try:
        # Validate conversation ID
        try:
            conv_uuid = UUID(conversation_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid conversation ID format"
            )

        # Get chat history record to verify it exists and belongs to user
        chat_history = await crud.get_chat_history_by_id(db, conv_uuid)

        if not chat_history:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )

        # Check if conversation belongs to current user
        if str(chat_history.user_id) != current_user.user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: Conversation does not belong to current user"
            )

        # Delete the conversation
        success = await crud.delete_chat_history(db, conv_uuid)

        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete conversation"
            )

        logger.info(f"Conversation {conversation_id} deleted for user {current_user.user_id}")

        return {
            "success": True,
            "message": f"Conversation {conversation_id} deleted successfully"
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting conversation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while deleting conversation"
        )


@router.delete("/")
async def delete_all_user_history(
    current_user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Delete all chat history for the current user
    """
    try:
        # Delete all chat history for the user
        success = await crud.delete_user_chat_histories(db, UUID(current_user.user_id))

        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete chat history"
            )

        logger.info(f"All chat history deleted for user {current_user.user_id}")

        return {
            "success": True,
            "message": "All chat history deleted successfully"
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting all chat history: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while deleting chat history"
        )