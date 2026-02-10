"""Pydantic schemas for task API requests and responses."""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, field_validator, model_validator


class Priority(str, Enum):
    """Task priority levels."""
    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class TaskCreate(BaseModel):
    """Request schema for creating a new task."""

    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    priority: Priority = Field(default=Priority.NONE)
    due_date: Optional[datetime] = Field(default=None)

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str) -> str:
        """Trim whitespace and validate non-empty title."""
        trimmed = v.strip()
        if not trimmed:
            raise ValueError("Title cannot be empty or whitespace only")
        return trimmed


class TaskUpdate(BaseModel):
    """Request schema for updating an existing task."""

    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    priority: Optional[Priority] = Field(default=None)
    due_date: Optional[datetime] = Field(default=None)

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: Optional[str]) -> Optional[str]:
        """Trim whitespace and validate non-empty title if provided."""
        if v is None:
            return None
        trimmed = v.strip()
        if not trimmed:
            raise ValueError("Title cannot be empty or whitespace only")
        return trimmed

    @model_validator(mode="after")
    def check_at_least_one_field(self) -> "TaskUpdate":
        """Ensure at least one field is provided for update."""
        if all(v is None for v in [self.title, self.description, self.priority, self.due_date]):
            raise ValueError("At least one field must be provided for update")
        return self


class TaskRead(BaseModel):
    """Response schema for task data."""

    id: int
    user_id: str
    title: str
    description: Optional[str]
    completed: bool
    priority: Priority
    due_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ErrorResponse(BaseModel):
    """Standard error response schema."""

    detail: str
    error_code: str
    field: Optional[str] = None
