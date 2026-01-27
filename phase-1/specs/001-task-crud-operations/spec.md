# Phase 1 Specification – In-Memory Python Console Todo App

## Feature: Task CRUD Operations

---

## User Stories

- As a user, I can add a new task
- As a user, I can view all tasks
- As a user, I can update a task
- As a user, I can delete a task
- As a user, I can mark a task as complete

---

## Data Model

### Task

| Field       | Type     | Description              |
|-------------|----------|--------------------------|
| id          | int      | Unique task identifier   |
| title       | str      | Short title (required)   |
| description | str      | Optional details         |
| completed   | bool     | Completion status        |
| created_at  | datetime | Creation timestamp       |
| updated_at  | datetime | Last update timestamp    |

---

## Functional Requirements

### Add Task

- User enters title and optional description
- Title is required (1–200 characters)
- Task is stored in memory
- Task ID is auto-generated
- Success message is displayed

### View Tasks

- Displays all tasks
- Shows: ID, Title, Status, Created Date
- If no tasks → show “No tasks found”

### Update Task

- User selects task by ID
- User can change title and/or description
- If ID not found → show error
- Updated timestamp is refreshed

### Delete Task

- User selects task by ID
- If ID not found → show error
- Task is removed from memory
- Confirmation message shown

### Mark Task Complete

- User selects task by ID
- Toggles completion state
- If ID not found → show error
- Status updated and displayed

---

## CLI Behavior

### Main Menu

- Add Task
- View Tasks
- Update Task
- Delete Task
- Mark Task Complete
- Exit

---

## Error Handling

- Invalid input → friendly message
- Non-numeric ID → prompt again
- Empty title → rejected

---

## Constraints

- In-memory only
- Python 3.13+
- No external services
- No file persistence

---

## Acceptance Criteria

- All 5 features work
- No crashes on invalid input
- Clean readable output
- Spec fully drives implementation

---

## Implementation Notes

- Repository pattern for in-memory storage
- Service layer for business logic
- CLI layer for user interaction
- Models for data structures

---

## Ready for Claude Code

When this spec is approved, generate:
> “Implement Phase 1 based on this specification.”