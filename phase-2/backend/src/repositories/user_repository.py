"""User repository for database operations."""

import uuid
from typing import Optional

from sqlmodel import Session, select

from src.core.logging_config import get_logger
from src.models.user import User

logger = get_logger(__name__)


class UserRepository:
    """Repository for User database operations."""

    def __init__(self, session: Session):
        """Initialize repository with database session."""
        self.session = session

    def get_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        """
        Get user by ID.

        Args:
            user_id: User UUID

        Returns:
            User if found, None otherwise
        """
        return self.session.get(User, user_id)

    def get_by_email(self, email: str) -> Optional[User]:
        """
        Get user by email (case-insensitive).

        Args:
            email: User email

        Returns:
            User if found, None otherwise
        """
        statement = select(User).where(User.email.ilike(email))
        return self.session.exec(statement).first()

    def create(self, email: str, name: str, password_hash: str) -> User:
        """
        Create a new user.

        Args:
            email: User email
            name: User display name
            password_hash: Bcrypt hashed password

        Returns:
            Created User
        """
        user = User(
            email=email.lower(),  # Store email in lowercase
            name=name,
            password_hash=password_hash,
        )
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)

        logger.info(f"Created user: {user.id} ({user.email})")
        return user

    def exists_by_email(self, email: str) -> bool:
        """
        Check if user exists by email (case-insensitive).

        Args:
            email: User email

        Returns:
            True if user exists
        """
        statement = select(User.id).where(User.email.ilike(email))
        return self.session.exec(statement).first() is not None
