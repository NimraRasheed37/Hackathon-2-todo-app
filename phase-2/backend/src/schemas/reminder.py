"""Pydantic schemas for reminders and notifications."""

from datetime import datetime
from enum import Enum
from typing import Optional, List, Any

from pydantic import BaseModel, Field, model_validator


class ReminderType(str, Enum):
    """Reminder type enum."""
    RELATIVE = "relative"
    ABSOLUTE = "absolute"


class ReminderChannel(str, Enum):
    """Supported reminder channels."""
    IN_APP = "in_app"
    EMAIL = "email"
    PUSH = "push"


class ReminderStatus(str, Enum):
    """Reminder status enum."""
    PENDING = "pending"
    SENT = "sent"
    CANCELLED = "cancelled"


class ReminderCreate(BaseModel):
    """Schema for creating a new reminder."""

    reminder_type: ReminderType = Field(
        default=ReminderType.RELATIVE,
        description="Type of reminder: relative (before due date) or absolute (specific time)"
    )
    relative_minutes: Optional[int] = Field(
        default=None,
        ge=1,
        le=525600,  # Max 1 year in minutes
        description="Minutes before due date to trigger reminder"
    )
    absolute_time: Optional[datetime] = Field(
        default=None,
        description="Specific time to trigger reminder"
    )
    channels: List[ReminderChannel] = Field(
        default=[ReminderChannel.IN_APP],
        min_length=1,
        description="Channels to deliver the reminder"
    )

    @model_validator(mode='after')
    def validate_reminder_config(self):
        """Validate that either relative_minutes or absolute_time is provided."""
        if self.reminder_type == ReminderType.RELATIVE:
            if self.relative_minutes is None:
                raise ValueError("relative_minutes is required for relative reminders")
        elif self.reminder_type == ReminderType.ABSOLUTE:
            if self.absolute_time is None:
                raise ValueError("absolute_time is required for absolute reminders")
        return self


class ReminderResponse(BaseModel):
    """Schema for reminder response."""

    id: int
    task_id: int
    user_id: str
    reminder_type: str
    relative_minutes: Optional[int] = None
    absolute_time: Optional[datetime] = None
    channels: List[str]
    status: str
    scheduled_at: datetime
    sent_at: Optional[datetime] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class NotificationType(str, Enum):
    """Notification type enum."""
    REMINDER = "reminder"
    TASK_UPDATE = "task_update"
    SYSTEM = "system"
    RECURRENCE = "recurrence"


class NotificationCreate(BaseModel):
    """Schema for creating a notification (internal use)."""

    user_id: str
    type: NotificationType
    title: str = Field(max_length=200)
    message: str = Field(max_length=1000)
    data: dict = Field(default_factory=dict)


class NotificationResponse(BaseModel):
    """Schema for notification response."""

    id: int
    user_id: str
    type: str
    title: str
    message: str
    data: dict
    read: bool
    created_at: datetime
    read_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class NotificationList(BaseModel):
    """Schema for paginated notification list."""

    notifications: List[NotificationResponse]
    total: int
    unread_count: int


class MarkNotificationsRead(BaseModel):
    """Schema for marking notifications as read."""

    notification_ids: List[int] = Field(
        min_length=1,
        description="IDs of notifications to mark as read"
    )
