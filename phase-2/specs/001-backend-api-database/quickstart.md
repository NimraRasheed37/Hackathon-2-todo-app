# Quick Start Guide: Backend API & Database Layer

**Feature**: Backend API & Database Layer (Phase 2 - Module 1)
**Date**: 2026-01-25
**Purpose**: Get the FastAPI backend running locally with Neon PostgreSQL in under 10 minutes

---

## Prerequisites

Before starting, ensure you have:

1. **Python 3.13+** installed
   - Verify: `python --version` (should show 3.13.0 or higher)
   - Download: https://www.python.org/downloads/

2. **Neon PostgreSQL Account**
   - Sign up: https://neon.tech/ (free tier available)
   - Create a new project (or use existing)
   - Copy your connection string (looks like: `postgresql://user:password@host/database`)

3. **Git** (for cloning repository)
   - Verify: `git --version`

4. **Code Editor** (VS Code, PyCharm, or similar)

5. **API Testing Tool** (optional but recommended)
   - cURL (built-in on most systems)
   - Postman (https://www.postman.com/downloads/)
   - HTTPie (https://httpie.io/)

---

## Step 1: Clone and Navigate

```bash
# Clone the repository
git clone <repository-url>
cd <repository-name>

# Navigate to backend directory
cd phase-2/backend
```

---

## Step 2: Set Up Python Environment

### Option A: Using venv (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Option B: Using Poetry

```bash
# Install Poetry if not already installed
pip install poetry

# Install dependencies
poetry install

# Activate shell
poetry shell
```

---

## Step 3: Configure Environment Variables

```bash
# Copy environment template
cp .env.example .env

# Open .env in your editor and configure:
# - DATABASE_URL (required)
# - API_PORT (optional, defaults to 8000)
# - CORS_ORIGINS (optional, defaults to localhost:3000)
```

**Example .env file**:

```env
# Database Configuration
DATABASE_URL=postgresql://user:password@ep-example-123456.us-east-2.aws.neon.tech/neondb?sslmode=require

# API Configuration
API_PORT=8000
API_HOST=0.0.0.0

# CORS Configuration (comma-separated list)
CORS_ORIGINS=http://localhost:3000,http://localhost:3001

# Environment
ENVIRONMENT=development

# Logging
LOG_LEVEL=INFO
```

**Important Notes**:
- **DATABASE_URL**: Get this from Neon dashboard → Project → Connection Details → Connection String
- **sslmode=require**: Required for Neon PostgreSQL connections
- **CORS_ORIGINS**: Add all frontend URLs that will access the API

---

## Step 4: Start the Backend Server

```bash
# Start server with auto-reload (development mode)
uvicorn src.main:app --reload --port 8000

# Alternative: Start with custom host/port
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected Output**:

```
INFO:     Will watch for changes in these directories: ['/path/to/backend']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using StatReload
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**Verify Server is Running**:

Open browser and navigate to:
- **API Docs**: http://localhost:8000/docs (Swagger UI)
- **Alternative Docs**: http://localhost:8000/redoc (ReDoc)
- **Health Check**: http://localhost:8000/ (should return `{"status": "ok"}`)

---

## Step 5: Verify Database Connection

The database schema is automatically created on first startup. Check the server logs for:

```
INFO:     Database connected successfully
INFO:     Tables created: tasks
INFO:     Indexes created: idx_tasks_user_id, idx_tasks_completed
```

**Manual Verification** (optional):

```bash
# Connect to Neon database using psql
psql $DATABASE_URL

# Check tables exist
\dt

# Expected output:
#  Schema |  Name  | Type  |   Owner
# --------+--------+-------+-----------
#  public | tasks  | table | neondb_owner

# Check table schema
\d tasks

# Exit psql
\q
```

---

## Step 6: Test API Endpoints

### Test 1: Create a Task

```bash
curl -X POST "http://localhost:8000/api/user123/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Task",
    "description": "Testing the API"
  }'
```

**Expected Response** (201 Created):

```json
{
  "id": 1,
  "user_id": "user123",
  "title": "Test Task",
  "description": "Testing the API",
  "completed": false,
  "created_at": "2026-01-25T10:30:00Z",
  "updated_at": "2026-01-25T10:30:00Z"
}
```

### Test 2: List All Tasks

```bash
curl -X GET "http://localhost:8000/api/user123/tasks"
```

**Expected Response** (200 OK):

```json
[
  {
    "id": 1,
    "user_id": "user123",
    "title": "Test Task",
    "description": "Testing the API",
    "completed": false,
    "created_at": "2026-01-25T10:30:00Z",
    "updated_at": "2026-01-25T10:30:00Z"
  }
]
```

### Test 3: Toggle Task Completion

```bash
curl -X PATCH "http://localhost:8000/api/user123/tasks/1/complete"
```

**Expected Response** (200 OK - task now marked complete):

```json
{
  "id": 1,
  "user_id": "user123",
  "title": "Test Task",
  "description": "Testing the API",
  "completed": true,
  "created_at": "2026-01-25T10:30:00Z",
  "updated_at": "2026-01-25T10:35:00Z"
}
```

### Test 4: Delete Task

```bash
curl -X DELETE "http://localhost:8000/api/user123/tasks/1"
```

**Expected Response** (204 No Content - no response body)

---

## Complete Testing Checklist

Use this checklist to verify all functionality:

### Database Connection Tests
- [ ] Server starts without errors
- [ ] Database connection successful (check logs)
- [ ] Tables created automatically (tasks table exists)
- [ ] Indexes created (idx_tasks_user_id, idx_tasks_completed)

### API Endpoint Tests
- [ ] GET /api/{user_id}/tasks (list all tasks) - returns 200
- [ ] POST /api/{user_id}/tasks (create task) - returns 201
- [ ] GET /api/{user_id}/tasks/{id} (get single task) - returns 200
- [ ] PUT /api/{user_id}/tasks/{id} (update task) - returns 200
- [ ] PATCH /api/{user_id}/tasks/{id}/complete (toggle) - returns 200
- [ ] DELETE /api/{user_id}/tasks/{id} (delete task) - returns 204

### Filtering and Sorting Tests
- [ ] GET /api/{user_id}/tasks?status=pending - returns only pending tasks
- [ ] GET /api/{user_id}/tasks?status=completed - returns only completed tasks
- [ ] GET /api/{user_id}/tasks?sort=title - returns tasks sorted alphabetically
- [ ] GET /api/{user_id}/tasks?sort=created - returns tasks by creation date

### Validation Tests
- [ ] POST with empty title - returns 400 with validation error
- [ ] POST with title > 200 chars - returns 400 with validation error
- [ ] POST with description > 1000 chars - returns 400 with validation error
- [ ] PUT with invalid JSON - returns 422 with error

### Data Isolation Tests
- [ ] GET /api/userA/tasks - returns only userA's tasks
- [ ] GET /api/userB/tasks/{userA_task_id} - returns 404 (cross-user access blocked)
- [ ] DELETE /api/userB/tasks/{userA_task_id} - returns 404 (cross-user deletion blocked)

### Error Handling Tests
- [ ] GET /api/{user_id}/tasks/999999 (non-existent ID) - returns 404
- [ ] DELETE /api/{user_id}/tasks/999999 (non-existent ID) - returns 404
- [ ] POST with malformed JSON - returns 422
- [ ] Database connection lost - returns 500 with user-friendly error

---

## Common Issues and Troubleshooting

### Issue 1: Server Won't Start

**Symptom**: `ModuleNotFoundError: No module named 'fastapi'`

**Solution**: Install dependencies
```bash
pip install -r requirements.txt
```

---

### Issue 2: Database Connection Failed

**Symptom**: `FATAL: password authentication failed for user "..."`

**Solution**: Check DATABASE_URL in .env file
- Ensure username and password are correct
- Verify connection string from Neon dashboard
- Check that `sslmode=require` is included

**Test Connection**:
```bash
# Test database connection directly
psql $DATABASE_URL -c "SELECT 1;"

# Expected output: 1 row returned with value 1
```

---

### Issue 3: CORS Errors in Browser

**Symptom**: `Access to fetch at 'http://localhost:8000' from origin 'http://localhost:3000' has been blocked by CORS policy`

**Solution**: Add frontend URL to CORS_ORIGINS in .env
```env
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
```

Restart the server after changing .env file.

---

### Issue 4: Port Already in Use

**Symptom**: `[ERROR] [Errno 48] Address already in use`

**Solution**: Change port or kill existing process
```bash
# Option 1: Use different port
uvicorn src.main:app --reload --port 8001

# Option 2: Kill process using port 8000 (Windows)
netstat -ano | findstr :8000
taskkill /PID <process_id> /F

# Option 2: Kill process using port 8000 (macOS/Linux)
lsof -ti:8000 | xargs kill -9
```

---

### Issue 5: Tables Not Created

**Symptom**: Server starts but queries fail with "relation 'tasks' does not exist"

**Solution**: Check server startup logs for errors
```bash
# Restart server with debug logging
LOG_LEVEL=DEBUG uvicorn src.main:app --reload
```

Look for errors in table creation. If issues persist:
```bash
# Manually create tables using psql
psql $DATABASE_URL -f migrations/001_create_tasks_table.sql
```

---

### Issue 6: 404 on Valid Endpoints

**Symptom**: `GET /api/user123/tasks` returns 404 Not Found

**Solution**: Check API docs to verify correct endpoint structure
- Open http://localhost:8000/docs
- Verify endpoint paths match OpenAPI specification
- Ensure server started without errors

---

## Development Workflow

### Making Changes

1. **Edit code** in `src/` directory
2. **Server auto-reloads** (if using `--reload` flag)
3. **Test changes** using cURL or Postman
4. **Check logs** for errors or warnings

### Viewing Logs

```bash
# Logs are printed to console by default
# To save logs to file:
uvicorn src.main:app --reload 2>&1 | tee logs/server.log
```

### Debugging

```bash
# Start server with debug logging
LOG_LEVEL=DEBUG uvicorn src.main:app --reload

# Use Python debugger (pdb)
# Add breakpoint in code:
import pdb; pdb.set_trace()
```

---

## Next Steps

After verifying the backend works locally:

1. **Frontend Integration**: Connect Next.js frontend (Module 3)
2. **Authentication**: Add JWT authentication (Module 2)
3. **Deployment**: Deploy to Vercel or similar PaaS
4. **Monitoring**: Set up logging and error tracking (Sentry, etc.)

---

## API Documentation

For complete API reference:
- **Interactive Docs**: http://localhost:8000/docs (Swagger UI)
- **Detailed Documentation**: See [contracts/README.md](./contracts/README.md)
- **OpenAPI Specification**: See [contracts/openapi.yaml](./contracts/openapi.yaml)

---

## Additional Resources

- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **SQLModel Documentation**: https://sqlmodel.tiangolo.com/
- **Neon Documentation**: https://neon.tech/docs/
- **Pydantic Documentation**: https://docs.pydantic.dev/

---

## Support

If you encounter issues not covered here:

1. **Check Logs**: Review server logs for error messages
2. **Verify Environment**: Ensure all prerequisites are met
3. **Database Status**: Check Neon dashboard for database health
4. **API Docs**: Use interactive docs at /docs to test endpoints
5. **Open Issue**: Create issue in GitHub repository with:
   - Error message
   - Steps to reproduce
   - Environment details (Python version, OS, etc.)

---

**Last Updated**: 2026-01-25
**Module**: Backend API & Database Layer (Phase 2 - Module 1)
