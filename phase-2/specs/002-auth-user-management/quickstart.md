# Quickstart: Authentication & User Management

**Branch**: `002-auth-user-management` | **Date**: 2026-01-26 | **Plan**: [plan.md](./plan.md)

This guide provides step-by-step instructions for implementing and testing the authentication module.

---

## Prerequisites

Before starting, ensure you have:

1. **Module 1 Complete**: Backend API running with task endpoints functional
2. **Python 3.13+**: Installed and in PATH
3. **Neon PostgreSQL**: Database connection working
4. **Environment Variables**: `.env` file configured

---

## Step 1: Update Environment Variables

Add the following to `phase-2/backend/.env`:

```bash
# Existing from Module 1
DATABASE_URL=postgresql://user:password@host/database?sslmode=require
API_PORT=8000
API_HOST=0.0.0.0
CORS_ORIGINS=http://localhost:3000
ENVIRONMENT=development
LOG_LEVEL=INFO

# NEW for Module 2 - Authentication
JWT_SECRET=your-super-secret-key-at-least-32-characters-long
JWT_ALGORITHM=HS256
JWT_EXPIRATION_DAYS=7
```

**Important**:
- `JWT_SECRET` must be at least 32 characters
- `JWT_SECRET` must match `BETTER_AUTH_SECRET` on frontend
- Use different secrets for development vs production

Update `.env.example` with placeholders for documentation.

---

## Step 2: Install New Dependencies

Add to `requirements.txt`:

```
PyJWT>=2.8.0
bcrypt>=4.1.0
```

Install:

```bash
cd phase-2/backend
pip install -r requirements.txt
```

---

## Step 3: Database Migration

For **fresh databases** (recommended for MVP), SQLModel will create all tables automatically on startup.

For **existing databases** with task data, run this SQL manually:

```sql
-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

CREATE INDEX IF NOT EXISTS ix_users_email ON users (email);

-- Note: Migrating existing tasks with string user_id to UUID
-- requires data transformation which is out of scope for MVP.
-- For MVP, assume fresh database.
```

---

## Step 4: Run the Backend

```bash
cd phase-2/backend
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

Verify health check:
```bash
curl http://localhost:8000/
```

Expected response:
```json
{"status": "healthy", "database": "connected"}
```

---

## Step 5: Testing Authentication

### Generate a Test JWT Token

For testing, you can create a token manually with PyJWT:

```python
import jwt
import uuid
from datetime import datetime, timedelta

secret = "your-super-secret-key-at-least-32-characters-long"
user_id = str(uuid.uuid4())

payload = {
    "sub": user_id,
    "email": "test@example.com",
    "name": "Test User",
    "iat": datetime.utcnow(),
    "exp": datetime.utcnow() + timedelta(days=7)
}

token = jwt.encode(payload, secret, algorithm="HS256")
print(f"User ID: {user_id}")
print(f"Token: {token}")
```

### Test Protected Endpoint

```bash
# Replace with your generated token and user_id
TOKEN="eyJhbGciOiJIUzI1NiIs..."
USER_ID="123e4567-e89b-12d3-a456-426614174000"

curl -X GET "http://localhost:8000/api/${USER_ID}/tasks" \
  -H "Authorization: Bearer ${TOKEN}"
```

### Test Missing Token (401)

```bash
curl -X GET "http://localhost:8000/api/${USER_ID}/tasks"
```

Expected: `401 Unauthorized`

### Test Wrong User (403)

```bash
# Use token for user A but request user B's tasks
OTHER_USER="987e6543-e89b-12d3-a456-426614174999"
curl -X GET "http://localhost:8000/api/${OTHER_USER}/tasks" \
  -H "Authorization: Bearer ${TOKEN}"
```

Expected: `403 Forbidden`

---

## Manual Testing Checklist

### Authentication Tests

| # | Test Case | Expected | Status |
|---|-----------|----------|--------|
| T001 | Request without Authorization header | 401 Unauthorized | [ ] |
| T002 | Request with invalid token format | 401 Unauthorized | [ ] |
| T003 | Request with expired token | 401 Unauthorized + "Token has expired" | [ ] |
| T004 | Request with valid token | 200 OK | [ ] |
| T005 | Request with wrong signature | 401 Unauthorized + "Invalid token" | [ ] |

### Authorization Tests

| # | Test Case | Expected | Status |
|---|-----------|----------|--------|
| T006 | GET /api/{user_id}/tasks with matching token | 200 OK | [ ] |
| T007 | GET /api/{user_id}/tasks with non-matching token | 403 Forbidden | [ ] |
| T008 | POST /api/{user_id}/tasks with matching token | 201 Created | [ ] |
| T009 | POST /api/{user_id}/tasks with non-matching token | 403 Forbidden | [ ] |
| T010 | PUT /api/{user_id}/tasks/{id} for own task | 200 OK | [ ] |
| T011 | PUT /api/{user_id}/tasks/{id} for other's task | 403 Forbidden | [ ] |
| T012 | DELETE /api/{user_id}/tasks/{id} for own task | 204 No Content | [ ] |
| T013 | DELETE /api/{user_id}/tasks/{id} for other's task | 403 Forbidden | [ ] |

### Database Tests

| # | Test Case | Expected | Status |
|---|-----------|----------|--------|
| T014 | Create user in database | User created with UUID id | [ ] |
| T015 | Create task with user_id FK | Task linked to user | [ ] |
| T016 | Delete user | User's tasks cascade deleted | [ ] |

---

## Troubleshooting

### "Invalid token" Error

1. Check that `JWT_SECRET` matches between frontend and backend
2. Verify token is not corrupted (copy full token)
3. Check algorithm is HS256

### "Token has expired" Error

1. Generate a new token
2. Check system clock is accurate
3. Increase `JWT_EXPIRATION_DAYS` for testing

### "Access denied" Error

1. Verify `user_id` in URL matches token's `sub` claim
2. Decode token to check claims: `jwt.decode(token, options={"verify_signature": False})`

### Database Connection Issues

1. Check `DATABASE_URL` in `.env`
2. Verify Neon database is running
3. Check network connectivity (VPN, firewall)

---

## Next Steps

After completing this module:

1. **Run full test checklist** to verify all authentication flows
2. **Document any issues** in the spec or plan files
3. **Proceed to Module 3** (Frontend UI) to implement Better Auth integration

---

## Files Modified/Created

| File | Status | Description |
|------|--------|-------------|
| `src/config.py` | Modified | Added JWT_* settings |
| `src/models/user.py` | New | User SQLModel entity |
| `src/models/task.py` | Modified | UUID user_id with FK |
| `src/schemas/auth.py` | New | TokenPayload schema |
| `src/core/security.py` | New | JWT verification utilities |
| `src/core/exceptions.py` | Modified | Auth exceptions |
| `src/api/middleware/auth.py` | New | JWT middleware |
| `src/api/dependencies.py` | Modified | get_current_user |
| `src/api/routes/tasks.py` | Modified | Protected routes |
| `src/main.py` | Modified | Auth exception handlers |
| `requirements.txt` | Modified | PyJWT, bcrypt |
| `.env.example` | Modified | JWT_* variables |
