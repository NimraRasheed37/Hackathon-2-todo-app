"""Create notifications table

Revision ID: 006
Revises: 005
Create Date: 2026-02-05

This migration creates the notifications table for storing
in-app notifications to users (reminders, system messages, etc).
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '006'
down_revision: Union[str, None] = '005'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'notifications',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('type', sa.String(50), nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('message', sa.Text(), nullable=True),
        sa.Column('reference_type', sa.String(50), nullable=True),
        sa.Column('reference_id', sa.Integer(), nullable=True),
        sa.Column('read', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    # Index for fetching user's unread notifications (most recent first)
    op.execute("""
        CREATE INDEX idx_notifications_user_unread
        ON notifications(user_id, created_at DESC)
        WHERE read = false
    """)

    # Index for fetching all user notifications
    op.create_index('idx_notifications_user_id', 'notifications', ['user_id', 'created_at'])

    # Check constraint for notification type
    op.execute("""
        ALTER TABLE notifications ADD CONSTRAINT chk_notification_type
        CHECK (type IN ('reminder', 'task_due', 'task_overdue', 'recurring_created', 'system'))
    """)


def downgrade() -> None:
    op.execute("ALTER TABLE notifications DROP CONSTRAINT IF EXISTS chk_notification_type")
    op.drop_index('idx_notifications_user_id', table_name='notifications')
    op.execute("DROP INDEX IF EXISTS idx_notifications_user_unread")
    op.drop_table('notifications')
