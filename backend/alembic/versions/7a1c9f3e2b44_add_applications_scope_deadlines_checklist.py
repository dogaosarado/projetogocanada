"""add applications table, scope deadlines/checklist to application

Revision ID: 7a1c9f3e2b44
Revises: d4c69dc88133
Create Date: 2026-07-25 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7a1c9f3e2b44'
down_revision: Union[str, Sequence[str], None] = 'd4c69dc88133'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'applications',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('request_id', sa.Integer(), nullable=False),
        sa.Column('university', sa.String(length=255), nullable=False),
        sa.Column('department', sa.String(length=255), nullable=False),
        sa.Column('url', sa.String(length=500), nullable=True),
        sa.Column('is_custom', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['request_id'], ['requests.id'], ),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_applications_user_id'), 'applications', ['user_id'], unique=False)

    op.add_column('deadlines', sa.Column('application_id', sa.Integer(), nullable=True))
    op.create_foreign_key(
        'fk_deadlines_application_id', 'deadlines', 'applications', ['application_id'], ['id']
    )

    op.add_column('checklist_progress', sa.Column('application_id', sa.Integer(), nullable=True))
    op.create_foreign_key(
        'fk_checklist_progress_application_id', 'checklist_progress', 'applications', ['application_id'], ['id']
    )
    op.drop_constraint('uq_user_checklist_item', 'checklist_progress', type_='unique')
    op.create_unique_constraint(
        'uq_application_checklist_item', 'checklist_progress', ['application_id', 'item_key']
    )

    # backfill: um Application por item de universities_selected em cada request existente
    op.execute("""
        INSERT INTO applications (user_id, request_id, university, department, url, is_custom, created_at)
        SELECT r.user_id, r.id,
               elem->>'university',
               elem->>'department',
               elem->>'url',
               COALESCE((elem->>'is_custom')::boolean, false),
               r.created_at
        FROM requests r,
             jsonb_array_elements(r.universities_selected) elem
    """)
    # nota: deadlines e checklist_progress criados ANTES desta migration ficam com
    # application_id NULL (não há como saber a qual universidade se referiam) —
    # precisam ser reatribuídos manualmente pelo admin se ainda forem relevantes.


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('uq_application_checklist_item', 'checklist_progress', type_='unique')
    op.create_unique_constraint('uq_user_checklist_item', 'checklist_progress', ['user_id', 'item_key'])
    op.drop_constraint('fk_checklist_progress_application_id', 'checklist_progress', type_='foreignkey')
    op.drop_column('checklist_progress', 'application_id')

    op.drop_constraint('fk_deadlines_application_id', 'deadlines', type_='foreignkey')
    op.drop_column('deadlines', 'application_id')

    op.drop_index(op.f('ix_applications_user_id'), table_name='applications')
    op.drop_table('applications')
