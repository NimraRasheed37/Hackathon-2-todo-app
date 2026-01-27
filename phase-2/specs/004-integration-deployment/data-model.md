# Data Model: Integration, Testing & Deployment

**Feature**: 004-integration-deployment
**Date**: 2026-01-26

---

## Overview

This module does not introduce any new data models. All data models were defined in previous modules:

- **Module 1**: Task model (id, title, description, completed, created_at, updated_at, user_id)
- **Module 2**: User model (managed by Better Auth via session/account tables)

## Existing Data Models Reference

### Tasks Table (Backend - SQLAlchemy)

```python
# phase-2/backend/src/models/task.py
class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    user_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now, onupdate=datetime.now, nullable=False
    )
```

### Better Auth Tables (Frontend/Neon - Auto-managed)

Better Auth automatically creates and manages:
- `user` - User accounts
- `session` - Active sessions
- `account` - OAuth accounts (if configured)
- `verification` - Email verification tokens

### TypeScript Types (Frontend)

```typescript
// phase-2/frontend/src/types/index.ts
interface Task {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  created_at: string;
  updated_at: string;
  user_id: string;
}

interface User {
  id: string;
  email: string;
  name: string;
}
```

## Database Configuration

### Neon PostgreSQL

Both backend and frontend connect to the same Neon PostgreSQL database:

```
postgresql://neondb_owner:***@ep-xxx.us-east-1.aws.neon.tech/neondb?sslmode=require
```

**Tables**:
| Table | Created By | Purpose |
|-------|-----------|---------|
| tasks | Backend (SQLAlchemy) | Task storage |
| user | Frontend (Better Auth) | User accounts |
| session | Frontend (Better Auth) | Active sessions |
| account | Frontend (Better Auth) | OAuth providers |

## Integration Notes

1. **Shared Database**: Backend and frontend share the same Neon database
2. **User ID Linking**: `tasks.user_id` references `user.id` from Better Auth
3. **No Foreign Key**: Soft reference (string) rather than hard FK constraint for flexibility
4. **Connection Pooling**: Both services use connection pooling to avoid exceeding Neon limits

## No Changes Required

This module focuses on:
- Docker configuration
- Deployment setup
- Documentation

No database schema changes are needed.
