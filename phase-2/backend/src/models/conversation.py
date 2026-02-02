"""Conversation SQLModel entity."""

from datetime import datetime, timezone
from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from src.models.message import Message


class Conversation(SQLModel, table=True):
    """SQLModel entity representing a chat conversation."""

    __tablename__ = "conversations"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(nullable=False, index=True, max_length=255)
    title: str = Field(default="New Conversation", max_length=255)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Relationship to messages
    messages: List["Message"] = Relationship(back_populates="conversation")
