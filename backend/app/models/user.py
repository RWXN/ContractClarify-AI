from datetime import datetime,timezone

from sqlalchemy import DateTime, Boolean, String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False
    )

    hashed_password: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    full_name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )
    
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now(timezone.utc),    #2026-08-07 04:54:49.971462+00:00 world time not sydney time
        nullable=False
    )

    
