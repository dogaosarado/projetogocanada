"""split tier enum and add is_admin

Revision ID: 0f705cf550bc
Revises: 6fa6d4a26003
Create Date: 2026-07-30 19:02:51.999320

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0f705cf550bc'
down_revision: Union[str, Sequence[str], None] = '6fa6d4a26003'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute("ALTER TYPE tierenum RENAME VALUE 'basico' TO 'relatorio_basico'")
    op.execute("ALTER TYPE tierenum RENAME VALUE 'intermediario' TO 'relatorio_intermediario'")
    op.execute("ALTER TYPE tierenum RENAME VALUE 'avancado' TO 'relatorio_avancado'")
    op.execute("ALTER TYPE tierenum ADD VALUE IF NOT EXISTS 'relatorio_gratis'")
    op.execute("ALTER TYPE tierenum ADD VALUE IF NOT EXISTS 'mentoria_basico'")
    op.execute("ALTER TYPE tierenum ADD VALUE IF NOT EXISTS 'mentoria_intermediario'")
    op.execute("ALTER TYPE tierenum ADD VALUE IF NOT EXISTS 'mentoria_avancado'")
    op.add_column("users", sa.Column("is_admin", sa.Boolean(), nullable=False, server_default="false"))


def downgrade():
    op.drop_column("users", "is_admin")
    op.execute("ALTER TYPE tierenum RENAME VALUE 'relatorio_basico' TO 'basico'")
    op.execute("ALTER TYPE tierenum RENAME VALUE 'relatorio_intermediario' TO 'intermediario'")
    op.execute("ALTER TYPE tierenum RENAME VALUE 'relatorio_avancado' TO 'avancado'")