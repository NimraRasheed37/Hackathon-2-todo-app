"""Database connection and session management."""

from typing import Generator

from sqlmodel import Session, SQLModel, create_engine

from src.config import get_settings

# Import models to ensure they are registered with SQLModel.metadata
# User must be imported BEFORE Task due to FK dependency
from src.models.user import User  # noqa: F401
from src.models.task import Task  # noqa: F401

settings = get_settings()

# Create database engine with connection pooling
engine = create_engine(
    settings.database_url,
    echo=settings.is_development,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
)


def create_db_and_tables() -> None:
    """Create database tables if they don't exist."""
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """Get database session with automatic cleanup."""
    with Session(engine) as session:
        yield session
