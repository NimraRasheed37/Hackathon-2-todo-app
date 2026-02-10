"""Task Reminder SQLModel entity."""

from datetime import datetime, timezone
from typing import Optional, List

from sqlmodel import Field, SQLModel
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import String


class TaskReminder(SQLModel, table=True):
    """SQLModel entity representing a task reminder."""

    __tablename__ = "task_reminders"

    id: Optional[int] = Field(default=None, primary_key=True)
    task_id: int = Field(nullable=False, foreign_key="tasks.id", index=True)
    user_id: str = Field(nullable=False, index=True)
    reminder_type: str = Field(default="relative", max_length=20)  # 'relative' or 'absolute'
    relative_minutes: Optional[int] = Field(default=None)
    absolute_time: Optional[datetime] = Field(default=None)
    channels: List[str] = Field(
        default=["in_app"],
        sa_column=Column(ARRAY(String), nullable=False)
    )
    status: str = Field(default="pending", max_length=20, index=True)  # pending, sent, cancelled
    scheduled_at: datetime = Field(nullable=False, index=True)
    sent_at: Optional[datetime] = Field(default=None)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
