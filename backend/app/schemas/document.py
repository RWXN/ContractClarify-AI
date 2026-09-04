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