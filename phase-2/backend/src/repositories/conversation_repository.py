"""Conversation repository for database operations."""

from datetime import datetime, timezone
from typing import Any, List, Optional

from sqlmodel import Session, func, select

from src.models.conversation import Conversation
from src.models.message import Message


class ConversationRepository:
    """Repository for conversation database operations."""

    def __init__(self, session: Session):
        self.session = session

    def get_by_id_and_user(self, conversation_id: int, user_id: str) -> Optional[Conversation]:
        """Get a conversation by ID with ownership validation."""
        statement = select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id,
        )
        return self.session.exec(statement).first()

    def get_all_by_user(self, user_id: str, limit: int = 20) -> List[Conversation]:
        """Get all conversations for a user, ordered by updated_at."""
        statement = (
            select(Conversation)
            .where(Conversation.user_id == user_id)
            .order_by(Conversation.updated_at.desc())
            .limit(limit)
        )
        return list(self.session.exec(statement).all())

    def create(self, user_id: str, title: str = "New Conversation") -> Conversation:
        """Create a new conversation for a user."""
        conversation = Conversation(
            user_id=user_id,
            title=title,
        )
        self.session.add(conversation)
        self.session.commit()
        self.session.refresh(conversation)
        return conversation

    def update_title(self, conversation_id: int, user_id: str, title: str) -> Optional[Conversation]:
        """Update conversation title with ownership validation."""
        conversation = self.get_by_id_and_user(conversation_id, user_id)
        if not conversation:
            return None

        conversation.title = title
        conversation.updated_at = datetime.now(timezone.utc)
        self.session.add(conversation)
        self.session.commit()
        self.session.refresh(conversation)
        return conversation

    def update_timestamp(self, conversation_id: int) -> None:
        """Update conversation's updated_at timestamp."""
        statement = select(Conversation).where(Conversation.id == conversation_id)
        conversation = self.session.exec(statement).first()
        if conversation:
            conversation.updated_at = datetime.now(timezone.utc)
            self.session.add(conversation)
            self.session.commit()

    def delete(self, conversation_id: int, user_id: str) -> bool:
        """Delete a conversation with ownership validation."""
        conversation = self.get_by_id_and_user(conversation_id, user_id)
        if not conversation:
            return False

        self.session.delete(conversation)
        self.session.commit()
        return True

    def add_message(
        self,
        conversation_id: int,
        role: str,
        content: str,
        tool_calls: Optional[dict[str, Any]] = None,
    ) -> Message:
        """Add a message to a conversation."""
        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
            tool_calls=tool_calls,
        )
        self.session.add(message)
        self.session.commit()
        self.session.refresh(message)

        # Update conversation timestamp
        self.update_timestamp(conversation_id)

        return message

    def get_messages(
        self, conversation_id: int, limit: int = 50
    ) -> List[Message]:
        """Get messages for a conversation, ordered by created_at."""
        statement = (
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.desc())
            .limit(limit)
        )
        messages = list(self.session.exec(statement).all())
        # Return in chronological order
        messages.reverse()
        return messages

    def get_message_count(self, conversation_id: int) -> int:
        """Get the count of messages in a conversation."""
        statement = (
            select(func.count())
            .select_from(Message)
            .where(Message.conversation_id == conversation_id)
        )
        result = self.session.exec(statement).first()
        return result or 0
