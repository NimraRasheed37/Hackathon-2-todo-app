"""Task Recurrence SQLModel entity."""

from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB


class TaskRecurrence(SQLModel, table=True):
    """SQLModel entity representing a recurring task pattern."""

    __tablename__ = "task_recurrences"

    id: Optional[int] = Field(default=None, primary_key=True)
    task_id: int = Field(nullable=False, foreign_key="tasks.id", index=True)
    pattern: dict = Field(default={}, sa_column=Column(JSONB, nullable=False))
    next_occurrence: Optional[datetime] = Field(default=None)
    last_generated: Optional[datetime] = Field(default=None)
    total_occurrences: int = Field(default=0)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
