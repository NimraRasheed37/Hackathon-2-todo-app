"""Create tags table

Revision ID: 002
Revises: 001
Create Date: 2026-02-05

This migration creates the tags table for user-defined labels.
Tags support custom colors and icons for visual organization.
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '002'
down_revision: Union[str, None] = '001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'tags',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('color', sa.String(7), server_default='#808080', nullable=False),
        sa.Column('icon', sa.String(10), nullable=True),
        sa.Column('usage_count', sa.Integer(), server_default='0', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        # Unique constraint on user_id + name
        sa.UniqueConstraint('user_id', 'name', name='uq_tags_user_name'),
    )

    # Create index on user_id for fast lookups
    op.create_index('idx_tags_user_id', 'tags', ['user_id'])

    # Add check constraint for valid hex color
    op.execute("""
        ALTER TABLE tags ADD CONSTRAINT chk_tags_color
        CHECK (color ~ '^#[0-9A-Fa-f]{6}$')
    """)


def downgrade() -> None:
    op.execute("ALTER TABLE tags DROP CONSTRAINT IF EXISTS chk_tags_color")
    op.drop_index('idx_tags_user_id', table_name='tags')
    op.drop_table('tags')
