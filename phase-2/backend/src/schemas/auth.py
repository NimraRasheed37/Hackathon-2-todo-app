"""Authentication schemas for JWT token handling."""

import uuid
from typing import Optional

from pydantic import BaseModel, Field


class TokenPayload(BaseModel):
    """JWT token payload structure from Better Auth."""

    sub: uuid.UUID = Field(..., description="User ID (subject claim)")
    email: str = Field(..., description="User's email address")
    name: str = Field(..., description="User's display name")
    iat: int = Field(..., description="Issued at (Unix timestamp)")
    exp: int = Field(..., description="Expiration (Unix timestamp)")


class UserInfo(BaseModel):
    """User information extracted from JWT for use in request context."""

    id: uuid.UUID = Field(..., description="User ID")
    email: str = Field(..., description="User's email address")
    name: str = Field(..., description="User's display name")


class AuthErrorResponse(BaseModel):
    """Authentication error response format."""

    detail: str = Field(..., description="Error message")
    error_code: Optional[str] = Field(None, description="Machine-readable error code")
