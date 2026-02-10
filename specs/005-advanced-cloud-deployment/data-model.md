# Data Model: Phase 5 - Advanced Cloud Deployment

**Feature**: `005-advanced-cloud-deployment`
**Date**: 2026-02-05
**Database**: Neon PostgreSQL

## Entity Relationship Diagram

```
┌──────────────┐       ┌──────────────┐       ┌──────────────┐
│    users     │       │    tasks     │       │     tags     │
├──────────────┤       ├──────────────┤       ├──────────────┤
│ id (PK)      │──┐    │ id (PK)      │──┐    │ id (PK)      │
│ email        │  │    │ user_id (FK) │◄─┘    │ user_id (FK) │
│ name         │  │    │ title        │       │ name         │
│ ...          │  │    │ description  │       │ color        │
└──────────────┘  │    │ status       │       │ icon         │
                  │    │ priority     │       │ usage_count  │
                  │    │ due_date     │       └──────┬───────┘
                  │    │ recurrence_* │              │
                  │    │ parent_id    │              │
                  │    │ search_vector│       ┌──────▼───────┐
                  │    └──────┬───────┘       │  task_tags   │
                  │           │               ├──────────────┤
                  │           │               │ task_id (FK) │◄┐
                  │           │               │ tag_id (FK)  │ │
                  │           │               └──────────────┘ │
                  │           │                                │
                  │           └────────────────────────────────┘
                  │
                  │    ┌────────────────────┐
                  │    │  task_recurrences  │
                  │    ├────────────────────┤
                  │    │ id (PK)            │
                  └───►│ task_id (FK)       │
                       │ pattern (JSONB)    │
                       │ next_occurrence    │
                       │ last_generated     │
                       │ total_occurrences  │
                       │ is_active          │
                       └────────────────────┘

                  ┌────────────────────┐       ┌──────────────────┐
                  │   task_reminders   │       │   notifications  │
                  ├────────────────────┤       ├──────────────────┤
                  │ id (PK)            │       │ id (PK)          │
                  │ task_id (FK)       │       │ user_id (FK)     │
                  │ user_id (FK)       │       │ type             │
                  │ reminder_type      │       │ title            │
                  │ relative_minutes   │       │ message          │
                  │ absolute_time      │       │ read             │
                  │ channels[]         │       │ created_at       │
                  │ status             │       └──────────────────┘
                  │ scheduled_at       │
                  │ sent_at            │
                  └────────────────────┘

                  ┌────────────────────┐
                  │     audit_log      │
                  ├────────────────────┤
                  │ id (PK)            │
                  │ event_id           │
                  │ event_type         │
                  │ aggregate_id       │
                  │ user_id            │
                  │ payload (JSONB)    │
                  │ timestamp          │
                  └────────────────────┘
```

## Entity Definitions

### tasks (Updated)

Existing `tasks` table with new columns for Phase 5 features.

```sql
-- New columns to add to existing tasks table
ALTER TABLE tasks ADD COLUMN priority VARCHAR(20) DEFAULT 'none';
ALTER TABLE tasks ADD COLUMN due_date TIMESTAMPTZ;
ALTER TABLE tasks ADD COLUMN recurrence_pattern JSONB;
ALTER TABLE tasks ADD COLUMN parent_task_id UUID REFERENCES tasks(id);
ALTER TABLE tasks ADD COLUMN occurrence_number INTEGER DEFAULT 1;
ALTER TABLE tasks ADD COLUMN search_vector tsvector;
ALTER TABLE tasks ADD COLUMN version INTEGER DEFAULT 1;

-- Indexes
CREATE INDEX idx_tasks_priority ON tasks(priority);
CREATE INDEX idx_tasks_due_date ON tasks(due_date);
CREATE INDEX idx_tasks_parent ON tasks(parent_task_id);
CREATE INDEX idx_tasks_search ON tasks USING GIN(search_vector);
CREATE INDEX idx_tasks_user_status ON tasks(user_id, status);
```

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK, DEFAULT gen_random_uuid() | Task identifier |
| user_id | UUID | FK users(id), NOT NULL | Owner |
| title | VARCHAR(255) | NOT NULL | Task title |
| description | TEXT | | Task details |
| status | VARCHAR(20) | DEFAULT 'pending' | pending, in_progress, completed |
| **priority** | VARCHAR(20) | DEFAULT 'none' | none, low, medium, high, critical |
| **due_date** | TIMESTAMPTZ | | When task is due |
| **recurrence_pattern** | JSONB | | Recurrence configuration |
| **parent_task_id** | UUID | FK tasks(id) | For recurring task instances |
| **occurrence_number** | INTEGER | DEFAULT 1 | Instance number in series |
| **search_vector** | tsvector | | Full-text search index |
| **version** | INTEGER | DEFAULT 1 | Optimistic locking |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | |
| updated_at | TIMESTAMPTZ | DEFAULT NOW() | |

**Recurrence Pattern JSON Schema**:
```json
{
  "frequency": "daily|weekly|monthly|yearly|custom",
  "interval": 1,
  "daysOfWeek": [0, 2, 4],
  "dayOfMonth": 15,
  "endDate": "2026-12-31",
  "maxOccurrences": 10
}
```

---

### tags (New)

User-defined labels for task organization.

```sql
CREATE TABLE tags (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  name VARCHAR(50) NOT NULL,
  color VARCHAR(7) DEFAULT '#808080',
  icon VARCHAR(10),
  usage_count INTEGER DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(user_id, name)
);

CREATE INDEX idx_tags_user ON tags(user_id);
```

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Tag identifier |
| user_id | UUID | FK users(id), NOT NULL | Owner |
| name | VARCHAR(50) | NOT NULL, UNIQUE per user | Tag name |
| color | VARCHAR(7) | DEFAULT '#808080' | Hex color code |
| icon | VARCHAR(10) | | Emoji or icon identifier |
| usage_count | INTEGER | DEFAULT 0 | Number of tasks using tag |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | |

---

### task_tags (New)

Junction table for many-to-many task-tag relationship.

```sql
CREATE TABLE task_tags (
  task_id UUID REFERENCES tasks(id) ON DELETE CASCADE,
  tag_id UUID REFERENCES tags(id) ON DELETE CASCADE,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  PRIMARY KEY (task_id, tag_id)
);

CREATE INDEX idx_task_tags_tag ON task_tags(tag_id);
```

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| task_id | UUID | FK tasks(id), PK | Task reference |
| tag_id | UUID | FK tags(id), PK | Tag reference |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | When tag was assigned |

---

### task_recurrences (New)

Tracks active recurrence patterns and next scheduled occurrence.

```sql
CREATE TABLE task_recurrences (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  task_id UUID NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
  pattern JSONB NOT NULL,
  next_occurrence TIMESTAMPTZ,
  last_generated TIMESTAMPTZ,
  total_occurrences INTEGER DEFAULT 0,
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_recurrences_next ON task_recurrences(next_occurrence)
  WHERE is_active = true;
CREATE INDEX idx_recurrences_task ON task_recurrences(task_id);
```

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Recurrence identifier |
| task_id | UUID | FK tasks(id), NOT NULL | Original task |
| pattern | JSONB | NOT NULL | Recurrence configuration |
| next_occurrence | TIMESTAMPTZ | | When to create next instance |
| last_generated | TIMESTAMPTZ | | When last instance was created |
| total_occurrences | INTEGER | DEFAULT 0 | Count of instances created |
| is_active | BOOLEAN | DEFAULT true | Whether recurrence is active |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | |

---

### task_reminders (New)

Scheduled reminders for tasks.

```sql
CREATE TABLE task_reminders (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  task_id UUID NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES users(id),
  reminder_type VARCHAR(20) NOT NULL,
  relative_minutes INTEGER,
  absolute_time TIMESTAMPTZ,
  channels TEXT[] NOT NULL DEFAULT ARRAY['in_app'],
  status VARCHAR(20) DEFAULT 'pending',
  scheduled_at TIMESTAMPTZ NOT NULL,
  sent_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  CONSTRAINT valid_reminder_type CHECK (
    (reminder_type = 'relative' AND relative_minutes IS NOT NULL) OR
    (reminder_type = 'absolute' AND absolute_time IS NOT NULL)
  )
);

CREATE INDEX idx_reminders_scheduled ON task_reminders(scheduled_at)
  WHERE status = 'pending';
CREATE INDEX idx_reminders_task ON task_reminders(task_id);
CREATE INDEX idx_reminders_user ON task_reminders(user_id);
```

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Reminder identifier |
| task_id | UUID | FK tasks(id), NOT NULL | Associated task |
| user_id | UUID | FK users(id), NOT NULL | Reminder recipient |
| reminder_type | VARCHAR(20) | NOT NULL | 'relative' or 'absolute' |
| relative_minutes | INTEGER | | Minutes before due date |
| absolute_time | TIMESTAMPTZ | | Specific reminder time |
| channels | TEXT[] | DEFAULT ['in_app'] | Delivery channels |
| status | VARCHAR(20) | DEFAULT 'pending' | pending, sent, cancelled |
| scheduled_at | TIMESTAMPTZ | NOT NULL | Calculated trigger time |
| sent_at | TIMESTAMPTZ | | When reminder was sent |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | |

---

### notifications (New)

In-app notifications for users.

```sql
CREATE TABLE notifications (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  type VARCHAR(50) NOT NULL,
  title VARCHAR(255) NOT NULL,
  message TEXT,
  reference_type VARCHAR(50),
  reference_id UUID,
  read BOOLEAN DEFAULT false,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_notifications_user_unread ON notifications(user_id, created_at DESC)
  WHERE read = false;
```

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Notification identifier |
| user_id | UUID | FK users(id), NOT NULL | Recipient |
| type | VARCHAR(50) | NOT NULL | reminder, task_assigned, etc. |
| title | VARCHAR(255) | NOT NULL | Notification title |
| message | TEXT | | Notification body |
| reference_type | VARCHAR(50) | | 'task', 'reminder', etc. |
| reference_id | UUID | | ID of referenced entity |
| read | BOOLEAN | DEFAULT false | Read status |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | |

---

### audit_log (New)

Event sourcing for all task operations.

```sql
CREATE TABLE audit_log (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  event_id UUID NOT NULL UNIQUE,
  event_type VARCHAR(100) NOT NULL,
  event_version VARCHAR(10) DEFAULT '1.0',
  aggregate_type VARCHAR(50) NOT NULL,
  aggregate_id UUID NOT NULL,
  user_id UUID,
  correlation_id UUID,
  payload JSONB NOT NULL,
  metadata JSONB,
  timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_audit_aggregate ON audit_log(aggregate_type, aggregate_id);
CREATE INDEX idx_audit_user ON audit_log(user_id);
CREATE INDEX idx_audit_timestamp ON audit_log(timestamp DESC);
CREATE INDEX idx_audit_event_type ON audit_log(event_type);
```

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Log entry identifier |
| event_id | UUID | NOT NULL, UNIQUE | Original event ID |
| event_type | VARCHAR(100) | NOT NULL | TaskCreated, TaskUpdated, etc. |
| event_version | VARCHAR(10) | DEFAULT '1.0' | Event schema version |
| aggregate_type | VARCHAR(50) | NOT NULL | 'Task', 'Reminder', etc. |
| aggregate_id | UUID | NOT NULL | ID of affected entity |
| user_id | UUID | | User who triggered event |
| correlation_id | UUID | | Request correlation |
| payload | JSONB | NOT NULL | Event data |
| metadata | JSONB | | Additional context |
| timestamp | TIMESTAMPTZ | DEFAULT NOW() | Event time |

---

## Full-Text Search Configuration

```sql
-- Update search vector trigger
CREATE OR REPLACE FUNCTION update_task_search_vector()
RETURNS TRIGGER AS $$
BEGIN
  NEW.search_vector := to_tsvector('english',
    COALESCE(NEW.title, '') || ' ' ||
    COALESCE(NEW.description, '')
  );
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER task_search_update
  BEFORE INSERT OR UPDATE OF title, description ON tasks
  FOR EACH ROW EXECUTE FUNCTION update_task_search_vector();

-- Populate existing tasks
UPDATE tasks SET search_vector = to_tsvector('english',
  COALESCE(title, '') || ' ' || COALESCE(description, ''));
```

---

## State Transitions

### Task Status
```
pending → in_progress → completed
    ↓           ↓
  deleted    deleted
```

### Reminder Status
```
pending → sent
    ↓
cancelled (when task completed or deleted)
```

### Recurrence Status
```
active → inactive (when end date reached or max occurrences)
```

---

## Migration Strategy

### Migration Order (Zero-Downtime)

1. **Migration 001**: Add new columns to tasks (backward compatible)
2. **Migration 002**: Create tags table
3. **Migration 003**: Create task_tags junction table
4. **Migration 004**: Create task_recurrences table
5. **Migration 005**: Create task_reminders table
6. **Migration 006**: Create notifications table
7. **Migration 007**: Create audit_log table
8. **Migration 008**: Add full-text search trigger
9. **Migration 009**: Add indexes

### Rollback Plan

Each migration has a corresponding down migration. Rollback order is reverse of migration order.

---

## Validation Rules

| Entity | Field | Rule |
|--------|-------|------|
| tasks | priority | One of: none, low, medium, high, critical |
| tasks | due_date | Must be in the future (for new tasks) |
| tags | name | 1-50 characters, alphanumeric + spaces |
| tags | color | Valid hex color (#XXXXXX) |
| task_reminders | channels | Array of: in_app, email, push |
| task_reminders | relative_minutes | > 0 if type is 'relative' |
| task_recurrences | pattern | Valid JSON matching recurrence schema |
