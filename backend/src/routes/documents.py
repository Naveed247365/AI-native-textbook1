"""
Document Management API routes for the AI Backend with RAG + Authentication
Implements document upload, storage, and management with user isolation
"""
from fastapi import APIRouter, HTTPException, status, Depends, UploadFile, File
import logging
from typing import Optional
from uuid import UUID
import hashlib
from datetime import datetime

from ..auth.auth import get_current_user
from ..models.documents import DocumentResponse, DocumentUploadResponse
from ..config.database import get_db_session
from ..db import crud
from ..models.auth import TokenData
from sqlalchemy.ext.asyncio import AsyncSession
from ..embeddings.processor import process_document_for_rag
from ..qdrant.operations import VectorOperations

router = APIRouter(prefix="/documents", tags=["documents"])

logger = logging.getLogger(__name__)


@router.post("/", response_model=DocumentUploadResponse)
async def save_document(
    title: str,
    content: str,
    current_user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Save a document with user isolation
    """
    try:
        # Validate input
        if not title or not title.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Document title is required"
            )

        if not content or not content.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Document content is required"
            )

        # Create content hash for deduplication
        content_hash = hashlib.sha256(content.encode()).hexdigest()

        # Check if document with same content already exists for this user
        existing_document = await crud.get_document_by_content_hash_and_user(
            db,
            content_hash=content_hash,
            user_id=UUID(current_user.user_id)
        )

        if existing_document:
            logger.info(f"Document with same content already exists for user {current_user.user_id}")
            return DocumentResponse(
                document_id=str(existing_document.id),
                success=True,
                message="Document already exists with identical content"
            )

        # Create document record in database
        db_document = await crud.create_document(
            db,
            user_id=UUID(current_user.user_id),
            title=title,
            content=content,
            content_hash=content_hash
        )

        # Process document for RAG (generate embeddings and store in Qdrant)
        success = await process_document_for_rag(
            document_id=db_document.id,
            user_id=UUID(current_user.user_id),
            content=content,
            title=title
        )

        if not success:
            logger.error(f"Failed to process document {db_document.id} for RAG")
            # We still return success since the document was saved to DB,
            # but we log the RAG processing failure
            return DocumentUploadResponse(
                document_id=str(db_document.id),
                success=True,
                message="Document saved to database but failed to process for RAG"
            )

        logger.info(f"Document {db_document.id} saved and processed successfully for user {current_user.user_id}")
        return DocumentUploadResponse(
            document_id=str(db_document.id),
            success=True,
            message="Document saved and processed successfully"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error saving document: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while saving the document"
        )


@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    current_user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Upload a document file with user isolation
    """
    try:
        # Validate file
        if not file.filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Filename is required"
            )

        # Check file type (allow only text-based files for now)
        allowed_extensions = {'.txt', '.pdf', '.docx', '.md', '.csv'}
        file_extension = '.' + file.filename.lower().split('.')[-1] if '.' in file.filename else ''

        if file_extension not in allowed_extensions:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File type not supported. Allowed types: {', '.join(allowed_extensions)}"
            )

        # Read file content
        content = await file.read()
        content_str = content.decode('utf-8')  # For text files

        # For other file types (PDF, DOCX), we would need specific parsers
        # This is a simplified implementation that assumes text files
        if file_extension in ['.pdf', '.docx']:
            content_str = f"Unsupported file type for direct parsing: {file_extension}. Content would need to be extracted using appropriate parser."

        title = file.filename.rsplit('.', 1)[0] if '.' in file.filename else file.filename

        # Create content hash for deduplication
        content_hash = hashlib.sha256(content_str.encode()).hexdigest()

        # Check if document with same content already exists for this user
        existing_document = await crud.get_document_by_content_hash_and_user(
            db,
            content_hash=content_hash,
            user_id=UUID(current_user.user_id)
        )

        if existing_document:
            logger.info(f"Document with same content already exists for user {current_user.user_id}")
            return DocumentResponse(
                document_id=str(existing_document.id),
                success=True,
                message="Document already exists with identical content"
            )

        # Create document record in database
        db_document = await crud.create_document(
            db,
            user_id=UUID(current_user.user_id),
            title=title,
            content=content_str,
            content_hash=content_hash,
            file_path=f"uploads/{current_user.user_id}/{file.filename}"
        )

        # Process document for RAG (generate embeddings and store in Qdrant)
        success = await process_document_for_rag(
            document_id=db_document.id,
            user_id=UUID(current_user.user_id),
            content=content_str,
            title=title
        )

        if not success:
            logger.error(f"Failed to process document {db_document.id} for RAG")
            # We still return success since the document was saved to DB,
            # but we log the RAG processing failure
            return DocumentUploadResponse(
                document_id=str(db_document.id),
                success=True,
                message="Document saved to database but failed to process for RAG"
            )

        logger.info(f"Document {db_document.id} uploaded and processed successfully for user {current_user.user_id}")
        return DocumentUploadResponse(
            document_id=str(db_document.id),
            success=True,
            message="Document uploaded and processed successfully"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading document: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while uploading the document"
        )


@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: str,
    current_user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Get a specific document by ID with user isolation
    """
    try:
        # Validate document ID
        try:
            doc_uuid = UUID(document_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid document ID format"
            )

        # Get document from database
        document = await crud.get_document_by_id(db, doc_uuid)

        if not document:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document not found"
            )

        # Verify that the document belongs to the current user
        if str(document.user_id) != current_user.user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: You don't have permission to access this document"
            )

        logger.info(f"Retrieved document {document_id} for user {current_user.user_id}")

        return DocumentResponse(
            document_id=str(document.id),
            title=document.title,
            content=document.content[:200] + "..." if len(document.content) > 200 else document.content,  # Truncate for security
            created_at=document.created_at,
            success=True,
            message="Document retrieved successfully"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving document: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving the document"
        )


@router.get("/")
async def list_documents(
    skip: int = 0,
    limit: int = 20,
    current_user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
):
    """
    List documents for the current user with pagination
    """
    try:
        # Validate parameters
        if skip < 0:
            skip = 0
        if limit < 1 or limit > 100:  # Set reasonable limits
            limit = 20

        # Get user's documents from database with pagination
        documents = await crud.get_documents_by_user(
            db,
            user_id=UUID(current_user.user_id),
            skip=skip,
            limit=limit
        )

        # Get total count for pagination info
        total_count = await crud.get_user_documents_count(db, UUID(current_user.user_id))

        # Format the documents (excluding full content for security)
        document_list = []
        for doc in documents:
            document_list.append({
                "id": str(doc.id),
                "title": doc.title,
                "created_at": doc.created_at,
                "updated_at": doc.updated_at
            })

        logger.info(f"Retrieved {len(document_list)} documents for user {current_user.user_id}")

        return {
            "documents": document_list,
            "total": total_count,
            "skip": skip,
            "limit": limit
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving documents: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving documents"
        )


@router.delete("/{document_id}")
async def delete_document(
    document_id: str,
    current_user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Delete a document with user isolation
    """
    try:
        # Validate document ID
        try:
            doc_uuid = UUID(document_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid document ID format"
            )

        # Get the document to verify it exists and belongs to user
        document = await crud.get_document_by_id(db, doc_uuid)

        if not document:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document not found"
            )

        # Verify that the document belongs to the current user
        if str(document.user_id) != current_user.user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: You don't have permission to delete this document"
            )

        # Delete the document from database
        success = await crud.delete_document(db, doc_uuid)

        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete document from database"
            )

        # Also delete associated vectors from Qdrant
        try:
            vector_ops = VectorOperations()
            await vector_ops.delete_vectors_by_user_and_document_id(
                user_id=UUID(current_user.user_id),
                document_id=doc_uuid
            )
            logger.info(f"Deleted associated vectors from Qdrant for document {document_id}")
        except Exception as e:
            logger.error(f"Error deleting vectors from Qdrant for document {document_id}: {e}")
            # Don't fail the operation if vector deletion fails

        logger.info(f"Deleted document {document_id} for user {current_user.user_id}")

        return {"message": "Document deleted successfully"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting document: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while deleting the document"
        )


# Health check endpoint
@router.get("/health")
async def documents_health():
    """
    Health check for documents service
    """
    return {"status": "healthy", "service": "Documents API"}