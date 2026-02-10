"""Create audit_log table

Revision ID: 007
Revises: 006
Create Date: 2026-02-05

This migration creates the audit_log table for event sourcing,
storing all task-related events for auditing and replay capability.
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '007'
down_revision: Union[str, None] = '006'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'audit_log',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('event_id', sa.String(36), nullable=False, unique=True),
        sa.Column('event_type', sa.String(100), nullable=False),
        sa.Column('event_version', sa.String(10), server_default='1.0', nullable=False),
        sa.Column('aggregate_type', sa.String(50), nullable=False),
        sa.Column('aggregate_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=True),
        sa.Column('correlation_id', sa.String(36), nullable=True),
        sa.Column('payload', postgresql.JSONB, nullable=False),
        sa.Column('metadata', postgresql.JSONB, nullable=True),
        sa.Column('timestamp', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    # Index for querying by aggregate (e.g., all events for a task)
    op.create_index('idx_audit_aggregate', 'audit_log', ['aggregate_type', 'aggregate_id'])

    # Index for querying by user
    op.create_index('idx_audit_user_id', 'audit_log', ['user_id'])

    # Index for querying by timestamp (most recent first)
    op.create_index('idx_audit_timestamp', 'audit_log', ['timestamp'])

    # Index for querying by event type
    op.create_index('idx_audit_event_type', 'audit_log', ['event_type'])

    # Index for correlation lookup
    op.create_index('idx_audit_correlation', 'audit_log', ['correlation_id'])


def downgrade() -> None:
    op.drop_index('idx_audit_correlation', table_name='audit_log')
    op.drop_index('idx_audit_event_type', table_name='audit_log')
    op.drop_index('idx_audit_timestamp', table_name='audit_log')
    op.drop_index('idx_audit_user_id', table_name='audit_log')
    op.drop_index('idx_audit_aggregate', table_name='audit_log')
    op.drop_table('audit_log')
