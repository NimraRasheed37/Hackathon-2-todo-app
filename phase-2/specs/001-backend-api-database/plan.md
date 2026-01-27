# Implementation Plan: Backend API & Database Layer

**Branch**: `001-backend-api-database` | **Date**: 2026-01-25 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `phase-2/specs/001-backend-api-database/spec.md`

## Summary

This module establishes the foundational backend infrastructure for the full-stack Todo application. We will build a RESTful API using FastAPI that provides CRUD operations for task management, backed by Neon Serverless PostgreSQL for data persistence. The API will serve as the data access layer consumed by the Next.js frontend and will be secured with authentication in a subsequent module.

**Primary Requirement**: Provide 6 RESTful API endpoints (List, Create, Get, Update, Toggle Complete, Delete) with robust error handling, data validation, and database persistence.

**Technical Approach**: Use FastAPI with SQLModel ORM for type-safe database operations, implement Repository pattern for data access abstraction, and enforce data isolation at the API layer (user_id validation). Deploy as a stateless microservice with connection pooling for scalability.

---

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: FastAPI (0.109.0+), SQLModel (0.0.14+), Uvicorn (0.27.0+), Pydantic v2 (2.5.0+), psycopg2-binary (2.9.9+)
**Storage**: Neon Serverless PostgreSQL (cloud-hosted, managed service)
**Testing**: Manual testing with cURL/Postman for MVP (pytest integration tests deferred to post-MVP)
**Target Platform**: Linux server (Docker container on Vercel or similar PaaS)
**Project Type**: Web (backend only - API microservice)
**Performance Goals**:
- API response time < 200ms for single-task operations
- API response time < 500ms for listing operations (up to 100 tasks)
- Database query time < 50ms for indexed queries
- Support 100 concurrent requests without degradation

**Constraints**:
- API endpoints MUST respond within 200ms (P95)
- Database connection MUST be established within 5 seconds on startup
- Memory usage < 512MB per container instance
- No hardcoded secrets (all config from environment variables)
- CORS enabled for frontend origins (localhost:3000 + production URL)

**Scale/Scope**:
- MVP: 100 concurrent users, ~1000 tasks per user maximum
- Database: Single Neon instance (auto-scaling, no manual sharding needed)
- API: Stateless, horizontally scalable via Vercel functions

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Article I: Spec-Driven Development
- ✅ PASS: Comprehensive specification exists with 6 user stories and 45 functional requirements
- ✅ PASS: All acceptance criteria defined in Given/When/Then format
- ✅ PASS: Code will be generated based on spec, no manual coding except configuration

### Article III: Security is Non-Negotiable
- ⚠️ PARTIAL: Authentication deferred to Module 2 (acceptable per spec assumptions)
- ✅ PASS: Data isolation enforced (user_id validation on all operations)
- ✅ PASS: No secrets in code (DATABASE_URL from environment)
- ✅ PASS: Input validation via Pydantic models
- ✅ PASS: SQL injection prevented (SQLModel ORM, parameterized queries)

**Note**: Article III partial compliance is documented in spec assumptions. Full authentication (JWT tokens) will be added in Module 2 - Authentication & User Management. Current implementation validates user_id from URL path to enforce data isolation.

### Article IV: Code Quality Standards
- ✅ PASS: Python code will use type hints (Pydantic/SQLModel enforce this)
- ✅ PASS: PEP 8 compliance (enforced by Black formatter + Ruff linter)
- ✅ PASS: Docstrings for modules, classes, public functions
- ✅ PASS: Maximum function length 50 lines (API route handlers naturally short)
- ✅ PASS: No print() statements (logging module used)

### Article V: Database Integrity
- ✅ PASS: Primary key (id) on tasks table
- ✅ PASS: created_at and updated_at timestamps required
- ✅ PASS: user_id indexed for performance
- ✅ PASS: Foreign key constraint (user_id references users table - added in Module 2)
- ✅ PASS: Database constraints enforced (NOT NULL, length limits)

### Article VI: Performance Requirements
- ✅ PASS: API response time target < 200ms (measured in success criteria)
- ✅ PASS: Database query time < 50ms (indexes on user_id, completed)
- ✅ PASS: Connection pooling configured (SQLModel default pool of 5-10)

### Article IX: API Design Principles
- ✅ PASS: RESTful conventions followed (GET list, POST create, PUT update, PATCH toggle, DELETE remove)
- ✅ PASS: Predictable URL structure (/api/{user_id}/tasks)
- ✅ PASS: Consistent response format (JSON with standardized error structure)
- ✅ PASS: HTTP status codes aligned with REST best practices (200, 201, 204, 400, 404, 422, 500)

### Article X: Error Handling Philosophy
- ✅ PASS: User-friendly error messages required (no stack traces to clients)
- ✅ PASS: Error response format specified (detail, error_code, field)
- ✅ PASS: Errors logged for debugging (logging module configuration)

### Article XII: Environment Management
- ✅ PASS: .env file for local development
- ✅ PASS: Environment variables documented (DATABASE_URL, API_PORT, CORS_ORIGINS)
- ✅ PASS: .env.example will be provided
- ✅ PASS: Different secrets for local vs production

**Constitution Check Result**: ✅ PASSES with documented exception (authentication deferred per spec)

---

## Project Structure

### Documentation (this feature)

```text
phase-2/specs/001-backend-api-database/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
│   ├── openapi.yaml    # OpenAPI 3.0 specification
│   └── README.md       # API documentation
├── spec.md              # Feature specification (already exists)
└── checklists/
    └── requirements.md  # Specification quality checklist (already exists)
```

### Source Code (repository root)

Since this is Phase 2 (full-stack web application), we use **Option 2: Web application** structure. However, for Module 1, we're implementing ONLY the backend portion.

```text
phase-2/
├── backend/
│   ├── src/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI app entry point
│   │   ├── config.py            # Configuration management (load env vars)
│   │   ├── database.py          # Database connection and session
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── task.py         # SQLModel Task entity
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   └── task.py         # Pydantic request/response models
│   │   ├── repositories/
│   │   │   ├── __init__.py
│   │   │   └── task_repository.py  # Data access layer
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── dependencies.py  # Dependency injection (DB session)
│   │   │   └── routes/
│   │   │       ├── __init__.py
│   │   │       └── tasks.py    # Task API endpoints
│   │   └── core/
│   │       ├── __init__.py
│   │       ├── exceptions.py    # Custom exception classes
│   │       └── logging_config.py  # Logging setup
│   ├── .env.example             # Environment variable template
│   ├── .env                     # Local environment variables (gitignored)
│   ├── requirements.txt         # Python dependencies
│   ├── Dockerfile               # Container image definition
│   ├── README.md                # Backend documentation
│   └── CLAUDE.md                # Backend-specific Claude Code instructions
│
└── frontend/                    # Placeholder for Module 3
    └── README.md                # "Frontend to be implemented in Module 3"
```

**Structure Decision**:

We chose the web application structure (Option 2) because Phase 2 is building a full-stack application with separate backend and frontend. The backend is organized using a layered architecture:

1. **Entry Point Layer** (`main.py`): FastAPI app initialization, CORS configuration, route registration
2. **API Layer** (`api/routes/`): HTTP route handlers, request validation, response serialization
3. **Repository Layer** (`repositories/`): Data access abstraction, database queries
4. **Model Layer** (`models/`): SQLModel entities (database tables)
5. **Schema Layer** (`schemas/`): Pydantic models for API requests/responses (DTOs)
6. **Core Layer** (`core/`): Cross-cutting concerns (exceptions, logging, config)

This layered architecture provides:
- **Separation of Concerns**: Each layer has single responsibility
- **Testability**: Repository layer can be mocked for API testing
- **Maintainability**: Changes to database don't affect API contracts
- **Type Safety**: Pydantic + SQLModel provide end-to-end type checking

**Rationale for Repository Pattern**: Although Article IV discourages over-engineering, the Repository pattern is justified here because:
1. It's a standard pattern for FastAPI + SQLModel applications (not premature abstraction)
2. It isolates database queries from API logic, making testing easier
3. It enables future optimizations (caching, query optimization) without touching API code
4. The complexity overhead is minimal (single repository class with ~6 methods)

---

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

**No violations requiring justification.**

The constitution check passed with one documented exception (authentication deferred to Module 2), which is explicitly acknowledged in the feature specification assumptions and does not violate constitutional principles.

**Architectural Decisions Aligned with Constitution**:

1. **Repository Pattern**: Justified above - standard pattern for this stack, minimal overhead, clear benefits
2. **Layered Architecture**: Promotes code quality (Article IV), maintainability, and testability
3. **Separate Schemas from Models**: Follows DTO pattern (Article IX) to decouple API contracts from database structure
4. **Environment-based Configuration**: Enforces Article XII (Environment Management) and Article III (Security)

---

## Phase 0: Research Tasks

### Research Task 1: Neon PostgreSQL Connection Best Practices

**Question**: What are the recommended connection pooling settings for Neon Serverless PostgreSQL with FastAPI?

**Why**: Neon is a serverless database that scales connections automatically, but we need to configure connection pooling correctly to avoid connection exhaustion and optimize performance.

**Research Focus**:
- Recommended pool size for Neon (min, max connections)
- Connection timeout settings
- Idle connection handling
- SSL/TLS requirements for Neon connections
- Connection string format and authentication method

### Research Task 2: FastAPI + SQLModel Integration Patterns

**Question**: What is the recommended way to structure database sessions with SQLModel in FastAPI (dependency injection pattern)?

**Why**: We need to ensure proper session management (create session per request, automatic cleanup) and understand how to use FastAPI's dependency injection with SQLModel.

**Research Focus**:
- Recommended session lifecycle (per-request vs long-lived)
- How to use `Depends()` for database session injection
- Transaction management best practices
- Error handling and session rollback patterns
- Alembic integration for migrations (optional for MVP, but good to understand)

### Research Task 3: Pydantic v2 Validation Patterns

**Question**: What are Pydantic v2 best practices for API request validation, especially for optional fields and custom validators?

**Why**: Pydantic v2 has breaking changes from v1. We need to understand the new syntax for validators and ensure we're using the latest patterns.

**Research Focus**:
- Field validation syntax (min_length, max_length)
- Custom validators (for complex business rules)
- Optional vs required fields
- Error message customization (user-friendly messages)
- Performance considerations (validation overhead)

### Research Task 4: CORS Configuration for Production

**Question**: What CORS settings are required for a FastAPI backend serving a Next.js frontend deployed on Vercel?

**Why**: We need to allow the frontend to make requests to the backend while preventing unauthorized origins.

**Research Focus**:
- Required CORS headers (Access-Control-Allow-Origin, etc.)
- Credentials support (cookies, auth tokens)
- Preflight request handling (OPTIONS method)
- Multiple allowed origins (localhost + production URL)
- Security implications and best practices

### Research Task 5: Error Handling and Logging Strategy

**Question**: How should we structure error handling and logging in FastAPI to provide user-friendly API responses while maintaining detailed logs for debugging?

**Why**: Article X requires user-friendly error messages (no stack traces), but we also need detailed logs for troubleshooting.

**Research Focus**:
- FastAPI exception handlers (global vs route-specific)
- Structured logging (JSON logs for production)
- Log levels and what to log where (INFO, WARNING, ERROR)
- Request ID tracking (for correlating logs with requests)
- Error response format standardization

---

## Phase 1 Design Outputs

*(To be completed during Phase 1 execution)*

### data-model.md Preview

The data-model.md file will document:

**Entity: Task**
- Primary key: id (auto-increment integer)
- Foreign key: user_id (string, indexed)
- Attributes: title (string 1-200), description (string max 1000, nullable), completed (boolean, default false)
- Timestamps: created_at (auto), updated_at (auto)
- Indexes: user_id, completed
- Validation rules: Title required, length constraints, description optional

**State Transitions**:
- pending → completed (via PATCH /complete)
- completed → pending (via PATCH /complete - toggle)

**Relationships**:
- Task belongs to User (user_id foreign key - enforced in Module 2 when users table exists)
- One-to-many: User has many Tasks

### contracts/ Preview

The contracts directory will contain:

**openapi.yaml** - OpenAPI 3.0 specification with:
- All 6 endpoints documented (GET list, POST create, GET single, PUT update, PATCH toggle, DELETE)
- Request/response schemas
- HTTP status codes for each endpoint
- Query parameters (status, sort)
- Error response schemas

**README.md** - Human-readable API documentation with:
- Authentication requirements (note: deferred to Module 2)
- Example requests and responses (cURL commands)
- Error code reference
- Rate limiting notes (N/A for MVP)

### quickstart.md Preview

The quickstart.md file will provide:

1. **Prerequisites**: Python 3.13+, Neon PostgreSQL account, DATABASE_URL
2. **Installation**: `pip install -r requirements.txt`
3. **Configuration**: Copy .env.example to .env, set DATABASE_URL
4. **Running locally**: `uvicorn src.main:app --reload --port 8000`
5. **Testing**: Manual testing checklist with cURL commands
6. **Common issues**: Troubleshooting guide (connection errors, CORS issues)

---

## Next Steps

1. **Complete Phase 0**: Execute research tasks and consolidate findings in research.md
2. **Complete Phase 1**: Generate data-model.md, contracts/openapi.yaml, quickstart.md
3. **Update Agent Context**: Run `.specify/scripts/powershell/update-agent-context.ps1 -AgentType claude`
4. **Proceed to /sp.tasks**: Generate executable task list for implementation
5. **Implementation**: Follow spec-driven development workflow (tasks → implementation → testing)

---

## Design Decisions Log

**Decision 1**: Use Repository Pattern
- **Rationale**: Standard for FastAPI + SQLModel, enables testability, isolates data access
- **Alternatives Considered**: Direct database queries in route handlers (rejected - violates separation of concerns)
- **Impact**: Adds ~100 lines of code, but improves maintainability significantly

**Decision 2**: Separate Pydantic Schemas from SQLModel Models
- **Rationale**: API contracts should be independent of database schema (DTO pattern)
- **Alternatives Considered**: Use SQLModel for both API and database (rejected - tight coupling)
- **Impact**: Slight duplication, but clear separation between API and database concerns

**Decision 3**: Connection Pooling with SQLModel Defaults
- **Rationale**: SQLModel provides sensible defaults (5-10 connections), sufficient for MVP
- **Alternatives Considered**: Custom pool configuration (deferred until performance testing)
- **Impact**: Simplifies initial implementation, can be optimized later if needed

**Decision 4**: Manual Testing Only for MVP
- **Rationale**: Automated tests deferred to post-MVP per constitution's focus on rapid delivery
- **Alternatives Considered**: Full pytest suite (deferred - not required for MVP validation)
- **Impact**: Faster initial delivery, testing checklist ensures quality

**Decision 5**: No Soft Delete
- **Rationale**: Hard delete simplifies implementation, no requirement for "undo" functionality
- **Alternatives Considered**: Soft delete with is_deleted flag (rejected - YAGNI for MVP)
- **Impact**: Permanent deletion, but aligns with spec requirements
