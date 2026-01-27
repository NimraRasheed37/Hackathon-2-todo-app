# API Contracts: Authentication & User Management

**Branch**: `002-auth-user-management` | **Date**: 2026-01-26

This directory contains API contracts for the authentication module.

---

## Overview

Module 2 adds JWT-based authentication to the existing Task API from Module 1. All task endpoints now require a valid JWT token in the `Authorization` header.

### Authentication Flow

```
1. User registers/logs in via Better Auth (frontend)
2. Better Auth issues JWT token
3. Token stored in httpOnly cookie or localStorage
4. Frontend includes token in API requests
5. Backend verifies token with PyJWT
6. Backend checks user authorization
7. Request proceeds or returns 401/403
```

---

## Security Scheme

### Bearer Token Authentication

All protected endpoints require a JWT token in the `Authorization` header:

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Token Structure

```json
{
  "sub": "123e4567-e89b-12d3-a456-426614174000",
  "email": "user@example.com",
  "name": "John Doe",
  "iat": 1706140800,
  "exp": 1706745600
}
```

| Claim | Type | Description |
|-------|------|-------------|
| `sub` | UUID | User ID (subject) |
| `email` | string | User's email address |
| `name` | string | User's display name |
| `iat` | integer | Issued at (Unix timestamp) |
| `exp` | integer | Expiration (Unix timestamp) |

### Token Expiration

- Default: 7 days (604800 seconds)
- Configurable via `JWT_EXPIRATION_DAYS` environment variable

---

## Error Responses

### 401 Unauthorized

Returned when authentication fails.

| Error Code | Description | Example |
|------------|-------------|---------|
| `NOT_AUTHENTICATED` | Missing Authorization header | No token provided |
| `INVALID_TOKEN` | Malformed or invalid signature | Token was tampered with |
| `TOKEN_EXPIRED` | Token has expired | Token older than 7 days |

**Response Format**:
```json
{
  "detail": "Token has expired",
  "error_code": "TOKEN_EXPIRED"
}
```

### 403 Forbidden

Returned when authorization fails (user lacks permission).

| Error Code | Description | Example |
|------------|-------------|---------|
| `ACCESS_DENIED` | User cannot access resource | Accessing another user's tasks |

**Response Format**:
```json
{
  "detail": "Access denied",
  "error_code": "ACCESS_DENIED"
}
```

---

## Protected Endpoints

All task endpoints require authentication:

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/{user_id}/tasks` | List user's tasks |
| POST | `/api/{user_id}/tasks` | Create a task |
| GET | `/api/{user_id}/tasks/{task_id}` | Get a task |
| PUT | `/api/{user_id}/tasks/{task_id}` | Update a task |
| PATCH | `/api/{user_id}/tasks/{task_id}/complete` | Toggle completion |
| DELETE | `/api/{user_id}/tasks/{task_id}` | Delete a task |

### Public Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check (no auth required) |

---

## Authorization Rules

### User ID Validation

The `user_id` in the URL path MUST match the `sub` claim in the JWT token:

```python
if str(current_user.sub) != user_id:
    raise HTTPException(status_code=403, detail="Access denied")
```

### Task Ownership

For operations on specific tasks, the task's `user_id` MUST match the token's `sub`:

- GET /api/{user_id}/tasks/{task_id} - Task must belong to user
- PUT /api/{user_id}/tasks/{task_id} - Task must belong to user
- PATCH /api/{user_id}/tasks/{task_id}/complete - Task must belong to user
- DELETE /api/{user_id}/tasks/{task_id} - Task must belong to user

---

## Example Requests

### Authenticated Request (Success)

```bash
curl -X GET http://localhost:8000/api/123e4567-e89b-12d3-a456-426614174000/tasks \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..." \
  -H "Content-Type: application/json"
```

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "user_id": "123e4567-e89b-12d3-a456-426614174000",
    "title": "Complete authentication module",
    "description": null,
    "completed": false,
    "created_at": "2026-01-26T10:30:00Z",
    "updated_at": "2026-01-26T10:30:00Z"
  }
]
```

### Missing Token (401)

```bash
curl -X GET http://localhost:8000/api/123e4567-e89b-12d3-a456-426614174000/tasks
```

**Response** (401 Unauthorized):
```json
{
  "detail": "Not authenticated"
}
```

### Expired Token (401)

```bash
curl -X GET http://localhost:8000/api/123e4567-e89b-12d3-a456-426614174000/tasks \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..." # expired token
```

**Response** (401 Unauthorized):
```json
{
  "detail": "Token has expired",
  "error_code": "TOKEN_EXPIRED"
}
```

### Wrong User (403)

```bash
# Token contains sub: "123e4567-..." but requesting "987e6543-..."
curl -X GET http://localhost:8000/api/987e6543-e89b-12d3-a456-426614174999/tasks \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..."
```

**Response** (403 Forbidden):
```json
{
  "detail": "Access denied",
  "error_code": "ACCESS_DENIED"
}
```

---

## Files in This Directory

| File | Description |
|------|-------------|
| `openapi.yaml` | OpenAPI 3.0 specification with security schemes |
| `README.md` | This file - human-readable API documentation |

---

## Integration Notes

### Frontend (Better Auth)

Better Auth handles:
- User registration (signup)
- User login (signin)
- Token storage (httpOnly cookie)
- Token inclusion in requests
- Token refresh

The backend only verifies tokens; it does not issue them.

### Backend (PyJWT)

Backend responsibilities:
- Verify token signature with shared secret
- Check token expiration
- Extract user claims (sub, email, name)
- Validate user authorization

### Shared Secret

The JWT secret MUST be identical on both sides:
- Frontend: `BETTER_AUTH_SECRET`
- Backend: `JWT_SECRET`

Example: `JWT_SECRET=your-super-secret-key-at-least-32-characters-long`
