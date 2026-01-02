# Data Model: Todo List Manager

**Feature Branch**: `001-todo-list-manager`  
**Created**: 2025-12-05
**Input**: Feature specification (`specs/001-todo-list-manager/spec.md`)

## Entities

### Task

Represents a single to-do item within the manager.

-   **Attributes**:
    -   `id` (string): A unique identifier for the task. Auto-generated upon creation (e.g., UUID).
    -   `title` (string): The primary description of the task. Mandatory.
    -   `description` (string, optional): Additional details or notes about the task. Optional.
    -   `created_date` (datetime string): Timestamp when the task was created. Auto-generated. Format: ISO 8601 (e.g., "YYYY-MM-DDTHH:MM:SS.ffffff").
    -   `completed` (boolean): Indicates whether the task has been marked as complete. Defaults to `false`.

-   **Relationships**: None (standalone entity).

-   **Validation Rules**:
    -   `title`: Must not be empty or consist only of whitespace.
    -   `id`: Must be unique across all tasks.
    -   `created_date`: Must be a valid datetime.

## Persistence

Tasks will be persisted as a list of Task objects (serialized to dictionaries) in a single JSON file named `todos.json`. Each Task object will be stored as a dictionary.

**Example `todos.json` structure:**

```json
[
  {
    "id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "created_date": "2025-12-05T10:00:00.000000",
    "completed": false
  },
  {
    "id": "f0e9d8c7-b6a5-4321-fedc-ba9876543210",
    "title": "Clean room",
    "description": null,
    "created_date": "2025-12-05T11:30:00.000000",
    "completed": true
  }
]
```
