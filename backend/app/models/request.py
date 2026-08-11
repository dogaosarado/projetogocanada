import enum

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class ConsultancyRequest(Base):
    __tablename__ = "requests"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    tier: Mapped[str] = mapped_column(String(50), nullable=False)
    service_type: Mapped[str] = mapped_column(String(50), nullable=False)
    universities_selected: Mapped[list] = mapped_column(JSONB, nullable=False)
    research_interests: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class Application(Base):
    """Uma candidatura individual (uma universidade/programa) derivada de um ConsultancyRequest.
    Cada item de `universities_selected` vira uma linha aqui, o que permite ter
    prazos e checklist de documentos por candidatura em vez de por usuário."""

    __tablename__ = "applications"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    request_id: Mapped[int] = mapped_column(ForeignKey("requests.id"), nullable=False)
    university: Mapped[str] = mapped_column(String(255), nullable=False)
    department: Mapped[str] = mapped_column(String(255), nullable=False)
    url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    is_custom: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )