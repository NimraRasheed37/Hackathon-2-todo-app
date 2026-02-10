"""Tag SQLModel entity."""

from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, SQLModel


class Tag(SQLModel, table=True):
    """SQLModel entity representing a user-defined tag."""

    __tablename__ = "tags"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(nullable=False, index=True)
    name: str = Field(max_length=50, nullable=False)
    color: str = Field(default="#808080", max_length=7)
    icon: Optional[str] = Field(default=None, max_length=10)
    usage_count: int = Field(default=0)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class TaskTag(SQLModel, table=True):
    """SQLModel entity representing the many-to-many relationship between tasks and tags."""

    __tablename__ = "task_tags"

    task_id: int = Field(foreign_key="tasks.id", primary_key=True)
    tag_id: int = Field(foreign_key="tags.id", primary_key=True)
