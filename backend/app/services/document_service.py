from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.models.document import Document
from app.models.user import User

MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024

ALLOWED_CONTENT_TYPES = {
    "application/pdf": "pdf",
    "text/plain": "txt"
}

ALLOWED_EXTENSIONS = {
    ".pdf",
    ".txt"
}

UPLOAD_DIR = Path("storage/uploads")


def validate_upload_file(file: UploadFile, file_bytes: bytes) -> str:
    original_filename = file.filename or ""

    suffix = Path(original_filename).suffix.lower()

    if suffix not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF and TXT files are allowed"
        )

    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file content type"
        )

    if len(file_bytes) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="File size must be less than 10MB"
        )

    return ALLOWED_CONTENT_TYPES[file.content_type]


def save_uploaded_file(file: UploadFile, file_bytes: bytes, owner_id: int) -> tuple[str, str]:
    original_filename = file.filename or "uploaded_file"
    suffix = Path(original_filename).suffix.lower()

    user_upload_dir = UPLOAD_DIR / str(owner_id)
    user_upload_dir.mkdir(parents=True, exist_ok=True)

    stored_filename = f"{uuid4()}{suffix}"
    file_path = user_upload_dir / stored_filename

    file_path.write_bytes(file_bytes)

    return stored_filename, str(file_path)


def create_document_record(
    db: Session,
    current_user: User,
    file: UploadFile,
    file_bytes: bytes,
    file_type: str,
    stored_filename: str,
    file_path: str
) -> Document:
    document = Document(
        owner_id=current_user.id,
        filename=file.filename or "uploaded_file",
        stored_filename=stored_filename,
        file_path=file_path,
        file_type=file_type,
        file_size=len(file_bytes),
        status="uploaded"
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return document


def get_user_documents(db: Session, current_user: User) -> list[Document]:
    return (
        db.query(Document)
        .filter(Document.owner_id == current_user.id)
        .order_by(Document.created_at.desc())
        .all()
    )


def get_user_document_by_id(
    db: Session,
    current_user: User,
    document_id: int
) -> Document | None:
    return (
        db.query(Document)
        .filter(Document.id == document_id)
        .filter(Document.owner_id == current_user.id)
        .first()
    )