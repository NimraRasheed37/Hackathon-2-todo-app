"""Create task_recurrences table

Revision ID: 004
Revises: 003
Create Date: 2026-02-05

This migration creates the task_recurrences table for tracking
active recurrence patterns and scheduling next occurrences.
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '004'
down_revision: Union[str, None] = '003'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'task_recurrences',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('task_id', sa.Integer(), nullable=False),
        sa.Column('pattern', postgresql.JSONB, nullable=False),
        sa.Column('next_occurrence', sa.DateTime(timezone=True), nullable=True),
        sa.Column('last_generated', sa.DateTime(timezone=True), nullable=True),
        sa.Column('total_occurrences', sa.Integer(), server_default='0', nullable=False),
        sa.Column('is_active', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        # Foreign key to tasks
        sa.ForeignKeyConstraint(['task_id'], ['tasks.id'], name='fk_task_recurrences_task_id', ondelete='CASCADE'),
    )

    # Index for finding due recurrences (only active ones)
    op.execute("""
        CREATE INDEX idx_recurrences_next_active
        ON task_recurrences(next_occurrence)
        WHERE is_active = true
    """)

    # Index for task lookup
    op.create_index('idx_recurrences_task_id', 'task_recurrences', ['task_id'])


def downgrade() -> None:
    op.drop_index('idx_recurrences_task_id', table_name='task_recurrences')
    op.execute("DROP INDEX IF EXISTS idx_recurrences_next_active")
    op.drop_table('task_recurrences')
