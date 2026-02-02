"""Message SQLModel entity."""

from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any, Optional

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from src.models.conversation import Conversation


class Message(SQLModel, table=True):
    """SQLModel entity representing a message in a conversation."""

    __tablename__ = "messages"

    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversations.id", nullable=False, index=True)
    role: str = Field(max_length=50, nullable=False)  # 'user', 'assistant', 'tool'
    content: str = Field(nullable=False)
    tool_calls: Optional[dict[str, Any]] = Field(default=None, sa_column=Column(JSONB))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Relationship to conversation
    conversation: Optional["Conversation"] = Relationship(back_populates="messages")
