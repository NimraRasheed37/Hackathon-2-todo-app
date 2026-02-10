"""Create task_tags junction table

Revision ID: 003
Revises: 002
Create Date: 2026-02-05

This migration creates the task_tags junction table for the
many-to-many relationship between tasks and tags.
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '003'
down_revision: Union[str, None] = '002'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'task_tags',
        sa.Column('task_id', sa.Integer(), nullable=False),
        sa.Column('tag_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        # Composite primary key
        sa.PrimaryKeyConstraint('task_id', 'tag_id', name='pk_task_tags'),
        # Foreign keys with CASCADE delete
        sa.ForeignKeyConstraint(['task_id'], ['tasks.id'], name='fk_task_tags_task_id', ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], name='fk_task_tags_tag_id', ondelete='CASCADE'),
    )

    # Index for lookups by tag_id (task_id is covered by PK)
    op.create_index('idx_task_tags_tag_id', 'task_tags', ['tag_id'])


def downgrade() -> None:
    op.drop_index('idx_task_tags_tag_id', table_name='task_tags')
    op.drop_table('task_tags')
