# Data Model: Authentication & User Management

**Branch**: `002-auth-user-management` | **Date**: 2026-01-26 | **Plan**: [plan.md](./plan.md)

This document defines the data model for user authentication and the updates to existing entities.

---

## Entity: User (NEW)

### Description

Represents a registered user account in the Todo application. Users authenticate with email/password and receive JWT tokens for API access.

### Schema

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY, NOT NULL, DEFAULT uuid_generate_v4() | Unique identifier for the user |
| `email` | VARCHAR(255) | UNIQUE, NOT NULL, INDEX | User's email address (case-insensitive) |
| `name` | VARCHAR(100) | NOT NULL | User's display name |
| `password_hash` | VARCHAR(255) | NOT NULL | Bcrypt-hashed password |
| `created_at` | TIMESTAMP WITH TIME ZONE | NOT NULL, DEFAULT NOW() | When the user registered |
| `updated_at` | TIMESTAMP WITH TIME ZONE | NOT NULL, DEFAULT NOW() | When the user was last updated |

### SQLModel Definition

```python
import uuid
from datetime import datetime, timezone
from typing import Optional
from sqlmodel import Field, SQLModel
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

class User(SQLModel, table=True):
    """SQLModel entity representing a user account."""

    __tablename__ = "users"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(PG_UUID(as_uuid=True), primary_key=True)
    )
    email: str = Field(unique=True, index=True, max_length=255)
    name: str = Field(max_length=100)
    password_hash: str = Field(max_length=255)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
```

### Indexes

| Index Name | Columns | Type | Purpose |
|------------|---------|------|---------|
| `users_pkey` | `id` | B-tree (Primary Key) | Unique identifier lookup |
| `ix_users_email` | `email` | B-tree (Unique) | Email lookup for login, uniqueness |

### Validation Rules

| Field | Rule | Error Message |
|-------|------|---------------|
| `email` | Valid email format (RFC 5322) | "Invalid email format" |
| `email` | Unique (case-insensitive) | "Email already exists" |
| `name` | 1-100 characters | "Name must be between 1 and 100 characters" |
| `password` | Min 8 characters (before hashing) | "Password must be at least 8 characters" |

---

## Entity: Task (UPDATED)

### Description

Represents a task in the Todo application. Updated to use UUID for `user_id` and add foreign key constraint to `users` table.

### Schema Changes

| Field | Old Type | New Type | Change Description |
|-------|----------|----------|-------------------|
| `user_id` | VARCHAR(255) | UUID | Changed to UUID for FK relationship |

### Updated Schema

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | INTEGER | PRIMARY KEY, AUTO INCREMENT | Unique identifier for the task |
| `user_id` | UUID | NOT NULL, FK → users.id, ON DELETE CASCADE, INDEX | Owner of the task |
| `title` | VARCHAR(200) | NOT NULL | Task title (1-200 characters) |
| `description` | VARCHAR(1000) | NULLABLE | Task description (optional) |
| `completed` | BOOLEAN | NOT NULL, DEFAULT FALSE, INDEX | Completion status |
| `created_at` | TIMESTAMP WITH TIME ZONE | NOT NULL, DEFAULT NOW() | When the task was created |
| `updated_at` | TIMESTAMP WITH TIME ZONE | NOT NULL, DEFAULT NOW() | When the task was last updated |

### Updated SQLModel Definition

```python
import uuid
from datetime import datetime, timezone
from typing import Optional
from sqlmodel import Field, SQLModel
from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

class Task(SQLModel, table=True):
    """SQLModel entity representing a task in the database."""

    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: uuid.UUID = Field(
        sa_column=Column(
            PG_UUID(as_uuid=True),
            ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
            index=True
        )
    )
    title: str = Field(max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False, index=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
```

### Foreign Key Behavior

| Action on User | Effect on Tasks |
|----------------|-----------------|
| DELETE user | CASCADE - all user's tasks are deleted |
| UPDATE user.id | Not applicable (UUID is immutable) |

---

## Entity: JWT Token (Transient)

### Description

Represents the JWT token payload. Not stored in database; exists only in memory during request processing.

### Schema (Pydantic Model)

```python
import uuid
from pydantic import BaseModel

class TokenPayload(BaseModel):
    """JWT token payload structure."""

    sub: uuid.UUID          # User ID (subject claim)
    email: str              # User's email
    name: str               # User's display name
    iat: int                # Issued at (Unix timestamp)
    exp: int                # Expiration (Unix timestamp)
```

### Token Claims

| Claim | Type | Description |
|-------|------|-------------|
| `sub` | UUID (string) | User ID - matches users.id |
| `email` | string | User's email address |
| `name` | string | User's display name |
| `iat` | integer | Unix timestamp when token was issued |
| `exp` | integer | Unix timestamp when token expires |

### Token Lifecycle

1. **Creation**: Frontend (Better Auth) creates token on signup/signin
2. **Storage**: Stored in httpOnly cookie or localStorage
3. **Transmission**: Sent via `Authorization: Bearer <token>` header
4. **Verification**: Backend validates signature and expiration
5. **Expiration**: Token becomes invalid after 7 days

---

## Entity Relationships

### Diagram

```
┌──────────────────────────────────────────────────────────────────┐
│                          USERS TABLE                              │
├──────────────────────────────────────────────────────────────────┤
│  id (UUID, PK)                                                   │
│  email (VARCHAR, UNIQUE)                                         │
│  name (VARCHAR)                                                  │
│  password_hash (VARCHAR)                                         │
│  created_at (TIMESTAMP)                                          │
│  updated_at (TIMESTAMP)                                          │
└──────────────────────────────────────────────────────────────────┘
         │
         │ 1
         │
         │ user_id (FK, ON DELETE CASCADE)
         │
         │ N
         ▼
┌──────────────────────────────────────────────────────────────────┐
│                          TASKS TABLE                              │
├──────────────────────────────────────────────────────────────────┤
│  id (INTEGER, PK)                                                │
│  user_id (UUID, FK → users.id)                                   │
│  title (VARCHAR)                                                 │
│  description (VARCHAR, NULLABLE)                                 │
│  completed (BOOLEAN)                                             │
│  created_at (TIMESTAMP)                                          │
│  updated_at (TIMESTAMP)                                          │
└──────────────────────────────────────────────────────────────────┘
```

### Relationship Details

| Relationship | Type | Description |
|--------------|------|-------------|
| User → Tasks | One-to-Many | A user can have many tasks |
| Task → User | Many-to-One | A task belongs to exactly one user |

### Cascade Behaviors

| Event | Behavior |
|-------|----------|
| User deleted | All user's tasks are automatically deleted (CASCADE) |
| Task deleted | No effect on user |
| User updated | No effect on tasks (FK references immutable UUID) |

---

## Database Migration

### Migration Script (for existing databases with string user_id)

```sql
-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

CREATE INDEX IF NOT EXISTS ix_users_email ON users (email);

-- NOTE: For new databases, tasks table is created with UUID user_id from start
-- For existing databases with data, migration requires data preservation strategy
-- which is out of scope for MVP (assuming fresh database for Module 2)

-- Recreate tasks table with UUID user_id (for fresh database)
CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description VARCHAR(1000),
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

CREATE INDEX IF NOT EXISTS ix_tasks_user_id ON tasks (user_id);
CREATE INDEX IF NOT EXISTS ix_tasks_completed ON tasks (completed);
```

### Fresh Database Initialization

For new deployments, SQLModel's `create_all()` will create both tables with correct schema:

```python
from sqlmodel import SQLModel
from database import engine
from models.user import User
from models.task import Task

def init_db():
    """Initialize database with all tables."""
    SQLModel.metadata.create_all(engine)
```

---

## Data Validation Summary

### Registration Input Validation

| Field | Validation | Source |
|-------|------------|--------|
| email | Format, uniqueness | Better Auth (frontend) |
| name | 1-100 chars | Better Auth (frontend) |
| password | Min 8 chars | Better Auth (frontend) |

### API Request Validation

| Field | Validation | Source |
|-------|------------|--------|
| user_id (URL) | Valid UUID format | FastAPI path parameter |
| Authorization header | Bearer token format | HTTPBearer dependency |
| JWT token | Valid signature, not expired | PyJWT verification |

### Authorization Validation

| Check | Error |
|-------|-------|
| Token user_id ≠ URL user_id | 403 Forbidden |
| Task user_id ≠ Token user_id | 403 Forbidden |
