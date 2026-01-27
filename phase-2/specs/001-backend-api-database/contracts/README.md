# API Documentation: Todo Backend API

**Version**: 1.0.0
**Base URL (Development)**: http://localhost:8000
**Base URL (Production)**: https://api.yourdomain.com

---

## Overview

This RESTful API provides task management operations with user-scoped data isolation. All endpoints follow REST conventions and return JSON responses.

**Key Features**:
- ✅ Create, read, update, delete tasks
- ✅ Filter tasks by completion status (all, pending, completed)
- ✅ Sort tasks by creation date or title
- ✅ Toggle task completion status
- ✅ Data isolation (users only see their own tasks)

**Authentication**: Currently accepts `user_id` in URL path. JWT token authentication will be added in Module 2.

---

## Endpoints Summary

| Method | Endpoint | Purpose | Auth Required |
|--------|----------|---------|---------------|
| GET | /api/{user_id}/tasks | List all tasks | Yes (Module 2) |
| POST | /api/{user_id}/tasks | Create new task | Yes (Module 2) |
| GET | /api/{user_id}/tasks/{id} | Get single task | Yes (Module 2) |
| PUT | /api/{user_id}/tasks/{id} | Update task | Yes (Module 2) |
| PATCH | /api/{user_id}/tasks/{id}/complete | Toggle completion | Yes (Module 2) |
| DELETE | /api/{user_id}/tasks/{id} | Delete task | Yes (Module 2) |

---

## 1. List All Tasks

Retrieve all tasks for a specific user with optional filtering and sorting.

**Endpoint**: `GET /api/{user_id}/tasks`

**Path Parameters**:
- `user_id` (required): Unique identifier of the user

**Query Parameters**:
- `status` (optional): Filter by completion status
  - Values: `all` (default), `pending`, `completed`
  - Example: `?status=pending`
- `sort` (optional): Sort order
  - Values: `created` (default), `title`, `updated`
  - Example: `?sort=title`

**Example Request**:
```bash
curl -X GET "http://localhost:8000/api/user123/tasks?status=pending&sort=title"
```

**Example Response** (200 OK):
```json
[
  {
    "id": 1,
    "user_id": "user123",
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": false,
    "created_at": "2026-01-25T10:30:00Z",
    "updated_at": "2026-01-25T10:30:00Z"
  },
  {
    "id": 2,
    "user_id": "user123",
    "title": "Call dentist",
    "description": null,
    "completed": false,
    "created_at": "2026-01-25T09:00:00Z",
    "updated_at": "2026-01-25T09:00:00Z"
  }
]
```

**Empty List** (200 OK):
```json
[]
```

---

## 2. Create New Task

Create a new task for a specific user.

**Endpoint**: `POST /api/{user_id}/tasks`

**Path Parameters**:
- `user_id` (required): Unique identifier of the user

**Request Body**:
```json
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"
}
```

**Field Constraints**:
- `title` (required): 1-200 characters
- `description` (optional): Max 1000 characters

**Example Request**:
```bash
curl -X POST "http://localhost:8000/api/user123/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Buy groceries",
    "description": "Milk, eggs, bread"
  }'
```

**Example Response** (201 Created):
```json
{
  "id": 1,
  "user_id": "user123",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "created_at": "2026-01-25T10:30:00Z",
  "updated_at": "2026-01-25T10:30:00Z"
}
```

**Error Response** (400 Bad Request - Title Too Long):
```json
{
  "detail": "Title must be at most 200 characters",
  "error_code": "VALIDATION_ERROR",
  "field": "title"
}
```

**Error Response** (400 Bad Request - Title Missing):
```json
{
  "detail": "Title is required",
  "error_code": "VALIDATION_ERROR",
  "field": "title"
}
```

---

## 3. Get Single Task

Retrieve a specific task by ID (with ownership validation).

**Endpoint**: `GET /api/{user_id}/tasks/{id}`

**Path Parameters**:
- `user_id` (required): Unique identifier of the user
- `id` (required): Task ID

**Example Request**:
```bash
curl -X GET "http://localhost:8000/api/user123/tasks/1"
```

**Example Response** (200 OK):
```json
{
  "id": 1,
  "user_id": "user123",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "created_at": "2026-01-25T10:30:00Z",
  "updated_at": "2026-01-25T10:30:00Z"
}
```

**Error Response** (404 Not Found):
```json
{
  "detail": "Task not found",
  "error_code": "NOT_FOUND"
}
```

---

## 4. Update Task

Update task title and/or description (with ownership validation).

**Endpoint**: `PUT /api/{user_id}/tasks/{id}`

**Path Parameters**:
- `user_id` (required): Unique identifier of the user
- `id` (required): Task ID

**Request Body**:
```json
{
  "title": "Buy groceries and fruits",
  "description": "Milk, eggs, bread, apples, bananas"
}
```

**Field Constraints**:
- `title` (optional): 1-200 characters if provided
- `description` (optional): Max 1000 characters if provided
- At least one field must be provided

**Example Request** (Update Both):
```bash
curl -X PUT "http://localhost:8000/api/user123/tasks/1" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Buy groceries and fruits",
    "description": "Milk, eggs, bread, apples, bananas"
  }'
```

**Example Request** (Update Title Only):
```bash
curl -X PUT "http://localhost:8000/api/user123/tasks/1" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Buy groceries and fruits"
  }'
```

**Example Response** (200 OK):
```json
{
  "id": 1,
  "user_id": "user123",
  "title": "Buy groceries and fruits",
  "description": "Milk, eggs, bread, apples, bananas",
  "completed": false,
  "created_at": "2026-01-25T10:30:00Z",
  "updated_at": "2026-01-25T12:00:00Z"
}
```

**Note**: The `updated_at` timestamp is automatically updated.

---

## 5. Toggle Task Completion

Toggle task between pending (false) and completed (true).

**Endpoint**: `PATCH /api/{user_id}/tasks/{id}/complete`

**Path Parameters**:
- `user_id` (required): Unique identifier of the user
- `id` (required): Task ID

**Request Body**: None

**Example Request**:
```bash
curl -X PATCH "http://localhost:8000/api/user123/tasks/1/complete"
```

**Example Response** (200 OK - Now Completed):
```json
{
  "id": 1,
  "user_id": "user123",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": true,
  "created_at": "2026-01-25T10:30:00Z",
  "updated_at": "2026-01-25T14:00:00Z"
}
```

**Example Response** (200 OK - Toggled Back to Pending):
```json
{
  "id": 1,
  "user_id": "user123",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "created_at": "2026-01-25T10:30:00Z",
  "updated_at": "2026-01-25T15:00:00Z"
}
```

**Behavior**: If `completed=false`, it will be set to `true`. If `completed=true`, it will be set to `false`.

---

## 6. Delete Task

Permanently delete a task (with ownership validation).

**Endpoint**: `DELETE /api/{user_id}/tasks/{id}`

**Path Parameters**:
- `user_id` (required): Unique identifier of the user
- `id` (required): Task ID

**Example Request**:
```bash
curl -X DELETE "http://localhost:8000/api/user123/tasks/1"
```

**Example Response** (204 No Content):
- No response body
- HTTP status 204 indicates successful deletion

**Error Response** (404 Not Found):
```json
{
  "detail": "Task not found",
  "error_code": "NOT_FOUND"
}
```

---

## HTTP Status Codes

| Status Code | Meaning | When Used |
|-------------|---------|-----------|
| 200 OK | Success | GET, PUT, PATCH operations |
| 201 Created | Resource created | POST operation (task created) |
| 204 No Content | Success (no body) | DELETE operation (task deleted) |
| 400 Bad Request | Validation error | Invalid input data (e.g., title too long) |
| 401 Unauthorized | Missing/invalid auth | No auth token (Module 2) |
| 404 Not Found | Resource not found | Task doesn't exist or doesn't belong to user |
| 422 Unprocessable Entity | Invalid JSON | Malformed request body |
| 500 Internal Server Error | Server error | Unexpected backend error |

---

## Error Response Format

All error responses follow this consistent format:

```json
{
  "detail": "Human-readable error message",
  "error_code": "MACHINE_READABLE_CODE",
  "field": "fieldname"
}
```

**Fields**:
- `detail` (string): User-friendly error message
- `error_code` (string): Machine-readable error code for frontend handling
- `field` (string, optional): Which field caused the error (for validation errors)

### Error Codes

| Error Code | HTTP Status | Meaning |
|------------|-------------|---------|
| `VALIDATION_ERROR` | 400 | Input validation failed (e.g., title too long) |
| `NOT_FOUND` | 404 | Task not found or not owned by user |
| `INVALID_JSON` | 422 | Request body is not valid JSON |
| `INTERNAL_ERROR` | 500 | Unexpected server error |

---

## Data Validation Rules

### Title Validation

- **Required**: Yes (cannot be empty)
- **Minimum Length**: 1 character
- **Maximum Length**: 200 characters
- **Trimming**: Leading/trailing whitespace is trimmed
- **Allowed Characters**: Any UTF-8 (including emojis)

**Examples**:
- ✅ "Buy groceries" (valid)
- ✅ "📧 Send email" (valid - emojis allowed)
- ✅ "A" (valid - minimum 1 character)
- ❌ "" (invalid - empty string)
- ❌ "   " (invalid - whitespace only)
- ❌ "{201 characters...}" (invalid - exceeds max length)

### Description Validation

- **Required**: No (nullable)
- **Maximum Length**: 1000 characters
- **Trimming**: NOT trimmed (preserves formatting)
- **Null vs Empty**: Both `null` and `""` are accepted

**Examples**:
- ✅ `null` (valid - no description)
- ✅ `""` (valid - empty description)
- ✅ "Buy milk, eggs, bread" (valid)
- ✅ "Multi-line\nwith newlines" (valid)
- ❌ "{1001 characters...}" (invalid - exceeds max length)

---

## Data Isolation & Security

### Current Implementation (Module 1)

- **User ID**: Passed in URL path (`/api/{user_id}/tasks`)
- **Validation**: All operations verify task belongs to specified user_id
- **Enforcement**: API layer checks `task.user_id === url.user_id`
- **Cross-User Access**: Attempting to access another user's task returns 404 Not Found

**Example**:
- User A creates task with ID 1
- User B attempts: `GET /api/userB/tasks/1`
- Result: 404 Not Found (even though task exists, it belongs to User A)

### Future Enhancement (Module 2 - Authentication)

- JWT tokens will be required in `Authorization` header
- User ID will be extracted from JWT token (not URL path)
- URL path will change to `/api/tasks` (no user_id in path)

---

## Rate Limiting

**Current**: No rate limiting (MVP)
**Future**: To be implemented based on usage patterns

---

## CORS Configuration

**Allowed Origins**:
- Development: `http://localhost:3000` (Next.js frontend)
- Production: `https://your-app.vercel.app`

**Allowed Methods**: GET, POST, PUT, PATCH, DELETE, OPTIONS
**Allowed Headers**: Content-Type, Authorization (Module 2)
**Credentials**: Supported (for cookies/auth tokens)

---

## Testing the API

### Using cURL

See examples above for each endpoint.

### Using Postman

1. Import OpenAPI specification: `openapi.yaml`
2. Set base URL: `http://localhost:8000`
3. Create requests for each endpoint
4. Test with valid and invalid data

### Automated Testing

Manual testing checklist provided in `quickstart.md`. Automated integration tests deferred to post-MVP.

---

## Common Issues & Troubleshooting

### 1. CORS Errors

**Problem**: Frontend gets CORS error when making requests

**Solution**: Ensure CORS_ORIGINS environment variable includes frontend URL:
```bash
CORS_ORIGINS=http://localhost:3000,https://your-app.vercel.app
```

### 2. Connection Refused

**Problem**: `curl: (7) Failed to connect to localhost port 8000`

**Solution**: Ensure backend is running:
```bash
uvicorn src.main:app --reload --port 8000
```

### 3. 404 on Valid Task ID

**Problem**: GET /api/user123/tasks/1 returns 404 even though task exists

**Solution**: Verify user_id matches - tasks are user-scoped:
```bash
# Check which user owns task ID 1
psql $DATABASE_URL -c "SELECT user_id FROM tasks WHERE id = 1;"
```

### 4. 422 Unprocessable Entity

**Problem**: POST request returns 422

**Solution**: Ensure request body is valid JSON and Content-Type header is set:
```bash
curl -X POST "http://localhost:8000/api/user123/tasks" \
  -H "Content-Type: application/json" \  # ← Required header
  -d '{"title": "Test"}'  # ← Valid JSON
```

---

## Changelog

### Version 1.0.0 (2026-01-25)

- Initial API release
- 6 endpoints: List, Create, Get, Update, Toggle Complete, Delete
- Filtering by status (all, pending, completed)
- Sorting by created, title, updated
- Data isolation (user-scoped queries)

### Upcoming (Module 2 - Authentication)

- JWT token authentication
- Remove user_id from URL path
- Add Authorization header requirement
- User registration and login endpoints

---

## API Schema

For the complete OpenAPI 3.0 specification, see: [openapi.yaml](./openapi.yaml)

You can visualize this schema using:
- **Swagger UI**: https://editor.swagger.io/ (paste openapi.yaml)
- **Redoc**: https://redocly.github.io/redoc/ (paste openapi.yaml)
- **Postman**: Import openapi.yaml directly

---

## Support

**Questions**: Open an issue in the GitHub repository
**Bug Reports**: Provide cURL command + expected vs actual response
**Feature Requests**: Submit via GitHub discussions

---

**Last Updated**: 2026-01-25
**API Version**: 1.0.0
