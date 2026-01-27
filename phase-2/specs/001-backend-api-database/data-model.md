# Data Model: Backend API & Database Layer

**Feature**: Backend API & Database Layer
**Date**: 2026-01-25
**Purpose**: Define the database schema, entities, relationships, and validation rules for the Todo application backend

---

## Overview

This data model defines a single entity (**Task**) with attributes, constraints, and relationships. The model is designed to support task management operations for multiple users with data isolation enforced at the application layer.

**Database**: Neon Serverless PostgreSQL
**ORM**: SQLModel (combines SQLAlchemy + Pydantic)
**Schema Management**: Auto-creation on startup (migrations deferred to post-MVP)

---

## Entity: Task

### Purpose

Represents a single todo item owned by a user. Tasks have a title, optional description, completion status, and audit timestamps.

### Attributes

| Attribute | Type | Constraints | Default | Description |
|-----------|------|-------------|---------|-------------|
| `id` | Integer | PRIMARY KEY, AUTO_INCREMENT | Auto-generated | Unique identifier for the task |
| `user_id` | VARCHAR(255) | NOT NULL, INDEXED | None | Owner of the task (references future users table) |
| `title` | VARCHAR(200) | NOT NULL, LENGTH(1-200) | None | Task name/summary |
| `description` | TEXT | NULLABLE, MAX_LENGTH(1000) | NULL | Detailed task description |
| `completed` | BOOLEAN | NOT NULL | FALSE | Whether task is marked as done |
| `created_at` | TIMESTAMP WITH TIME ZONE | NOT NULL | CURRENT_TIMESTAMP | When task was created |
| `updated_at` | TIMESTAMP WITH TIME ZONE | NOT NULL | CURRENT_TIMESTAMP | When task was last modified |

### Indexes

| Index Name | Columns | Purpose |
|------------|---------|---------|
| `idx_tasks_user_id` | `user_id` | Fast filtering by user (primary query pattern) |
| `idx_tasks_completed` | `completed` | Fast filtering by completion status |
| `idx_tasks_user_completed` | `user_id, completed` | Composite index for combined filters (optional optimization) |

**Rationale for Indexes**:
- **user_id**: Every query filters by user for data isolation → must be indexed
- **completed**: Common filter for "pending" vs "completed" tasks → should be indexed
- **Composite index**: Considered but deferred to post-MVP (single-column indexes sufficient for MVP scale)

### Constraints

#### Database-Level Constraints

```sql
-- Primary key constraint
CONSTRAINT pk_tasks PRIMARY KEY (id)

-- NOT NULL constraints
CONSTRAINT nn_tasks_user_id CHECK (user_id IS NOT NULL)
CONSTRAINT nn_tasks_title CHECK (title IS NOT NULL)
CONSTRAINT nn_tasks_completed CHECK (completed IS NOT NULL)
CONSTRAINT nn_tasks_created_at CHECK (created_at IS NOT NULL)
CONSTRAINT nn_tasks_updated_at CHECK (updated_at IS NOT NULL)

-- Length constraints (enforced by column type)
-- title: VARCHAR(200) limits to 200 characters
-- description: TEXT with application-level validation for 1000 char max

-- Foreign key constraint (deferred to Module 2 when users table exists)
-- CONSTRAINT fk_tasks_user_id FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
```

#### Application-Level Validation (Pydantic)

```python
# Validation rules enforced by Pydantic schemas:
# - title: min_length=1, max_length=200
# - description: max_length=1000 if provided
# - user_id: format validation (UUID or string)
# - completed: boolean type validation
```

---

## State Transitions

Tasks have a simple state machine with two states:

```
┌─────────┐            PATCH /complete            ┌───────────┐
│ PENDING │ ────────────────────────────────────> │ COMPLETED │
│ (false) │                                        │   (true)  │
└─────────┘ <──────────────────────────────────── └───────────┘
              PATCH /complete (toggle back)
```

**State Rules**:
1. New tasks start in PENDING state (completed = false)
2. PATCH /complete toggles between PENDING ↔ COMPLETED
3. PUT /update does NOT change completion status (only title/description)
4. DELETE removes task from any state (no soft delete)

**Allowed Transitions**:
- PENDING → COMPLETED (via PATCH /complete when completed=false)
- COMPLETED → PENDING (via PATCH /complete when completed=true)

**Forbidden Transitions**:
- None (any state can transition to any other state via toggle)

---

## Relationships

### Task → User (Many-to-One)

**Relationship Type**: Many tasks belong to one user

```
┌──────┐         owns          ┌──────┐
│ User │ ○────────────────< ● │ Task │
└──────┘      1         *      └──────┘
```

**Foreign Key**: `tasks.user_id` → `users.id` (enforced in Module 2)

**Cascade Behavior** (when users table exists):
- **ON DELETE CASCADE**: Deleting a user deletes all their tasks
- **ON UPDATE CASCADE**: Updating a user's ID updates all task references (rare)

**Data Isolation Enforcement**:
- Application layer validates user_id in URL matches task.user_id
- API layer enforces: "User can only access their own tasks"
- Database layer (future): Foreign key constraint ensures referential integrity

### Future Relationships (Out of Scope for Module 1)

- Task → Tags (many-to-many) - deferred to Phase 3+
- Task → Comments (one-to-many) - deferred to Phase 3+
- Task → Attachments (one-to-many) - deferred to Phase 3+

---

## Validation Rules

### Title Validation

- **Required**: ✅ YES (cannot be null or empty)
- **Minimum Length**: 1 character
- **Maximum Length**: 200 characters
- **Allowed Characters**: Any UTF-8 characters (including emojis)
- **Trimming**: Leading/trailing whitespace trimmed before validation
- **Unique**: ❌ NO (users can have duplicate task titles)

**Example Valid Titles**:
- "Buy groceries"
- "📧 Send email to client"
- "A" (single character is valid)
- "Write documentation for the new API endpoint that handles task creation and update operations" (long but under 200 chars)

**Example Invalid Titles**:
- "" (empty string - rejected)
- "   " (whitespace only - trimmed to empty, then rejected)
- "{201 characters}" (exceeds maximum length - rejected)

### Description Validation

- **Required**: ❌ NO (nullable field)
- **Minimum Length**: 0 characters (can be empty string or null)
- **Maximum Length**: 1000 characters
- **Allowed Characters**: Any UTF-8 characters (including emojis, newlines)
- **Trimming**: NOT trimmed (preserve user formatting)
- **Null vs Empty**: Both null and empty string ("") are allowed and treated as "no description"

**Example Valid Descriptions**:
- null (no description provided)
- "" (empty description)
- "Buy milk, eggs, bread" (simple description)
- "Multi-line description\nwith newlines\nand formatting" (preserves newlines)

**Example Invalid Descriptions**:
- "{1001 characters}" (exceeds maximum length - rejected)

### User ID Validation

- **Required**: ✅ YES (cannot be null)
- **Format**: String (UUID format recommended but not enforced in Module 1)
- **Length**: 1-255 characters (VARCHAR(255))
- **Source**: Extracted from URL path (/api/{user_id}/tasks)
- **Validation**: Currently accepts any non-empty string; will be validated against users table in Module 2

**Example Valid User IDs**:
- "user123" (simple string)
- "550e8400-e29b-41d4-a716-446655440000" (UUID format)
- "auth0|1234567890" (Auth0 format)

**Example Invalid User IDs**:
- "" (empty string - rejected)
- null (rejected)

### Completed Status Validation

- **Required**: ✅ YES (cannot be null)
- **Type**: Boolean
- **Default**: false (new tasks are pending)
- **Allowed Values**: true, false

---

## Timestamps

### created_at

- **Purpose**: Record when task was first created
- **Type**: TIMESTAMP WITH TIME ZONE (includes timezone information)
- **Timezone**: UTC (all timestamps stored in UTC)
- **Default**: CURRENT_TIMESTAMP (database sets automatically)
- **Mutability**: IMMUTABLE (never updated after creation)

### updated_at

- **Purpose**: Record when task was last modified
- **Type**: TIMESTAMP WITH TIME ZONE
- **Timezone**: UTC
- **Default**: CURRENT_TIMESTAMP (same as created_at for new tasks)
- **Mutability**: MUTABLE (updated on every PUT or PATCH operation)
- **Update Trigger**: Application sets updated_at = CURRENT_TIMESTAMP on update

**Update Behavior**:
- PUT /tasks/{id} → Updates updated_at
- PATCH /tasks/{id}/complete → Updates updated_at
- GET /tasks → Does NOT update updated_at (read-only)
- DELETE /tasks/{id} → Task deleted, no update needed

---

## Database Schema (SQL DDL)

```sql
-- Create tasks table
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,

    -- Indexes for performance
    CONSTRAINT pk_tasks PRIMARY KEY (id)
);

-- Create indexes
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_completed ON tasks(completed);

-- Foreign key constraint (deferred to Module 2)
-- ALTER TABLE tasks ADD CONSTRAINT fk_tasks_user_id
--     FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;
```

---

## SQLModel Entity Definition

```python
from sqlmodel import Field, SQLModel
from datetime import datetime
from typing import Optional

class Task(SQLModel, table=True):
    """
    SQLModel entity representing a task in the database.

    This model is used for database operations (CREATE TABLE, INSERT, SELECT, etc.).
    Separate Pydantic schemas (in schemas/task.py) are used for API requests/responses.
    """

    # Primary key with auto-increment
    id: Optional[int] = Field(default=None, primary_key=True)

    # Foreign key to users table (validated in Module 2)
    user_id: str = Field(
        index=True,
        max_length=255,
        description="Owner of this task (references users.id)"
    )

    # Task details
    title: str = Field(
        max_length=200,
        min_length=1,
        description="Task title (1-200 characters)"
    )

    description: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="Optional task description (max 1000 characters)"
    )

    # Status
    completed: bool = Field(
        default=False,
        index=True,
        description="Whether task is marked as complete"
    )

    # Audit timestamps
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="When task was created (UTC)"
    )

    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="When task was last modified (UTC)"
    )

    class Config:
        """SQLModel configuration"""
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "id": 1,
                "user_id": "user123",
                "title": "Buy groceries",
                "description": "Milk, eggs, bread",
                "completed": False,
                "created_at": "2026-01-25T10:30:00Z",
                "updated_at": "2026-01-25T10:30:00Z"
            }
        }
```

---

## Migration Strategy

### MVP (Module 1)

**Approach**: Auto-create schema on application startup

```python
# In database.py or main.py startup event
def create_db_and_tables():
    """Create database tables if they don't exist"""
    SQLModel.metadata.create_all(engine)
```

**Pros**:
- Simple, no migration tooling needed
- Works for MVP with single table
- Fast development iteration

**Cons**:
- Not suitable for production (can't handle schema changes safely)
- No migration history tracking
- Can't rollback schema changes

### Post-MVP (Future Enhancement)

**Approach**: Use Alembic for database migrations

```bash
# Generate migration when schema changes
alembic revision --autogenerate -m "Add user_id foreign key constraint"

# Apply migration
alembic upgrade head

# Rollback if needed
alembic downgrade -1
```

**When to Migrate**: After Module 2 (when users table is added and foreign key constraint is needed)

---

## Query Patterns

### Most Common Queries (Optimized with Indexes)

1. **List all tasks for a user** (filtered by status):
   ```sql
   SELECT * FROM tasks
   WHERE user_id = $1 AND completed = $2
   ORDER BY created_at DESC;
   ```
   - Uses: idx_tasks_user_id + idx_tasks_completed
   - Performance: < 50ms for 1000 tasks

2. **Get single task by ID** (with ownership check):
   ```sql
   SELECT * FROM tasks
   WHERE id = $1 AND user_id = $2;
   ```
   - Uses: Primary key (id) + idx_tasks_user_id
   - Performance: < 10ms

3. **Update task**:
   ```sql
   UPDATE tasks
   SET title = $1, description = $2, updated_at = CURRENT_TIMESTAMP
   WHERE id = $3 AND user_id = $4;
   ```
   - Uses: Primary key + idx_tasks_user_id
   - Performance: < 20ms

4. **Toggle completion**:
   ```sql
   UPDATE tasks
   SET completed = NOT completed, updated_at = CURRENT_TIMESTAMP
   WHERE id = $1 AND user_id = $2;
   ```
   - Uses: Primary key + idx_tasks_user_id
   - Performance: < 20ms

5. **Delete task**:
   ```sql
   DELETE FROM tasks
   WHERE id = $1 AND user_id = $2;
   ```
   - Uses: Primary key + idx_tasks_user_id
   - Performance: < 20ms

### Query Optimization Notes

- All queries include user_id in WHERE clause for data isolation
- Indexes on user_id and completed enable fast filtering
- ORDER BY created_at DESC requires sequential scan (acceptable for MVP with <1000 tasks per user)
- Future optimization: Add composite index on (user_id, created_at DESC) if sorting becomes bottleneck

---

## Data Retention Policy

### MVP Policy

- **Retention Period**: Indefinite (tasks persist until explicitly deleted by user)
- **Soft Delete**: NOT implemented (hard delete only)
- **Backup**: Handled by Neon automatic backups (point-in-time recovery)
- **Archival**: NOT implemented for MVP

### Post-MVP Considerations

- **Soft Delete**: Add is_deleted flag and deleted_at timestamp
- **Auto-Archive**: Move tasks older than X months to archive table
- **GDPR Compliance**: Add data export and deletion workflows when users table is added

---

## Testing Strategy

### Database Schema Tests (Manual for MVP)

1. **Verify table creation**:
   ```sql
   SELECT table_name FROM information_schema.tables
   WHERE table_schema = 'public' AND table_name = 'tasks';
   ```
   - Expected: tasks table exists

2. **Verify columns**:
   ```sql
   SELECT column_name, data_type, character_maximum_length, is_nullable
   FROM information_schema.columns
   WHERE table_name = 'tasks';
   ```
   - Expected: All 7 columns with correct types and constraints

3. **Verify indexes**:
   ```sql
   SELECT indexname, indexdef FROM pg_indexes
   WHERE tablename = 'tasks';
   ```
   - Expected: idx_tasks_user_id, idx_tasks_completed exist

### Data Validation Tests

See feature specification (spec.md) for complete acceptance scenarios testing:
- Task creation with valid/invalid data
- Update operations with ownership validation
- Deletion with ownership validation
- Filtering and sorting queries

---

## Summary

This data model defines a single **Task** entity with:
- 7 attributes (id, user_id, title, description, completed, created_at, updated_at)
- 2 indexes for query performance (user_id, completed)
- Comprehensive validation rules (length limits, required fields)
- Simple state machine (PENDING ↔ COMPLETED)
- Clear ownership model (many tasks belong to one user)

**Ready for Implementation**: This data model is complete and ready for code generation in the implementation phase.
