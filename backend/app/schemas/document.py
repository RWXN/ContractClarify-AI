from datetime import datetime

from pydantic import BaseModel


class DocumentRead(BaseModel):
    id: int
    owner_id: int
    filename: str
    stored_filename: str
    file_path: str
    file_type: str
    file_size: int
    status: str
    extracted_text_preview: str | None
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


class DocumentListResponse(BaseModel):
    documents: list[DocumentRead]


class DocumentChunkRead(BaseModel):
    id: int
    document_id: int
    chunk_index: int
    page_number: int | None
    content: str
    token_count_estimate: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


class DocumentChunksResponse(BaseModel):
    document_id: int
    chunks: list[DocumentChunkRead]