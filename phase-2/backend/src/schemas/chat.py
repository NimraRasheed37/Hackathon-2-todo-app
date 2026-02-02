"""Chat request and response schemas."""

from datetime import datetime
from typing import Any, List, Optional

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Request schema for chat endpoint."""

    message: str = Field(..., min_length=1, max_length=2000)
    conversation_id: Optional[int] = None  # None = new conversation


class ToolCallResult(BaseModel):
    """Schema for a tool call result."""

    name: str
    arguments: dict[str, Any]
    result: dict[str, Any]


class ChatResponse(BaseModel):
    """Response schema for chat endpoint."""

    message: str
    conversation_id: int
    tool_calls: Optional[List[ToolCallResult]] = None


class MessageRead(BaseModel):
    """Schema for reading a message."""

    id: int
    role: str
    content: str
    tool_calls: Optional[dict[str, Any]] = None
    created_at: datetime


class ConversationSummary(BaseModel):
    """Schema for conversation list item."""

    id: int
    title: str
    updated_at: datetime
    message_count: int = 0


class ConversationDetail(BaseModel):
    """Schema for conversation with messages."""

    id: int
    title: str
    created_at: datetime
    updated_at: datetime
    messages: List[MessageRead]
