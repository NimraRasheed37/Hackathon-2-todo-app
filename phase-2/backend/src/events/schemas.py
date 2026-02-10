"""Event schema definitions for Kafka events via Dapr pub/sub."""
from datetime import datetime
from enum import Enum
from typing import Any, Optional
from uuid import uuid4

from pydantic import BaseModel, Field


class EventType(str, Enum):
    """Task event types."""
    TASK_CREATED = "task.created"
    TASK_UPDATED = "task.updated"
    TASK_COMPLETED = "task.completed"
    TASK_DELETED = "task.deleted"
    REMINDER_DUE = "reminder.due"
    REMINDER_SENT = "reminder.sent"
    RECURRENCE_TRIGGERED = "recurrence.triggered"
    NOTIFICATION_SENT = "notification.sent"


class EventMetadata(BaseModel):
    """Event metadata for tracing and debugging."""
    source: str = "todo-backend"
    schema_version: str = "1.0"
    correlation_id: Optional[str] = None


class BaseEvent(BaseModel):
    """Base class for all events."""
    event_id: str = Field(default_factory=lambda: str(uuid4()))
    event_type: EventType
    aggregate_type: str
    aggregate_id: str
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    version: int = 1
    user_id: str
    correlation_id: Optional[str] = None
    payload: dict[str, Any] = Field(default_factory=dict)
    metadata: EventMetadata = Field(default_factory=EventMetadata)

    class Config:
        use_enum_values = True


class TaskEvent(BaseEvent):
    """Event for task operations."""
    aggregate_type: str = "Task"

    @classmethod
    def task_created(
        cls,
        task_id: str,
        user_id: str,
        title: str,
        description: Optional[str] = None,
        priority: str = "none",
        due_date: Optional[str] = None,
        recurrence_pattern: Optional[dict] = None,
        correlation_id: Optional[str] = None,
    ) -> "TaskEvent":
        """Create a TaskCreated event."""
        return cls(
            event_type=EventType.TASK_CREATED,
            aggregate_id=task_id,
            user_id=user_id,
            correlation_id=correlation_id,
            payload={
                "task_id": task_id,
                "title": title,
                "description": description,
                "priority": priority,
                "due_date": due_date,
                "recurrence_pattern": recurrence_pattern,
            },
        )

    @classmethod
    def task_updated(
        cls,
        task_id: str,
        user_id: str,
        changes: dict[str, Any],
        correlation_id: Optional[str] = None,
    ) -> "TaskEvent":
        """Create a TaskUpdated event."""
        return cls(
            event_type=EventType.TASK_UPDATED,
            aggregate_id=task_id,
            user_id=user_id,
            correlation_id=correlation_id,
            payload={"task_id": task_id, "changes": changes},
        )

    @classmethod
    def task_completed(
        cls,
        task_id: str,
        user_id: str,
        has_recurrence: bool = False,
        correlation_id: Optional[str] = None,
    ) -> "TaskEvent":
        """Create a TaskCompleted event."""
        return cls(
            event_type=EventType.TASK_COMPLETED,
            aggregate_id=task_id,
            user_id=user_id,
            correlation_id=correlation_id,
            payload={"task_id": task_id, "has_recurrence": has_recurrence},
        )

    @classmethod
    def task_deleted(
        cls,
        task_id: str,
        user_id: str,
        correlation_id: Optional[str] = None,
    ) -> "TaskEvent":
        """Create a TaskDeleted event."""
        return cls(
            event_type=EventType.TASK_DELETED,
            aggregate_id=task_id,
            user_id=user_id,
            correlation_id=correlation_id,
            payload={"task_id": task_id},
        )


class ReminderEvent(BaseEvent):
    """Event for reminder operations."""
    aggregate_type: str = "Reminder"

    @classmethod
    def reminder_due(
        cls,
        reminder_id: str,
        task_id: str,
        user_id: str,
        task_title: str,
        channels: list[str],
        correlation_id: Optional[str] = None,
    ) -> "ReminderEvent":
        """Create a ReminderDue event."""
        return cls(
            event_type=EventType.REMINDER_DUE,
            aggregate_id=reminder_id,
            user_id=user_id,
            correlation_id=correlation_id,
            payload={
                "reminder_id": reminder_id,
                "task_id": task_id,
                "task_title": task_title,
                "channels": channels,
            },
        )

    @classmethod
    def reminder_sent(
        cls,
        reminder_id: str,
        user_id: str,
        channel: str,
        correlation_id: Optional[str] = None,
    ) -> "ReminderEvent":
        """Create a ReminderSent event."""
        return cls(
            event_type=EventType.REMINDER_SENT,
            aggregate_id=reminder_id,
            user_id=user_id,
            correlation_id=correlation_id,
            payload={"reminder_id": reminder_id, "channel": channel},
        )


class RecurrenceEvent(BaseEvent):
    """Event for recurrence operations."""
    aggregate_type: str = "Recurrence"

    @classmethod
    def recurrence_triggered(
        cls,
        recurrence_id: str,
        original_task_id: str,
        new_task_id: str,
        user_id: str,
        occurrence_number: int,
        correlation_id: Optional[str] = None,
    ) -> "RecurrenceEvent":
        """Create a RecurrenceTriggered event."""
        return cls(
            event_type=EventType.RECURRENCE_TRIGGERED,
            aggregate_id=recurrence_id,
            user_id=user_id,
            correlation_id=correlation_id,
            payload={
                "recurrence_id": recurrence_id,
                "original_task_id": original_task_id,
                "new_task_id": new_task_id,
                "occurrence_number": occurrence_number,
            },
        )


# Kafka topic names
TOPICS = {
    "task_events": "todo.tasks.events",
    "reminders": "todo.reminders.scheduled",
    "notifications": "todo.notifications.outbound",
    "audit": "todo.audit.log",
    "dlq": "todo.dlq",
}
