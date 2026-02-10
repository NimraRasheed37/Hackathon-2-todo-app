"""Add Phase 5 indexes

Revision ID: 009
Revises: 008
Create Date: 2026-02-05

This migration adds optimized indexes for Phase 5 features:
- Priority filtering
- Due date queries
- Parent task lookups
- Full-text search GIN index
- Composite user+status index
"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '009'
down_revision: Union[str, None] = '008'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Index for filtering by priority
    op.create_index('idx_tasks_priority', 'tasks', ['priority'])

    # Index for due date queries (upcoming tasks, overdue, etc.)
    op.create_index('idx_tasks_due_date', 'tasks', ['due_date'])

    # Index for parent task lookups (recurring task instances)
    op.create_index('idx_tasks_parent_task_id', 'tasks', ['parent_task_id'])

    # GIN index for full-text search on search_vector
    op.execute("""
        CREATE INDEX idx_tasks_search_vector
        ON tasks USING GIN(search_vector)
    """)

    # Composite index for user + completed status (common query pattern)
    op.create_index('idx_tasks_user_completed', 'tasks', ['user_id', 'completed'])

    # Composite index for user + priority (for sorted lists)
    op.create_index('idx_tasks_user_priority', 'tasks', ['user_id', 'priority'])

    # Composite index for user + due_date (for calendar views)
    op.create_index('idx_tasks_user_due_date', 'tasks', ['user_id', 'due_date'])

    # Partial index for active (non-completed) tasks with due dates
    op.execute("""
        CREATE INDEX idx_tasks_active_due
        ON tasks(user_id, due_date)
        WHERE completed = false AND due_date IS NOT NULL
    """)


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS idx_tasks_active_due")
    op.drop_index('idx_tasks_user_due_date', table_name='tasks')
    op.drop_index('idx_tasks_user_priority', table_name='tasks')
    op.drop_index('idx_tasks_user_completed', table_name='tasks')
    op.execute("DROP INDEX IF EXISTS idx_tasks_search_vector")
    op.drop_index('idx_tasks_parent_task_id', table_name='tasks')
    op.drop_index('idx_tasks_due_date', table_name='tasks')
    op.drop_index('idx_tasks_priority', table_name='tasks')
