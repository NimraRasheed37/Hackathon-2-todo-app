"""Notification SQLModel entity."""

from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, SQLModel
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB


class Notification(SQLModel, table=True):
    """SQLModel entity representing a user notification."""

    __tablename__ = "notifications"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(nullable=False, index=True)
    type: str = Field(max_length=50, index=True)  # reminder, task_update, system, etc.
    title: str = Field(max_length=200)
    message: str = Field(max_length=1000)
    data: dict = Field(default={}, sa_column=Column(JSONB))
    read: bool = Field(default=False, index=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    read_at: Optional[datetime] = Field(default=None)
