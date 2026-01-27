# API Contracts: Frontend UI

This document describes the API contracts between the Next.js frontend and FastAPI backend.

## Base Configuration

```typescript
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
```

## Authentication

All task endpoints require JWT authentication:

```typescript
headers: {
  "Authorization": `Bearer ${token}`,
  "Content-Type": "application/json"
}
```

## Endpoints

### Health Check

```
GET /
```

**Response**: `200 OK`
```json
{
  "status": "healthy",
  "database": "connected"
}
```

---

### List Tasks

```
GET /api/{user_id}/tasks
```

**Query Parameters**:
| Param | Type | Default | Values |
|-------|------|---------|--------|
| status | string | "all" | "all", "pending", "completed" |
| sort | string | "created" | "created", "title", "updated" |

**Response**: `200 OK`
```json
[
  {
    "id": 1,
    "user_id": "uuid-string",
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": false,
    "created_at": "2026-01-26T10:00:00Z",
    "updated_at": "2026-01-26T10:00:00Z"
  }
]
```

**Errors**:
- `401 Unauthorized`: Missing or invalid token
- `403 Forbidden`: User ID mismatch

---

### Create Task

```
POST /api/{user_id}/tasks
```

**Request Body**:
```json
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"
}
```

**Validation**:
- `title`: Required, 1-200 characters
- `description`: Optional, max 1000 characters

**Response**: `201 Created`
```json
{
  "id": 1,
  "user_id": "uuid-string",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "created_at": "2026-01-26T10:00:00Z",
  "updated_at": "2026-01-26T10:00:00Z"
}
```

**Errors**:
- `400 Bad Request`: Validation error
- `401 Unauthorized`: Missing or invalid token
- `403 Forbidden`: User ID mismatch

---

### Get Task

```
GET /api/{user_id}/tasks/{task_id}
```

**Response**: `200 OK`
```json
{
  "id": 1,
  "user_id": "uuid-string",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "created_at": "2026-01-26T10:00:00Z",
  "updated_at": "2026-01-26T10:00:00Z"
}
```

**Errors**:
- `401 Unauthorized`: Missing or invalid token
- `403 Forbidden`: User ID mismatch
- `404 Not Found`: Task does not exist

---

### Update Task

```
PUT /api/{user_id}/tasks/{task_id}
```

**Request Body**:
```json
{
  "title": "Updated title",
  "description": "Updated description"
}
```

**Validation**:
- At least one field required
- `title`: 1-200 characters if provided
- `description`: max 1000 characters if provided

**Response**: `200 OK`
```json
{
  "id": 1,
  "user_id": "uuid-string",
  "title": "Updated title",
  "description": "Updated description",
  "completed": false,
  "created_at": "2026-01-26T10:00:00Z",
  "updated_at": "2026-01-26T10:30:00Z"
}
```

**Errors**:
- `400 Bad Request`: Validation error
- `401 Unauthorized`: Missing or invalid token
- `403 Forbidden`: User ID mismatch
- `404 Not Found`: Task does not exist

---

### Toggle Task Completion

```
PATCH /api/{user_id}/tasks/{task_id}/complete
```

**Response**: `200 OK`
```json
{
  "id": 1,
  "user_id": "uuid-string",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": true,
  "created_at": "2026-01-26T10:00:00Z",
  "updated_at": "2026-01-26T10:30:00Z"
}
```

**Errors**:
- `401 Unauthorized`: Missing or invalid token
- `403 Forbidden`: User ID mismatch
- `404 Not Found`: Task does not exist

---

### Delete Task

```
DELETE /api/{user_id}/tasks/{task_id}
```

**Response**: `204 No Content`

**Errors**:
- `401 Unauthorized`: Missing or invalid token
- `403 Forbidden`: User ID mismatch
- `404 Not Found`: Task does not exist

---

## Error Response Format

All errors return:
```json
{
  "detail": "Human-readable message",
  "error_code": "MACHINE_READABLE_CODE",
  "field": "field_name_if_applicable"
}
```

### Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| NOT_AUTHENTICATED | 401 | No token provided |
| INVALID_TOKEN | 401 | Token malformed or invalid signature |
| TOKEN_EXPIRED | 401 | Token has expired |
| ACCESS_DENIED | 403 | User cannot access this resource |
| NOT_FOUND | 404 | Resource does not exist |
| VALIDATION_ERROR | 400 | Request data validation failed |
| INTERNAL_ERROR | 500 | Unexpected server error |

---

## Frontend API Client

```typescript
// lib/api.ts

const API_URL = process.env.NEXT_PUBLIC_API_URL;

class ApiClient {
  private token: string | null = null;

  setToken(token: string) {
    this.token = token;
  }

  private async fetch<T>(
    path: string,
    options: RequestInit = {}
  ): Promise<T> {
    const response = await fetch(`${API_URL}${path}`, {
      ...options,
      headers: {
        "Content-Type": "application/json",
        ...(this.token && { Authorization: `Bearer ${this.token}` }),
        ...options.headers,
      },
    });

    if (!response.ok) {
      const error = await response.json();
      throw new ApiError(error.detail, error.error_code, response.status);
    }

    if (response.status === 204) {
      return undefined as T;
    }

    return response.json();
  }

  // Task operations
  getTasks(userId: string, status?: string, sort?: string) {
    const params = new URLSearchParams();
    if (status) params.set("status", status);
    if (sort) params.set("sort", sort);
    const query = params.toString() ? `?${params}` : "";
    return this.fetch<Task[]>(`/api/${userId}/tasks${query}`);
  }

  createTask(userId: string, data: TaskCreate) {
    return this.fetch<Task>(`/api/${userId}/tasks`, {
      method: "POST",
      body: JSON.stringify(data),
    });
  }

  updateTask(userId: string, taskId: number, data: TaskUpdate) {
    return this.fetch<Task>(`/api/${userId}/tasks/${taskId}`, {
      method: "PUT",
      body: JSON.stringify(data),
    });
  }

  toggleComplete(userId: string, taskId: number) {
    return this.fetch<Task>(`/api/${userId}/tasks/${taskId}/complete`, {
      method: "PATCH",
    });
  }

  deleteTask(userId: string, taskId: number) {
    return this.fetch<void>(`/api/${userId}/tasks/${taskId}`, {
      method: "DELETE",
    });
  }
}

export const api = new ApiClient();
```
