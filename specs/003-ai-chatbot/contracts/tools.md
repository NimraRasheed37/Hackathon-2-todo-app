# AI Agent Tool Contracts

**Feature**: `003-ai-chatbot`
**Date**: 2026-02-02

## Overview

These tools are exposed to the OpenAI agent for task management operations. All tools enforce user isolation and return structured responses.

## Tool Response Format

All tools return a consistent response structure:

```json
{
  "success": true | false,
  "data": { ... },      // Present when success=true
  "message": "...",     // Human-readable description
  "error": "..."        // Present when success=false
}
```

---

## Tool 1: add_task

**Purpose**: Create a new task for the authenticated user

### OpenAI Function Definition

```json
{
  "type": "function",
  "function": {
    "name": "add_task",
    "description": "Add a new task for the user. Use this when the user wants to create, add, or remember something as a task.",
    "parameters": {
      "type": "object",
      "properties": {
        "title": {
          "type": "string",
          "description": "The title/name of the task to create (max 500 characters)"
        },
        "description": {
          "type": "string",
          "description": "Optional detailed description of the task"
        }
      },
      "required": ["title"]
    }
  }
}
```

### Implementation Contract

```python
async def add_task(
    session: Session,
    user_id: str,  # Injected from JWT, not from AI
    title: str,
    description: Optional[str] = None
) -> dict:
    """
    Preconditions:
      - user_id is validated from JWT
      - title is non-empty, max 500 chars

    Postconditions:
      - New task created with provided title
      - Task belongs to user_id
      - Returns created task data

    Errors:
      - VALIDATION_ERROR: title empty or too long
      - DATABASE_ERROR: insertion failed
    """
```

### Response Examples

**Success**:
```json
{
  "success": true,
  "data": {
    "task_id": 42,
    "title": "buy milk",
    "description": null,
    "completed": false
  },
  "message": "Task created successfully"
}
```

**Error**:
```json
{
  "success": false,
  "error": "Task title cannot exceed 500 characters",
  "message": "Failed to create task"
}
```

---

## Tool 2: list_tasks

**Purpose**: List all tasks for the authenticated user

### OpenAI Function Definition

```json
{
  "type": "function",
  "function": {
    "name": "list_tasks",
    "description": "List all tasks for the user. Can filter by status (pending, completed, or all).",
    "parameters": {
      "type": "object",
      "properties": {
        "status": {
          "type": "string",
          "enum": ["all", "pending", "completed"],
          "description": "Filter tasks by status. Default is 'all'."
        }
      },
      "required": []
    }
  }
}
```

### Implementation Contract

```python
async def list_tasks(
    session: Session,
    user_id: str,  # Injected from JWT
    status: Optional[str] = "all"
) -> dict:
    """
    Preconditions:
      - user_id is validated from JWT
      - status is one of: 'all', 'pending', 'completed'

    Postconditions:
      - Returns list of user's tasks
      - If status specified, filters accordingly

    Errors:
      - VALIDATION_ERROR: invalid status value
      - DATABASE_ERROR: query failed
    """
```

### Response Examples

**Success (has tasks)**:
```json
{
  "success": true,
  "data": {
    "tasks": [
      {"id": 1, "title": "buy milk", "completed": false},
      {"id": 2, "title": "call mom", "completed": true}
    ],
    "count": 2
  },
  "message": "Found 2 tasks"
}
```

**Success (no tasks)**:
```json
{
  "success": true,
  "data": {
    "tasks": [],
    "count": 0
  },
  "message": "No tasks found"
}
```

---

## Tool 3: complete_task

**Purpose**: Mark a task as completed

### OpenAI Function Definition

```json
{
  "type": "function",
  "function": {
    "name": "complete_task",
    "description": "Mark a task as completed. Can identify task by ID or by partial title match.",
    "parameters": {
      "type": "object",
      "properties": {
        "task_identifier": {
          "type": "string",
          "description": "Task ID (number) or partial title to match"
        }
      },
      "required": ["task_identifier"]
    }
  }
}
```

### Implementation Contract

```python
async def complete_task(
    session: Session,
    user_id: str,  # Injected from JWT
    task_identifier: str
) -> dict:
    """
    Preconditions:
      - user_id is validated from JWT
      - task_identifier is non-empty

    Postconditions:
      - Task matching identifier is marked completed
      - Only user's own tasks can be completed

    Errors:
      - NOT_FOUND: no matching task
      - AMBIGUOUS: multiple tasks match (returns candidates)
      - DATABASE_ERROR: update failed
    """
```

### Response Examples

**Success**:
```json
{
  "success": true,
  "data": {
    "task_id": 42,
    "title": "buy milk",
    "completed": true
  },
  "message": "Task marked as completed"
}
```

**Not Found**:
```json
{
  "success": false,
  "error": "NOT_FOUND",
  "message": "No task found matching 'nonexistent'"
}
```

**Ambiguous**:
```json
{
  "success": false,
  "error": "AMBIGUOUS",
  "data": {
    "candidates": [
      {"id": 1, "title": "buy milk"},
      {"id": 2, "title": "buy bread"}
    ]
  },
  "message": "Multiple tasks match 'buy'. Please be more specific."
}
```

---

## Tool 4: delete_task

**Purpose**: Permanently delete a task

### OpenAI Function Definition

```json
{
  "type": "function",
  "function": {
    "name": "delete_task",
    "description": "Delete a task permanently. Can identify task by ID or by partial title match.",
    "parameters": {
      "type": "object",
      "properties": {
        "task_identifier": {
          "type": "string",
          "description": "Task ID (number) or partial title to match"
        }
      },
      "required": ["task_identifier"]
    }
  }
}
```

### Implementation Contract

```python
async def delete_task(
    session: Session,
    user_id: str,  # Injected from JWT
    task_identifier: str
) -> dict:
    """
    Preconditions:
      - user_id is validated from JWT
      - task_identifier is non-empty

    Postconditions:
      - Task matching identifier is deleted
      - Only user's own tasks can be deleted

    Errors:
      - NOT_FOUND: no matching task
      - AMBIGUOUS: multiple tasks match
      - DATABASE_ERROR: deletion failed
    """
```

### Response Examples

**Success**:
```json
{
  "success": true,
  "data": {
    "task_id": 42,
    "title": "buy milk"
  },
  "message": "Task deleted successfully"
}
```

---

## Tool 5: update_task

**Purpose**: Update a task's properties

### OpenAI Function Definition

```json
{
  "type": "function",
  "function": {
    "name": "update_task",
    "description": "Update a task's title or description. Can identify task by ID or partial title match.",
    "parameters": {
      "type": "object",
      "properties": {
        "task_identifier": {
          "type": "string",
          "description": "Task ID (number) or partial title to match"
        },
        "new_title": {
          "type": "string",
          "description": "New title for the task"
        },
        "new_description": {
          "type": "string",
          "description": "New description for the task"
        }
      },
      "required": ["task_identifier"]
    }
  }
}
```

### Implementation Contract

```python
async def update_task(
    session: Session,
    user_id: str,  # Injected from JWT
    task_identifier: str,
    new_title: Optional[str] = None,
    new_description: Optional[str] = None
) -> dict:
    """
    Preconditions:
      - user_id is validated from JWT
      - task_identifier is non-empty
      - At least one of new_title or new_description provided

    Postconditions:
      - Task matching identifier is updated
      - Only user's own tasks can be updated

    Errors:
      - NOT_FOUND: no matching task
      - AMBIGUOUS: multiple tasks match
      - VALIDATION_ERROR: no updates provided or title too long
      - DATABASE_ERROR: update failed
    """
```

### Response Examples

**Success**:
```json
{
  "success": true,
  "data": {
    "task_id": 42,
    "old_title": "buy milk",
    "new_title": "buy groceries",
    "description": null
  },
  "message": "Task updated successfully"
}
```

---

## Security Guarantees

1. **User Isolation**: `user_id` is ALWAYS injected from the JWT token, never from AI arguments
2. **Query Filtering**: All database queries include `WHERE user_id = :user_id`
3. **No Cross-User Access**: Tools cannot access another user's tasks under any circumstances
4. **Input Validation**: All inputs are validated before database operations
5. **Error Sanitization**: Internal errors are logged but not exposed to users

## Error Code Reference

| Code | HTTP Status | Description |
|------|-------------|-------------|
| VALIDATION_ERROR | 400 | Invalid input parameters |
| NOT_FOUND | 404 | Requested resource not found |
| AMBIGUOUS | 400 | Multiple matches, needs clarification |
| DATABASE_ERROR | 500 | Database operation failed |
| UNAUTHORIZED | 401 | Invalid or missing authentication |
