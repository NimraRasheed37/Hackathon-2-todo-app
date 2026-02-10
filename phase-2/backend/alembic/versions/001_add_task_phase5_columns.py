"""Add Phase 5 columns to tasks table

Revision ID: 001
Revises:
Create Date: 2026-02-05

This migration adds new columns to the tasks table for Phase 5 features:
- priority: Task priority level (none, low, medium, high, critical)
- due_date: When the task is due
- recurrence_pattern: JSONB for recurring task configuration
- parent_task_id: Reference to parent task for recurring instances
- occurrence_number: Instance number in a recurring series
- search_vector: tsvector for full-text search
- version: Optimistic locking version number
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add priority column with constraint
    op.add_column('tasks', sa.Column('priority', sa.String(20), server_default='none', nullable=False))

    # Add due_date column
    op.add_column('tasks', sa.Column('due_date', sa.DateTime(timezone=True), nullable=True))

    # Add recurrence_pattern as JSONB
    op.add_column('tasks', sa.Column('recurrence_pattern', postgresql.JSONB, nullable=True))

    # Add parent_task_id for recurring task instances (self-referential FK)
    op.add_column('tasks', sa.Column('parent_task_id', sa.Integer(), nullable=True))
    op.create_foreign_key(
        'fk_tasks_parent_task_id',
        'tasks', 'tasks',
        ['parent_task_id'], ['id'],
        ondelete='SET NULL'
    )

    # Add occurrence_number for recurring tasks
    op.add_column('tasks', sa.Column('occurrence_number', sa.Integer(), server_default='1', nullable=False))

    # Add search_vector for full-text search
    op.add_column('tasks', sa.Column('search_vector', postgresql.TSVECTOR, nullable=True))

    # Add version for optimistic locking
    op.add_column('tasks', sa.Column('version', sa.Integer(), server_default='1', nullable=False))

    # Add check constraint for priority values
    op.execute("""
        ALTER TABLE tasks ADD CONSTRAINT chk_task_priority
        CHECK (priority IN ('none', 'low', 'medium', 'high', 'critical'))
    """)


def downgrade() -> None:
    # Drop constraint first
    op.execute("ALTER TABLE tasks DROP CONSTRAINT IF EXISTS chk_task_priority")

    # Drop foreign key
    op.drop_constraint('fk_tasks_parent_task_id', 'tasks', type_='foreignkey')

    # Drop columns in reverse order
    op.drop_column('tasks', 'version')
    op.drop_column('tasks', 'search_vector')
    op.drop_column('tasks', 'occurrence_number')
    op.drop_column('tasks', 'parent_task_id')
    op.drop_column('tasks', 'recurrence_pattern')
    op.drop_column('tasks', 'due_date')
    op.drop_column('tasks', 'priority')
