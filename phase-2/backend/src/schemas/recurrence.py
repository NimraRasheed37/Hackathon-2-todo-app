"""Pydantic schemas for task recurrence."""

from datetime import datetime
from enum import Enum
from typing import Optional, List

from pydantic import BaseModel, Field, field_validator


class RecurrenceFrequency(str, Enum):
    """Supported recurrence frequencies."""
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"
    CUSTOM = "custom"


class RecurrencePattern(BaseModel):
    """Schema for recurrence pattern configuration.

    Examples:
    - Daily: {"frequency": "daily", "interval": 1}
    - Every 2 weeks on Mon/Wed: {"frequency": "weekly", "interval": 2, "days_of_week": [0, 2]}
    - Monthly on 15th: {"frequency": "monthly", "interval": 1, "day_of_month": 15}
    """

    frequency: RecurrenceFrequency = Field(..., description="Recurrence frequency type")
    interval: int = Field(default=1, ge=1, le=365, description="Interval between occurrences")
    days_of_week: Optional[List[int]] = Field(
        default=None,
        description="Days of week (0=Monday, 6=Sunday) for weekly recurrence"
    )
    day_of_month: Optional[int] = Field(
        default=None,
        ge=1,
        le=31,
        description="Day of month for monthly recurrence"
    )
    end_date: Optional[datetime] = Field(
        default=None,
        description="When the recurrence should stop"
    )
    max_occurrences: Optional[int] = Field(
        default=None,
        ge=1,
        le=1000,
        description="Maximum number of occurrences to create"
    )

    @field_validator("days_of_week")
    @classmethod
    def validate_days_of_week(cls, v):
        if v is not None:
            for day in v:
                if day < 0 or day > 6:
                    raise ValueError("days_of_week must be between 0 (Monday) and 6 (Sunday)")
        return v


class RecurrenceCreate(BaseModel):
    """Schema for creating a new recurrence on a task."""

    pattern: RecurrencePattern = Field(..., description="Recurrence configuration")
    start_date: Optional[datetime] = Field(
        default=None,
        description="When to start the recurrence (defaults to task due_date or now)"
    )


class RecurrenceUpdate(BaseModel):
    """Schema for updating an existing recurrence."""

    pattern: Optional[RecurrencePattern] = Field(default=None, description="Updated pattern")
    is_active: Optional[bool] = Field(default=None, description="Whether recurrence is active")


class RecurrenceResponse(BaseModel):
    """Schema for recurrence response."""

    id: int
    task_id: int
    pattern: dict
    next_occurrence: Optional[datetime] = None
    last_generated: Optional[datetime] = None
    total_occurrences: int
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class RecurrenceWithTaskInfo(RecurrenceResponse):
    """Schema for recurrence response with task info."""

    task_title: str
    task_user_id: str
