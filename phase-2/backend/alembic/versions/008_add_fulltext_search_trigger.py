"""Add full-text search trigger

Revision ID: 008
Revises: 007
Create Date: 2026-02-05

This migration creates the PostgreSQL trigger function for automatically
updating the search_vector column when task title or description changes.
Also populates existing tasks with search vectors.
"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '008'
down_revision: Union[str, None] = '007'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create the trigger function for updating search_vector
    op.execute("""
        CREATE OR REPLACE FUNCTION update_task_search_vector()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.search_vector := to_tsvector('english',
                COALESCE(NEW.title, '') || ' ' ||
                COALESCE(NEW.description, '')
            );
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """)

    # Create the trigger on tasks table
    op.execute("""
        CREATE TRIGGER task_search_vector_update
        BEFORE INSERT OR UPDATE OF title, description ON tasks
        FOR EACH ROW
        EXECUTE FUNCTION update_task_search_vector();
    """)

    # Populate search_vector for existing tasks
    op.execute("""
        UPDATE tasks
        SET search_vector = to_tsvector('english',
            COALESCE(title, '') || ' ' ||
            COALESCE(description, '')
        );
    """)


def downgrade() -> None:
    # Drop the trigger
    op.execute("DROP TRIGGER IF EXISTS task_search_vector_update ON tasks")

    # Drop the trigger function
    op.execute("DROP FUNCTION IF EXISTS update_task_search_vector()")

    # Clear the search vectors (optional, column will be dropped in migration 001)
    op.execute("UPDATE tasks SET search_vector = NULL")
