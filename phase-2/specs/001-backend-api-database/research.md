# Research Findings: Backend API & Database Layer

**Feature**: Backend API & Database Layer (Phase 2 - Module 1)
**Date**: 2026-01-25
**Phase**: Phase 0 - Research
**Purpose**: Consolidate research findings to inform implementation decisions

---

## Overview

This document consolidates findings from 5 parallel research tasks conducted during Phase 0 of the planning process. Each research task addressed specific technical questions critical to implementing the backend API with best practices.

**Research Tasks Completed**:
1. Neon PostgreSQL Connection Best Practices
2. FastAPI + SQLModel Integration Patterns
3. Pydantic v2 Validation Patterns
4. CORS Configuration for Production
5. Error Handling and Logging Strategy

---

## Research Task 1: Neon PostgreSQL Connection Best Practices

**Question**: What are the recommended connection pooling settings for Neon Serverless PostgreSQL with FastAPI?

### Key Findings

#### 1. Connection Pooling Configuration

**Recommended Pool Size for Neon**:
- **Minimum Connections**: 5 (keeps connections warm, reduces cold start latency)
- **Maximum Connections**: 10-20 (balances between connection overhead and concurrency)
- **Idle Timeout**: 300 seconds (5 minutes)
- **Max Overflow**: 10 (allows temporary burst capacity)

**Rationale**: Neon is serverless and auto-scales, but connection pooling at the application layer reduces latency and prevents connection exhaustion during traffic spikes.

**SQLModel/SQLAlchemy Configuration**:
```python
from sqlmodel import create_engine

engine = create_engine(
    database_url,
    pool_size=10,           # Core pool size
    max_overflow=10,        # Additional connections during burst
    pool_timeout=30,        # Wait time before giving up (seconds)
    pool_recycle=3600,      # Recycle connections after 1 hour
    pool_pre_ping=True,     # Verify connections before use
    echo=False              # Disable SQL query logging in production
)
```

#### 2. SSL/TLS Requirements

**Neon Requirements**:
- **SSL Mode**: `require` (mandatory for all Neon connections)
- **Certificate Verification**: Neon provides valid SSL certificates (no custom CA needed)
- **Connection String Format**: `postgresql://user:password@host/db?sslmode=require`

**Example Connection String**:
```
postgresql://user:password@ep-example-123456.us-east-2.aws.neon.tech/neondb?sslmode=require
```

#### 3. Connection String Format and Authentication

**Best Practices**:
- Store connection string in environment variable (DATABASE_URL)
- Use connection pooler for production (Neon provides built-in pooler)
- Enable `pool_pre_ping` to detect stale connections
- Set reasonable timeouts to fail fast on connection issues

**Connection Pooler URL** (for production with high concurrency):
```
postgresql://user:password@ep-pooler-123456.us-east-2.aws.neon.tech/neondb?sslmode=require
```

#### 4. Error Handling for Connection Issues

**Common Scenarios**:
- **Connection Timeout**: Increase `pool_timeout` or check network latency
- **SSL Handshake Failed**: Verify `sslmode=require` is in connection string
- **Too Many Connections**: Use Neon's connection pooler or reduce `pool_size`

**Recommended Error Handling**:
```python
from sqlalchemy.exc import OperationalError

try:
    engine.connect()
except OperationalError as e:
    logger.error(f"Database connection failed: {e}")
    # Implement retry logic with exponential backoff
```

### Implementation Recommendations

1. **Use Default Pool Settings for MVP**: SQLModel defaults (pool_size=5) are sufficient for initial launch
2. **Enable pool_pre_ping**: Prevents stale connection errors in serverless environments
3. **Set pool_recycle=3600**: Recycle connections hourly to avoid long-lived connection issues
4. **Use Environment Variables**: Never hardcode DATABASE_URL
5. **Monitor Connection Usage**: Add logging for pool exhaustion warnings

---

## Research Task 2: FastAPI + SQLModel Integration Patterns

**Question**: What is the recommended way to structure database sessions with SQLModel in FastAPI (dependency injection pattern)?

### Key Findings

#### 1. Session Lifecycle (Per-Request Pattern)

**Recommended Approach**: Create a new database session for each request and automatically close it when the request completes.

**Implementation**:
```python
# database.py
from sqlmodel import Session, create_engine

engine = create_engine(database_url, pool_pre_ping=True)

def get_session():
    """Dependency for FastAPI route handlers"""
    with Session(engine) as session:
        yield session
```

**Usage in Route Handlers**:
```python
# routes/tasks.py
from fastapi import Depends
from sqlmodel import Session
from database import get_session

@app.get("/api/{user_id}/tasks")
def list_tasks(
    user_id: str,
    session: Session = Depends(get_session)
):
    # Session is automatically created and closed
    tasks = session.exec(select(Task).where(Task.user_id == user_id)).all()
    return tasks
```

**Rationale**: Per-request sessions ensure clean state, prevent memory leaks, and align with FastAPI's request/response lifecycle.

#### 2. Transaction Management Best Practices

**Automatic Commit on Success**:
```python
@app.post("/api/{user_id}/tasks")
def create_task(
    user_id: str,
    task_data: TaskCreate,
    session: Session = Depends(get_session)
):
    task = Task(**task_data.dict(), user_id=user_id)
    session.add(task)
    session.commit()      # Explicit commit
    session.refresh(task) # Refresh to get auto-generated fields
    return task
```

**Automatic Rollback on Error**:
```python
try:
    session.add(task)
    session.commit()
except Exception as e:
    session.rollback()  # Automatic rollback on exception
    raise HTTPException(status_code=500, detail="Database error")
```

**Best Practice**: Use `with Session(engine)` context manager (as in `get_session()`) - it automatically handles commit/rollback.

#### 3. Dependency Injection Pattern

**Benefits of Depends()**:
- **Automatic Lifecycle Management**: Session created/closed per request
- **Testability**: Easy to mock database sessions for testing
- **Type Safety**: FastAPI validates dependency types
- **Reusability**: Same dependency used across all route handlers

**Advanced Pattern (Repository Injection)**:
```python
# repositories/task_repository.py
class TaskRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_user(self, user_id: str):
        return self.session.exec(
            select(Task).where(Task.user_id == user_id)
        ).all()

# api/dependencies.py
def get_task_repository(
    session: Session = Depends(get_session)
) -> TaskRepository:
    return TaskRepository(session)

# routes/tasks.py
@app.get("/api/{user_id}/tasks")
def list_tasks(
    user_id: str,
    repo: TaskRepository = Depends(get_task_repository)
):
    return repo.get_by_user(user_id)
```

#### 4. Alembic Integration (Optional for MVP)

**When to Use Alembic**:
- Production deployments (after MVP)
- Schema changes on existing databases
- Multiple environments (dev, staging, prod)

**MVP Approach**: Use `SQLModel.metadata.create_all(engine)` for automatic schema creation
**Post-MVP**: Migrate to Alembic for version-controlled migrations

### Implementation Recommendations

1. **Use Per-Request Sessions**: Implement `get_session()` dependency with context manager
2. **Repository Pattern**: Create repository layer for complex queries (justified in plan.md)
3. **Explicit Commits**: Always call `session.commit()` after modifications
4. **Error Handling**: Rely on context manager for automatic rollback
5. **Defer Alembic**: Use auto-create for MVP, plan Alembic migration for Module 2

---

## Research Task 3: Pydantic v2 Validation Patterns

**Question**: What are Pydantic v2 best practices for API request validation, especially for optional fields and custom validators?

### Key Findings

#### 1. Field Validation Syntax (Pydantic v2)

**Basic Field Constraints**:
```python
from pydantic import BaseModel, Field

class TaskCreate(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=200,
        description="Task title (1-200 characters)"
    )
    description: str | None = Field(
        default=None,
        max_length=1000,
        description="Optional task description"
    )
```

**Key Changes from Pydantic v1**:
- Use `str | None` instead of `Optional[str]` (Python 3.10+ syntax)
- Use `Field()` for constraints instead of deprecated `constr()`
- Default values must be set explicitly (`default=None` for optional fields)

#### 2. Custom Validators (Pydantic v2)

**Field Validators**:
```python
from pydantic import field_validator

class TaskCreate(BaseModel):
    title: str

    @field_validator('title')
    @classmethod
    def title_must_not_be_whitespace(cls, v: str) -> str:
        if not v.strip():
            raise ValueError('Title cannot be empty or whitespace only')
        return v.strip()  # Trim whitespace
```

**Model Validators** (for cross-field validation):
```python
from pydantic import model_validator

class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None

    @model_validator(mode='after')
    def check_at_least_one_field(self):
        if self.title is None and self.description is None:
            raise ValueError('At least one field must be provided')
        return self
```

#### 3. Optional vs Required Fields

**Pydantic v2 Syntax**:
```python
# Required field (no default)
title: str

# Optional field (nullable)
description: str | None = None

# Optional field with default value
completed: bool = False

# Required but can be None
explicit_none: str | None = Field(...)
```

**Best Practice**: Use `str | None = None` for truly optional fields (most common case).

#### 4. Error Message Customization

**Custom Error Messages**:
```python
from pydantic import Field, ValidationError

class TaskCreate(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=200,
        description="Task title",
        json_schema_extra={
            "example": "Buy groceries"
        }
    )

    @field_validator('title')
    @classmethod
    def validate_title(cls, v: str) -> str:
        if len(v) > 200:
            raise ValueError('Title must be at most 200 characters')
        return v
```

**Error Response Handling**:
```python
from fastapi import HTTPException
from pydantic import ValidationError

try:
    task = TaskCreate(**request_data)
except ValidationError as e:
    # Convert Pydantic errors to user-friendly format
    errors = e.errors()
    raise HTTPException(
        status_code=400,
        detail={
            "detail": errors[0]["msg"],
            "error_code": "VALIDATION_ERROR",
            "field": errors[0]["loc"][0]
        }
    )
```

#### 5. Performance Considerations

**Validation Overhead**:
- Pydantic v2 is ~5-10x faster than v1 (Rust-based core)
- Validation typically adds <1ms per request (negligible for API)
- Use `model_config = {"validate_assignment": False}` to skip validation on field assignment (if needed)

**Best Practice**: Default settings are performant enough for MVP; optimize only if profiling shows validation bottlenecks.

### Implementation Recommendations

1. **Use Pydantic v2 Syntax**: Modern `str | None` syntax for optional fields
2. **Field Constraints**: Use `Field(min_length=..., max_length=...)` for validation
3. **Custom Validators**: Implement `@field_validator` for business logic (e.g., trim whitespace)
4. **Model Validators**: Use for cross-field validation (e.g., "at least one field required")
5. **Error Handling**: Convert ValidationError to standardized error response format
6. **Performance**: Trust defaults; validation overhead is negligible

---

## Research Task 4: CORS Configuration for Production

**Question**: What CORS settings are required for a FastAPI backend serving a Next.js frontend deployed on Vercel?

### Key Findings

#### 1. Required CORS Headers

**Minimum Required Headers**:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://your-app.vercel.app"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)
```

**Headers Explained**:
- **Access-Control-Allow-Origin**: Which origins can make requests
- **Access-Control-Allow-Credentials**: Whether cookies/auth tokens are allowed
- **Access-Control-Allow-Methods**: Which HTTP methods are permitted
- **Access-Control-Allow-Headers**: Which request headers are allowed

#### 2. Credentials Support

**When to Enable `allow_credentials=True`**:
- Using cookies for session management
- Using Authorization header with JWT tokens
- Frontend needs to send/receive credentials

**Security Implications**:
- Cannot use wildcard `*` for `allow_origins` when `allow_credentials=True`
- Must specify exact origins (e.g., `http://localhost:3000`)
- Tokens/cookies are sent with every request (CSRF protection needed)

**Best Practice**: Enable credentials support for JWT authentication (Module 2).

#### 3. Preflight Request Handling (OPTIONS Method)

**What is Preflight**:
- Browser sends OPTIONS request before actual request (for non-simple requests)
- Checks if server allows the requested method/headers
- FastAPI middleware handles this automatically

**Manual Handling Not Required**: `CORSMiddleware` handles OPTIONS requests automatically.

#### 4. Multiple Allowed Origins

**Development + Production Origins**:
```python
import os

origins = os.getenv("CORS_ORIGINS", "").split(",")

# Example CORS_ORIGINS env var:
# CORS_ORIGINS=http://localhost:3000,http://localhost:3001,https://your-app.vercel.app

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Best Practice**: Use environment variable for flexibility across environments.

#### 5. Security Best Practices

**DO**:
- ✅ Specify exact origins (never use `*` in production with credentials)
- ✅ Use HTTPS in production (never HTTP for public APIs)
- ✅ Limit allowed methods to what's actually used
- ✅ Validate Origin header on server (FastAPI middleware does this)

**DON'T**:
- ❌ Use `allow_origins=["*"]` with `allow_credentials=True` (not allowed by CORS spec)
- ❌ Allow all headers (`["*"]`) in production (security risk)
- ❌ Expose sensitive endpoints without authentication

### Implementation Recommendations

1. **Environment-Based Configuration**: Load origins from CORS_ORIGINS environment variable
2. **Enable Credentials**: Set `allow_credentials=True` for JWT authentication (Module 2)
3. **Explicit Origins**: List exact origins (localhost + production URLs)
4. **Allow All Methods**: Use `allow_methods=["*"]` for simplicity (restrict later if needed)
5. **Standard Headers**: Allow `Content-Type` and `Authorization` headers
6. **Automatic Preflight**: Trust FastAPI middleware to handle OPTIONS requests

---

## Research Task 5: Error Handling and Logging Strategy

**Question**: How should we structure error handling and logging in FastAPI to provide user-friendly API responses while maintaining detailed logs for debugging?

### Key Findings

#### 1. FastAPI Exception Handlers

**Global Exception Handler**:
```python
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "error_code": "HTTP_ERROR",
        }
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "An unexpected error occurred. Please try again later.",
            "error_code": "INTERNAL_ERROR",
        }
    )
```

**Route-Specific Exception Handling**:
```python
@app.get("/api/{user_id}/tasks/{id}")
def get_task(user_id: str, id: int, session: Session = Depends(get_session)):
    task = session.get(Task, id)
    if not task or task.user_id != user_id:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )
    return task
```

#### 2. Structured Logging (JSON Logs for Production)

**Logging Configuration**:
```python
import logging
import json
from datetime import datetime

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
        }
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_data)

# Configure logging
logging.basicConfig(level=logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logger = logging.getLogger("app")
logger.addHandler(handler)
```

**Development vs Production**:
```python
import os

if os.getenv("ENVIRONMENT") == "production":
    # JSON logs for production (parseable by log aggregators)
    handler.setFormatter(JSONFormatter())
else:
    # Human-readable logs for development
    handler.setFormatter(logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    ))
```

#### 3. Log Levels and What to Log Where

**Log Level Guidelines**:

- **DEBUG**: Detailed diagnostic information (disabled in production)
  - Example: SQL queries, function entry/exit, variable values

- **INFO**: General informational messages (important events)
  - Example: Server startup, database connection, API request received

- **WARNING**: Something unexpected but not an error
  - Example: Deprecated API usage, rate limit approaching

- **ERROR**: Error events that need attention
  - Example: Database query failed, validation error, external API timeout

- **CRITICAL**: Severe errors causing service disruption
  - Example: Database connection lost, unrecoverable error

**What to Log**:
```python
# INFO: Successful operations
logger.info(f"Task {task.id} created for user {user_id}")

# WARNING: Unexpected but handled situations
logger.warning(f"User {user_id} attempted to access task {id} belonging to another user")

# ERROR: Failures and exceptions
logger.error(f"Database query failed for user {user_id}", exc_info=True)

# DEBUG: Detailed diagnostic info (development only)
logger.debug(f"Query executed: {query}")
```

#### 4. Request ID Tracking (for Correlating Logs)

**Middleware for Request IDs**:
```python
import uuid
from starlette.middleware.base import BaseHTTPMiddleware

class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id

        # Add to logger context
        logger.info(f"Request started", extra={"request_id": request_id})

        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response

app.add_middleware(RequestIDMiddleware)
```

**Usage in Route Handlers**:
```python
@app.get("/api/{user_id}/tasks")
def list_tasks(request: Request, user_id: str):
    request_id = request.state.request_id
    logger.info(f"Listing tasks for user {user_id}", extra={"request_id": request_id})
    # ... rest of handler
```

#### 5. Error Response Format Standardization

**Consistent Error Response Schema**:
```python
from pydantic import BaseModel

class ErrorResponse(BaseModel):
    detail: str              # User-friendly message
    error_code: str          # Machine-readable code (e.g., "NOT_FOUND")
    field: str | None = None # Field name for validation errors

# Usage
raise HTTPException(
    status_code=404,
    detail="Task not found",
    headers={"X-Error-Code": "NOT_FOUND"}
)
```

**Error Code Mapping**:
```python
ERROR_CODES = {
    "NOT_FOUND": "Resource not found",
    "VALIDATION_ERROR": "Input validation failed",
    "UNAUTHORIZED": "Authentication required",
    "FORBIDDEN": "Access denied",
    "INTERNAL_ERROR": "An unexpected error occurred"
}
```

### Implementation Recommendations

1. **Global Exception Handlers**: Implement handlers for HTTPException and generic Exception
2. **Structured Logging**: Use JSON logs in production, human-readable logs in development
3. **Log Levels**: INFO for successful operations, ERROR for failures, DEBUG for diagnostics
4. **Request ID Tracking**: Add middleware to correlate logs with requests
5. **User-Friendly Errors**: Never expose stack traces or internal details to clients
6. **Standardized Format**: Use consistent error response schema across all endpoints
7. **Log Important Events**: Database connections, user actions, errors (but avoid logging PII)

---

## Summary of Key Decisions

Based on research findings, the following decisions have been made for implementation:

### Database (Neon PostgreSQL)
- ✅ Use SQLModel default pool settings (pool_size=5-10)
- ✅ Enable `pool_pre_ping=True` for connection validation
- ✅ Set `pool_recycle=3600` (1 hour)
- ✅ Use `sslmode=require` for all connections
- ✅ Load DATABASE_URL from environment variable

### Session Management (FastAPI + SQLModel)
- ✅ Use per-request sessions with `get_session()` dependency
- ✅ Implement Repository pattern for data access abstraction
- ✅ Explicit commits with automatic rollback on errors
- ✅ Defer Alembic migrations to post-MVP (use auto-create for MVP)

### Validation (Pydantic v2)
- ✅ Use modern `str | None` syntax for optional fields
- ✅ Use `Field()` for constraints (min_length, max_length)
- ✅ Implement custom validators for business logic (e.g., trim whitespace)
- ✅ Convert ValidationError to standardized error response format

### CORS Configuration
- ✅ Load origins from CORS_ORIGINS environment variable
- ✅ Enable `allow_credentials=True` for JWT authentication (Module 2)
- ✅ Allow all methods and standard headers (Content-Type, Authorization)
- ✅ Trust FastAPI middleware for automatic OPTIONS handling

### Error Handling and Logging
- ✅ Implement global exception handlers (HTTPException and generic Exception)
- ✅ Use structured JSON logs in production, readable logs in development
- ✅ Log at INFO level for successful operations, ERROR for failures
- ✅ Add request ID middleware for log correlation
- ✅ Use standardized error response format (detail, error_code, field)
- ✅ Never expose stack traces or internal details to clients

---

## Open Questions and Future Research

### Questions Deferred to Post-MVP
1. **Alembic Migration Strategy**: When to migrate from auto-create to Alembic?
   - Decision: After Module 2 (when users table is added)
2. **Connection Pool Optimization**: Should we tune pool settings based on load testing?
   - Decision: Monitor performance metrics in production, optimize if needed
3. **Advanced Logging**: Should we integrate with external logging service (Sentry, Datadog)?
   - Decision: Defer to post-MVP, evaluate based on operational needs

### Questions Answered by Research
- ✅ How to configure Neon connection pooling? → Use SQLModel defaults with pool_pre_ping
- ✅ How to structure database sessions? → Per-request with dependency injection
- ✅ How to validate input with Pydantic v2? → Use Field() constraints and custom validators
- ✅ How to configure CORS for Vercel? → Environment-based origins with credentials support
- ✅ How to log errors without exposing details? → Global handlers + structured logging

---

## References

- **Neon Documentation**: https://neon.tech/docs/
- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **SQLModel Documentation**: https://sqlmodel.tiangolo.com/
- **Pydantic v2 Documentation**: https://docs.pydantic.dev/latest/
- **CORS Specification**: https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS

---

**Last Updated**: 2026-01-25
**Phase**: Phase 0 - Research
**Status**: Complete (all 5 research tasks consolidated)
