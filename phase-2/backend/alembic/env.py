"""Alembic environment configuration."""

import os
import sys
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool, create_engine

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import SQLModel models to get metadata
from sqlmodel import SQLModel

# Import all models to register them with SQLModel.metadata
from src.models.user import User  # noqa: F401
from src.models.task import Task  # noqa: F401
from src.models.conversation import Conversation  # noqa: F401
from src.models.message import Message  # noqa: F401

# Phase 5 models (will be added as we create them)
# from src.models.tag import Tag  # noqa: F401
# from src.models.task_tag import TaskTag  # noqa: F401
# from src.models.task_recurrence import TaskRecurrence  # noqa: F401
# from src.models.task_reminder import TaskReminder  # noqa: F401
# from src.models.notification import Notification  # noqa: F401
# from src.models.audit_log import AuditLog  # noqa: F401

# Alembic Config object
config = context.config

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Target metadata for autogenerate support
target_metadata = SQLModel.metadata

# Get database URL from environment
def get_url():
    """Get database URL from environment variable."""
    return os.getenv("DATABASE_URL", "postgresql://localhost/todo_app")


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL and not an Engine,
    though an Engine is acceptable here as well. By skipping the Engine
    creation we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.
    """
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine and associate a
    connection with the context.
    """
    url = get_url()
    connectable = create_engine(
        url,
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
