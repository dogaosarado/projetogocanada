"""drop leads table

Revision ID: ef56ff9dfdca
Revises: 3cdc0f62c3d3
Create Date: 2026-08-10 13:53:38.790691

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ef56ff9dfdca'
down_revision: Union[str, Sequence[str], None] = '3cdc0f62c3d3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('requests', sa.Column('service_type', sa.String(length=50), nullable=False, server_default='relatorio'))

def downgrade() -> None:
    op.drop_column('requests', 'service_type')
