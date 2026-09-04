import logging

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.document import DocumentListResponse, DocumentRead
from app.services.document_service import (
    create_document_record,
    get_user_document_by_id,
    get_user_documents,
    save_uploaded_file,
    validate_upload_file,
)

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)


@router.post("/upload", response_model=DocumentRead, status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    logger.info(
        "Document upload started: user_id=%s filename=%s content_type=%s",
        current_user.id,
        file.filename,
        file.content_type
    )

    file_bytes = await file.read()

    file_type = validate_upload_file(
        file=file,
        file_bytes=file_bytes
    )

    stored_filename, file_path = save_uploaded_file(
        file=file,
        file_bytes=file_bytes,
        owner_id=current_user.id
    )

    document = create_document_record(
        db=db,
        current_user=current_user,
        file=file,
        file_bytes=file_bytes,
        file_type=file_type,
        stored_filename=stored_filename,
        file_path=file_path
    )

    logger.info(
        "Document upload completed: user_id=%s document_id=%s filename=%s",
        current_user.id,
        document.id,
        document.filename
    )

    return document


@router.get("", response_model=DocumentListResponse)
def list_documents(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    documents = get_user_documents(
        db=db,
        current_user=current_user
    )

    return DocumentListResponse(documents=documents)


@router.get("/{document_id}", response_model=DocumentRead)
def get_document(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    document = get_user_document_by_id(
        db=db,
        current_user=current_user,
        document_id=document_id
    )

    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )

    return document