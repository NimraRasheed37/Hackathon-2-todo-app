"""Create task_reminders table

Revision ID: 005
Revises: 004
Create Date: 2026-02-05

This migration creates the task_reminders table for scheduled
task reminders supporting both relative (e.g., 15 min before due)
and absolute (specific datetime) reminder types.
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '005'
down_revision: Union[str, None] = '004'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'task_reminders',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('task_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('reminder_type', sa.String(20), nullable=False),
        sa.Column('relative_minutes', sa.Integer(), nullable=True),
        sa.Column('absolute_time', sa.DateTime(timezone=True), nullable=True),
        sa.Column('channels', postgresql.ARRAY(sa.String()), server_default='{in_app}', nullable=False),
        sa.Column('status', sa.String(20), server_default='pending', nullable=False),
        sa.Column('scheduled_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('sent_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        # Foreign keys
        sa.ForeignKeyConstraint(['task_id'], ['tasks.id'], name='fk_task_reminders_task_id', ondelete='CASCADE'),
    )

    # Check constraint for valid reminder type (relative requires minutes, absolute requires time)
    op.execute("""
        ALTER TABLE task_reminders ADD CONSTRAINT chk_reminder_type_valid
        CHECK (
            (reminder_type = 'relative' AND relative_minutes IS NOT NULL) OR
            (reminder_type = 'absolute' AND absolute_time IS NOT NULL)
        )
    """)

    # Check constraint for status values
    op.execute("""
        ALTER TABLE task_reminders ADD CONSTRAINT chk_reminder_status
        CHECK (status IN ('pending', 'sent', 'cancelled'))
    """)

    # Check constraint for reminder_type values
    op.execute("""
        ALTER TABLE task_reminders ADD CONSTRAINT chk_reminder_type_values
        CHECK (reminder_type IN ('relative', 'absolute'))
    """)

    # Index for finding pending reminders by scheduled time
    op.execute("""
        CREATE INDEX idx_reminders_scheduled_pending
        ON task_reminders(scheduled_at)
        WHERE status = 'pending'
    """)

    # Index for task lookup
    op.create_index('idx_reminders_task_id', 'task_reminders', ['task_id'])

    # Index for user lookup
    op.create_index('idx_reminders_user_id', 'task_reminders', ['user_id'])


def downgrade() -> None:
    op.drop_index('idx_reminders_user_id', table_name='task_reminders')
    op.drop_index('idx_reminders_task_id', table_name='task_reminders')
    op.execute("DROP INDEX IF EXISTS idx_reminders_scheduled_pending")
    op.execute("ALTER TABLE task_reminders DROP CONSTRAINT IF EXISTS chk_reminder_type_values")
    op.execute("ALTER TABLE task_reminders DROP CONSTRAINT IF EXISTS chk_reminder_status")
    op.execute("ALTER TABLE task_reminders DROP CONSTRAINT IF EXISTS chk_reminder_type_valid")
    op.drop_table('task_reminders')
