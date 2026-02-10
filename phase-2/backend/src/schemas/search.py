"""Pydantic schemas for task search."""

from datetime import datetime
from enum import Enum
from typing import Optional, List

from pydantic import BaseModel, Field


class TaskPriority(str, Enum):
    """Task priority levels."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    NONE = "none"


class TaskStatus(str, Enum):
    """Task status values."""
    PENDING = "pending"
    COMPLETED = "completed"


class SortField(str, Enum):
    """Sortable fields for search."""
    RELEVANCE = "relevance"
    DUE_DATE = "due_date"
    PRIORITY = "priority"
    CREATED_AT = "created_at"
    TITLE = "title"


class SortOrder(str, Enum):
    """Sort order."""
    ASC = "asc"
    DESC = "desc"


class SearchQuery(BaseModel):
    """Schema for search query."""

    text: Optional[str] = Field(
        default=None,
        max_length=200,
        description="Full-text search query"
    )
    status: Optional[List[TaskStatus]] = Field(
        default=None,
        description="Filter by status"
    )
    priority: Optional[List[TaskPriority]] = Field(
        default=None,
        description="Filter by priority levels"
    )
    tags: Optional[List[int]] = Field(
        default=None,
        description="Filter by tag IDs"
    )
    due_date_from: Optional[datetime] = Field(
        default=None,
        description="Filter tasks due after this date"
    )
    due_date_to: Optional[datetime] = Field(
        default=None,
        description="Filter tasks due before this date"
    )
    has_recurrence: Optional[bool] = Field(
        default=None,
        description="Filter by recurrence status"
    )
    sort_by: SortField = Field(
        default=SortField.RELEVANCE,
        description="Field to sort by"
    )
    sort_order: SortOrder = Field(
        default=SortOrder.DESC,
        description="Sort order"
    )
    limit: int = Field(
        default=20,
        ge=1,
        le=100,
        description="Maximum results to return"
    )
    offset: int = Field(
        default=0,
        ge=0,
        description="Pagination offset"
    )


class SearchResultItem(BaseModel):
    """Schema for a single search result."""

    id: int
    user_id: str
    title: str
    description: Optional[str] = None
    completed: bool
    priority: Optional[str] = None
    due_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    tags: List[dict] = Field(default_factory=list)
    has_recurrence: bool = False
    relevance_score: Optional[float] = None

    model_config = {"from_attributes": True}


class SearchResults(BaseModel):
    """Schema for search results."""

    results: List[SearchResultItem]
    total: int
    has_more: bool
    query: dict  # Original query for reference


class QuickSearchResult(BaseModel):
    """Schema for quick search (autocomplete) results."""

    tasks: List[dict] = Field(
        description="Matching tasks with id, title, and status"
    )
    tags: List[dict] = Field(
        description="Matching tags with id and name"
    )
