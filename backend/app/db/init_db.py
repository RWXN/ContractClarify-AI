from sqlalchemy import text
from sqlalchemy.orm import Session


def enable_pgvector_extension(db: Session) -> None:
    db.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
    db.commit()