"""split tier enum and add is_admin

Revision ID: 6fa6d4a26003
Revises: 7a1c9f3e2b44
Create Date: 2026-07-30 18:51:53.925087

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6fa6d4a26003'
down_revision: Union[str, Sequence[str], None] = '7a1c9f3e2b44'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
