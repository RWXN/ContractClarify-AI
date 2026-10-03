from sqlalchemy.orm import Session

from app.models.document_chunk import DocumentChunk


def create_document_chunks(
    db: Session,
    document_id: int,
    chunks: list[dict]
) -> list[DocumentChunk]:
    chunk_records = []

    for chunk in chunks:
        chunk_record = DocumentChunk(
            document_id=document_id,
            chunk_index=chunk["chunk_index"],
            page_number=chunk["page_number"],
            content=chunk["content"],
            token_count_estimate=chunk["token_count_estimate"],
            embedding=None
        )

        chunk_records.append(chunk_record)

    db.add_all(chunk_records)
    db.commit()

    for chunk_record in chunk_records:
        db.refresh(chunk_record)

    return chunk_records


def get_chunks_by_document_id(
    db: Session,
    document_id: int
) -> list[DocumentChunk]:
    return (
        db.query(DocumentChunk)
        .filter(DocumentChunk.document_id == document_id)
        .order_by(DocumentChunk.chunk_index.asc())
        .all()
    )


def delete_chunks_by_document_id(
    db: Session,
    document_id: int
) -> None:
    (
        db.query(DocumentChunk)
        .filter(DocumentChunk.document_id == document_id)
        .delete()
    )

    db.commit()