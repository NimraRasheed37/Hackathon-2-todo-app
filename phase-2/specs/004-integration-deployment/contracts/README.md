# API Contracts: Integration, Testing & Deployment

**Feature**: 004-integration-deployment
**Date**: 2026-01-26

---

## Overview

This module does not introduce any new API contracts. All API contracts were defined in previous modules:

- **Module 1 (Backend API)**: Task CRUD endpoints
- **Module 2 (Auth)**: JWT authentication middleware

## Existing API Reference

### Backend API (FastAPI)

**Base URL**: `http://localhost:8000` (local) | `https://your-api.railway.app` (production)

#### Health Check

```http
GET /
```

Response:
```json
{
  "status": "healthy",
  "database": "connected"
}
```

#### Tasks API

All task endpoints require JWT authentication via Bearer token.

```http
Authorization: Bearer <jwt_token>
```

##### List Tasks

```http
GET /api/tasks
```

Query parameters:
- `completed` (optional): Filter by completion status (true/false)

Response: `200 OK`
```json
{
  "tasks": [
    {
      "id": "uuid",
      "title": "string",
      "description": "string | null",
      "completed": false,
      "user_id": "string",
      "created_at": "2026-01-26T12:00:00Z",
      "updated_at": "2026-01-26T12:00:00Z"
    }
  ],
  "total": 1,
  "pending_count": 1,
  "completed_count": 0
}
```

##### Create Task

```http
POST /api/tasks
Content-Type: application/json

{
  "title": "string (required, max 200)",
  "description": "string (optional, max 1000)"
}
```

Response: `201 Created`

##### Get Task

```http
GET /api/tasks/{task_id}
```

Response: `200 OK` | `404 Not Found`

##### Update Task

```http
PUT /api/tasks/{task_id}
Content-Type: application/json

{
  "title": "string (optional)",
  "description": "string (optional)"
}
```

Response: `200 OK` | `404 Not Found`

##### Delete Task

```http
DELETE /api/tasks/{task_id}
```

Response: `204 No Content` | `404 Not Found`

##### Toggle Completion

```http
PATCH /api/tasks/{task_id}/toggle
```

Response: `200 OK` | `404 Not Found`

### Error Responses

All errors follow this format:

```json
{
  "detail": "Human-readable error message",
  "error_code": "MACHINE_READABLE_CODE",
  "field": "optional_field_name"
}
```

Error codes:
- `VALIDATION_ERROR` (400)
- `AUTHENTICATION_ERROR` (401)
- `ACCESS_DENIED` (403)
- `NOT_FOUND` (404)
- `INTERNAL_ERROR` (500)

### Frontend Authentication (Better Auth)

Better Auth provides these client-side methods:

```typescript
// Sign up
await authClient.signUp.email({
  email: "user@example.com",
  password: "password",
  name: "User Name"
});

// Sign in
await authClient.signIn.email({
  email: "user@example.com",
  password: "password"
});

// Sign out
await authClient.signOut();

// Get session
const { data: session } = authClient.useSession();
```

## Contract Location

Full API contracts are documented in:
- `phase-2/specs/001-backend-api-database/contracts/README.md`
- `phase-2/specs/002-auth-user-management/contracts/README.md`

## Integration Notes

1. **JWT Token Flow**:
   - Better Auth issues JWT when user signs in
   - Frontend stores token and includes in API requests
   - Backend validates JWT and extracts user_id

2. **CORS**:
   - Backend allows frontend origin
   - Credentials included in requests

3. **Error Handling**:
   - Backend returns structured errors
   - Frontend displays user-friendly messages
