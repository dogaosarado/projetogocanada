"""departments as jsonb with url

Revision ID: 415d80cc6a2b
Revises: d19dcd7180e6
Create Date: 2026-06-06 23:09:30.172707

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '415d80cc6a2b'
down_revision: Union[str, Sequence[str], None] = 'd19dcd7180e6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        ALTER TABLE universities 
        ALTER COLUMN departments TYPE JSONB 
        USING to_jsonb(departments)
    """)


def downgrade() -> None:
    op.execute("""
        ALTER TABLE universities 
        ALTER COLUMN departments TYPE VARCHAR[] 
        USING ARRAY(SELECT jsonb_array_elements_text(departments))
    """)
    # ### end Alembic commands ###
