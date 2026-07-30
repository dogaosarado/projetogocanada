# app/models/user.py

import enum
from typing import Optional

from sqlalchemy import Boolean, DateTime, Enum, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class TierEnum(str, enum.Enum):
    # Relatório (produto avulso)
    relatorio_gratis = "relatorio_gratis"
    relatorio_basico = "relatorio_basico"
    relatorio_intermediario = "relatorio_intermediario"
    relatorio_avancado = "relatorio_avancado"
    # Mentoria (produto separado)
    mentoria_basico = "mentoria_basico"
    mentoria_intermediario = "mentoria_intermediario"
    mentoria_avancado = "mentoria_avancado"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    tier: Mapped[TierEnum] = mapped_column(Enum(TierEnum), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    # NOVO: o admin panel era gated por tier == "avancado" — hack que quebra
    # sozinho com o rename dos valores do enum, mentoria ou não. Campo
    # explícito, não sobrecarrega mais o tier de compra pra dizer quem é admin.
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
