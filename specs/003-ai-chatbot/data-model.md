# Data Model: AI-Powered Todo Chatbot (Phase 3)

**Feature**: `003-ai-chatbot`
**Date**: 2026-02-02

## Entity Relationship Diagram

```
┌─────────────┐       ┌──────────────────┐       ┌─────────────┐
│    User     │       │   Conversation   │       │   Message   │
│  (Phase 2)  │       │                  │       │             │
├─────────────┤       ├──────────────────┤       ├─────────────┤
│ id (UUID)   │──1:N──│ id (SERIAL)      │──1:N──│ id (SERIAL) │
│ email       │       │ user_id (FK)     │       │ conv_id(FK) │
│ name        │       │ title            │       │ role        │
│ ...         │       │ created_at       │       │ content     │
└─────────────┘       │ updated_at       │       │ tool_calls  │
                      └──────────────────┘       │ created_at  │
                                                 └─────────────┘
                                                       │
                                                       │
                      ┌──────────────────┐             │ References
                      │      Task        │◄────────────┘ (via tools)
                      │    (Phase 2)     │
                      ├──────────────────┤
                      │ id (SERIAL)      │
                      │ user_id (VARCHAR)│
                      │ title            │
                      │ description      │
                      │ completed        │
                      └──────────────────┘
```

## New Entities

### Conversation

Represents a chat session belonging to a user.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | SERIAL | PRIMARY KEY | Auto-incrementing ID |
| user_id | VARCHAR(255) | NOT NULL, INDEX | References Better Auth user |
| title | VARCHAR(255) | DEFAULT 'New Conversation' | Display title |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMP | DEFAULT NOW() | Last activity timestamp |

**Indexes**:
- `idx_conversations_user_id` on `user_id` (for user's conversations lookup)
- `idx_conversations_updated_at` on `updated_at` (for recent conversations)

**SQLModel Definition**:
```python
class Conversation(SQLModel, table=True):
    __tablename__ = "conversations"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True, nullable=False, max_length=255)
    title: str = Field(default="New Conversation", max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    messages: List["Message"] = Relationship(back_populates="conversation")
```

### Message

Represents a single message in a conversation.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | SERIAL | PRIMARY KEY | Auto-incrementing ID |
| conversation_id | INTEGER | FOREIGN KEY, NOT NULL | References conversation |
| role | VARCHAR(50) | NOT NULL, CHECK | 'user', 'assistant', or 'tool' |
| content | TEXT | NOT NULL | Message content |
| tool_calls | JSONB | NULLABLE | OpenAI tool call data |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation timestamp |

**Indexes**:
- `idx_messages_conversation_id` on `conversation_id` (for message lookup)
- `idx_messages_created_at` on `created_at` (for ordering)

**Constraints**:
- `fk_messages_conversation` FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
- `chk_messages_role` CHECK (role IN ('user', 'assistant', 'tool'))

**SQLModel Definition**:
```python
class Message(SQLModel, table=True):
    __tablename__ = "messages"

    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversations.id", nullable=False)
    role: str = Field(max_length=50, nullable=False)  # 'user', 'assistant', 'tool'
    content: str = Field(nullable=False)
    tool_calls: Optional[dict] = Field(default=None, sa_column=Column(JSON))
    created_at: datetime = Field(default_factory=datetime.utcnow)

    conversation: Optional[Conversation] = Relationship(back_populates="messages")
```

## Existing Entities (Phase 2 - Unchanged)

### Task

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | SERIAL | PRIMARY KEY | Auto-incrementing ID |
| user_id | VARCHAR(255) | NOT NULL, INDEX | Owner user ID |
| title | VARCHAR(500) | NOT NULL | Task title |
| description | TEXT | NULLABLE | Task description |
| completed | BOOLEAN | DEFAULT FALSE | Completion status |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMP | DEFAULT NOW() | Last update timestamp |

**Note**: Phase 3 tools will interact with this existing entity via the TaskRepository.

## State Transitions

### Conversation Lifecycle

```
┌─────────────┐     User sends      ┌─────────────┐
│   (none)    │────first message───►│   Created   │
└─────────────┘                     └──────┬──────┘
                                           │
                                           │ User sends messages
                                           ▼
                                    ┌─────────────┐
                                    │   Active    │◄───┐
                                    └──────┬──────┘    │
                                           │           │
                                           │ More      │
                                           │ messages  │
                                           └───────────┘
```

### Message Types

| Role | Source | Contains Tool Calls | Example |
|------|--------|---------------------|---------|
| user | End user | No | "Add buy milk to my tasks" |
| assistant | OpenAI | Yes (optional) | "✓ Created task: buy milk" |
| tool | Tool execution | No | {"success": true, "data": {...}} |

## Validation Rules

### Conversation
- `user_id`: Required, must match authenticated user
- `title`: Max 255 characters, auto-generated from first message if not provided

### Message
- `conversation_id`: Required, must exist and belong to user
- `role`: Must be one of 'user', 'assistant', 'tool'
- `content`: Required, max 10000 characters
- `tool_calls`: Valid JSON if present

## Query Patterns

### Load Conversation with Recent Messages
```sql
SELECT c.*, m.*
FROM conversations c
LEFT JOIN (
    SELECT *
    FROM messages
    WHERE conversation_id = :conv_id
    ORDER BY created_at DESC
    LIMIT 50
) m ON m.conversation_id = c.id
WHERE c.id = :conv_id AND c.user_id = :user_id;
```

### List User's Conversations
```sql
SELECT id, title, updated_at
FROM conversations
WHERE user_id = :user_id
ORDER BY updated_at DESC
LIMIT 20;
```

### Insert Message and Update Conversation
```sql
BEGIN;
INSERT INTO messages (conversation_id, role, content, tool_calls)
VALUES (:conv_id, :role, :content, :tool_calls);

UPDATE conversations
SET updated_at = NOW()
WHERE id = :conv_id;
COMMIT;
```

## Migration Strategy

### Phase 3 Migration Script
```sql
-- Create conversations table
CREATE TABLE IF NOT EXISTS conversations (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    title VARCHAR(255) DEFAULT 'New Conversation',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_conversations_user_id ON conversations(user_id);
CREATE INDEX idx_conversations_updated_at ON conversations(updated_at);

-- Create messages table
CREATE TABLE IF NOT EXISTS messages (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    role VARCHAR(50) NOT NULL CHECK (role IN ('user', 'assistant', 'tool')),
    content TEXT NOT NULL,
    tool_calls JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX idx_messages_created_at ON messages(created_at);
```

### Rollback Script
```sql
DROP TABLE IF EXISTS messages CASCADE;
DROP TABLE IF EXISTS conversations CASCADE;
```
