"""Pydantic schemas for tags."""

from datetime import datetime
from typing import Optional, List
import re

from pydantic import BaseModel, Field, field_validator


class TagCreate(BaseModel):
    """Schema for creating a new tag."""

    name: str = Field(
        min_length=1,
        max_length=50,
        description="Tag name"
    )
    color: str = Field(
        default="#808080",
        description="Hex color code (e.g., #FF5733)"
    )
    icon: Optional[str] = Field(
        default=None,
        max_length=10,
        description="Emoji or icon character"
    )

    @field_validator("color")
    @classmethod
    def validate_color(cls, v):
        if not re.match(r"^#[0-9A-Fa-f]{6}$", v):
            raise ValueError("Color must be a valid hex code (e.g., #FF5733)")
        return v.upper()

    @field_validator("name")
    @classmethod
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError("Tag name cannot be empty")
        return v.strip()


class TagUpdate(BaseModel):
    """Schema for updating a tag."""

    name: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=50
    )
    color: Optional[str] = Field(default=None)
    icon: Optional[str] = Field(default=None, max_length=10)

    @field_validator("color")
    @classmethod
    def validate_color(cls, v):
        if v is not None and not re.match(r"^#[0-9A-Fa-f]{6}$", v):
            raise ValueError("Color must be a valid hex code (e.g., #FF5733)")
        return v.upper() if v else v

    @field_validator("name")
    @classmethod
    def validate_name(cls, v):
        if v is not None and not v.strip():
            raise ValueError("Tag name cannot be empty")
        return v.strip() if v else v


class TagResponse(BaseModel):
    """Schema for tag response."""

    id: int
    user_id: str
    name: str
    color: str
    icon: Optional[str] = None
    usage_count: int
    created_at: datetime

    model_config = {"from_attributes": True}


class TaskTagsUpdate(BaseModel):
    """Schema for updating task tags."""

    tag_ids: List[int] = Field(
        description="List of tag IDs to assign to the task"
    )


class TaskTagsResponse(BaseModel):
    """Schema for task tags response."""

    task_id: int
    tags: List[TagResponse]
