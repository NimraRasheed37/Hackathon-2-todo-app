# Implementation Plan: Authentication & User Management

**Branch**: `002-auth-user-management` | **Date**: 2026-01-26 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `phase-2/specs/002-auth-user-management/spec.md`

## Summary

This module implements secure user authentication for the Todo application, enabling user registration, login, session management, and logout. The existing backend API endpoints from Module 1 will be protected with JWT token verification, and data isolation will be enforced to ensure users can only access their own tasks.

**Primary Requirement**: Implement 6 authentication user stories (Registration, Login, Protected API Access, Authorization, Session Management, Logout) with 29 functional requirements ensuring secure, private task management.

**Technical Approach**: Use Better Auth library for frontend authentication (Next.js) with PyJWT for backend JWT verification. Implement JWT middleware in FastAPI to protect all `/api/{user_id}/tasks/*` endpoints. Create users table with UUID primary keys and update tasks table with foreign key constraint.

---

## Technical Context

**Language/Version**:
- Backend: Python 3.13+
- Frontend: TypeScript/Next.js 14+ (for Better Auth integration)

**Primary Dependencies**:
- Backend: PyJWT (2.8.0+), bcrypt (4.1.0+) - for JWT verification and password hashing
- Frontend: Better Auth (0.x) - handles signup/signin, session management, token storage

**Storage**: Neon Serverless PostgreSQL (existing from Module 1, extended with users table)

**Testing**:
- Manual testing with cURL/Postman for JWT-protected endpoints
- Integration testing with frontend authentication flow

**Target Platform**:
- Backend: Linux server (Docker container on Vercel or similar PaaS)
- Frontend: Vercel Edge (Next.js deployment)

**Project Type**: Web (full-stack - backend API + frontend auth library)

**Performance Goals**:
- Registration completion < 30 seconds with valid input
- Login to dashboard < 5 seconds
- Token validation adds < 50ms latency to API requests
- Handle 100 concurrent authentication requests without degradation

**Constraints**:
- JWT tokens MUST expire after 7 days (configurable via environment)
- Passwords MUST be hashed with bcrypt before storage
- Generic error messages for failed login (security - no user enumeration)
- Email comparison MUST be case-insensitive
- JWT secret MUST match between frontend (BETTER_AUTH_SECRET) and backend (JWT_SECRET)

**Scale/Scope**:
- MVP: 100 concurrent users, single-region deployment
- Database: Single Neon instance (auto-scaling)
- No multi-session enforcement for MVP

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Article I: Spec-Driven Development
- ✅ PASS: Comprehensive specification exists with 6 user stories and 29 functional requirements
- ✅ PASS: All acceptance criteria defined in Given/When/Then format
- ✅ PASS: 10 success criteria provide measurable outcomes

### Article III: Security is Non-Negotiable
- ✅ PASS: Authentication implemented with industry-standard JWT tokens
- ✅ PASS: Passwords hashed with bcrypt (secure algorithm)
- ✅ PASS: Data isolation enforced (user_id from JWT matches URL path)
- ✅ PASS: No secrets in code (JWT_SECRET from environment)
- ✅ PASS: Generic error messages prevent user enumeration attacks
- ✅ PASS: Security events logged for audit (login, logout, failed attempts)

### Article IV: Code Quality Standards
- ✅ PASS: Python code will use type hints (Pydantic/PyJWT enforce this)
- ✅ PASS: Authentication middleware follows single responsibility principle
- ✅ PASS: Docstrings for modules, classes, public functions
- ✅ PASS: No print() statements (logging module used)

### Article V: Database Integrity
- ✅ PASS: Primary key (id) on users table (UUID type)
- ✅ PASS: Unique constraint on email column
- ✅ PASS: created_at and updated_at timestamps required
- ✅ PASS: Foreign key constraint (tasks.user_id references users.id)
- ✅ PASS: Cascade delete on user deletion (removes associated tasks)

### Article VI: Performance Requirements
- ✅ PASS: Token validation target < 50ms
- ✅ PASS: Login/registration response targets defined
- ✅ PASS: No blocking operations in auth middleware

### Article IX: API Design Principles
- ✅ PASS: RESTful conventions maintained for protected endpoints
- ✅ PASS: Standard HTTP status codes (401 Unauthorized, 403 Forbidden)
- ✅ PASS: Consistent error response format

### Article X: Error Handling Philosophy
- ✅ PASS: User-friendly error messages (no stack traces)
- ✅ PASS: Generic "Invalid credentials" message for security
- ✅ PASS: Auth errors logged for debugging

### Article XII: Environment Management
- ✅ PASS: JWT_SECRET, JWT_ALGORITHM, JWT_EXPIRATION_DAYS from environment
- ✅ PASS: .env.example will be updated
- ✅ PASS: Different secrets for local vs production

**Constitution Check Result**: ✅ PASSES all articles

---

## Project Structure

### Documentation (this feature)

```text
phase-2/specs/002-auth-user-management/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
│   ├── openapi.yaml    # OpenAPI 3.0 specification for auth endpoints
│   └── README.md       # API documentation
├── spec.md              # Feature specification (already exists)
└── checklists/
    └── requirements.md  # Specification quality checklist (already exists)
```

### Source Code (repository root)

Since this is Phase 2 (full-stack web application), we continue using **Option 2: Web application** structure. Module 2 extends the existing backend with authentication components.

```text
phase-2/
├── backend/
│   ├── src/
│   │   ├── __init__.py
│   │   ├── main.py              # Updated: Add JWT middleware, auth exception handlers
│   │   ├── config.py            # Updated: Add JWT_SECRET, JWT_ALGORITHM, JWT_EXPIRATION_DAYS
│   │   ├── database.py          # Unchanged
│   │   ├── models/
│   │   │   ├── __init__.py      # Updated: Export User model
│   │   │   ├── task.py          # Updated: user_id becomes UUID type with FK constraint
│   │   │   └── user.py          # NEW: SQLModel User entity
│   │   ├── schemas/
│   │   │   ├── __init__.py      # Updated: Export auth schemas
│   │   │   ├── task.py          # Unchanged
│   │   │   └── auth.py          # NEW: TokenPayload, UserInfo schemas
│   │   ├── repositories/
│   │   │   ├── __init__.py      # Unchanged
│   │   │   └── task_repository.py  # Updated: user_id as UUID
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── dependencies.py  # Updated: Add get_current_user dependency
│   │   │   ├── middleware/      # NEW: Middleware directory
│   │   │   │   ├── __init__.py
│   │   │   │   └── auth.py      # NEW: JWT verification middleware
│   │   │   └── routes/
│   │   │       ├── __init__.py
│   │   │       └── tasks.py     # Updated: Use auth dependency
│   │   └── core/
│   │       ├── __init__.py      # Updated: Export auth exceptions
│   │       ├── exceptions.py    # Updated: Add AuthenticationError, AuthorizationError
│   │       ├── logging_config.py  # Unchanged
│   │       └── security.py      # NEW: JWT decode/verify utilities
│   ├── .env.example             # Updated: Add JWT_* variables
│   ├── requirements.txt         # Updated: Add PyJWT, bcrypt
│   └── README.md                # Updated: Add auth documentation
│
└── frontend/                    # Module 3 will implement this
    └── README.md                # Placeholder
```

**Structure Decision**:

We extend the existing Module 1 structure with authentication components:

1. **Middleware Layer** (`api/middleware/`): JWT verification middleware for protected routes
2. **Security Layer** (`core/security.py`): JWT decode/verify utilities, centralized security functions
3. **User Model** (`models/user.py`): New SQLModel entity for user accounts
4. **Auth Schemas** (`schemas/auth.py`): Pydantic models for JWT payload and user info

This maintains the layered architecture from Module 1 while adding authentication as a cross-cutting concern.

---

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

**No violations requiring justification.**

The constitution check passed all articles. Authentication is a fundamental security requirement, not over-engineering.

**Architectural Decisions Aligned with Constitution**:

1. **JWT Middleware Pattern**: Standard approach for FastAPI authentication, minimal overhead
2. **Separate Security Module**: Isolates JWT logic from business logic (separation of concerns)
3. **User Model with UUID**: Industry standard for user IDs, prevents sequential ID enumeration
4. **Cascade Delete**: Ensures referential integrity when users are deleted

---

## Phase 0: Research Tasks

### Research Task 1: PyJWT Token Verification

**Question**: How should we verify JWT tokens issued by Better Auth in the FastAPI backend?

**Why**: Better Auth handles token creation on the frontend; the backend must verify these tokens with the same secret.

**Research Focus**:
- JWT structure (header, payload, signature)
- PyJWT decode and verify functions
- Handling token expiration and invalid signatures
- Extracting user claims (sub, email, name)
- Error handling for malformed tokens

### Research Task 2: Better Auth JWT Structure

**Question**: What is the exact structure of JWT tokens issued by Better Auth?

**Why**: We need to know the exact claims structure to extract user information on the backend.

**Research Focus**:
- Standard Better Auth JWT claims (sub, email, name, iat, exp)
- Token expiration format (Unix timestamp vs ISO date)
- Custom claims if any
- Token storage strategy (httpOnly cookie vs localStorage)
- Authorization header format (Bearer token)

### Research Task 3: UUID Foreign Key with SQLModel

**Question**: How do we implement UUID foreign keys between users and tasks tables in SQLModel?

**Why**: Module 1 uses string user_id, but we need to change to UUID for proper database integrity.

**Research Focus**:
- SQLModel UUID field type (sqlalchemy dialects)
- Foreign key constraint syntax
- Migration strategy from string to UUID
- Neon PostgreSQL UUID support
- Index considerations for UUID columns

### Research Task 4: FastAPI Dependency Injection for Auth

**Question**: What is the best pattern for implementing authentication as a FastAPI dependency?

**Why**: We want to protect routes declaratively without boilerplate in each endpoint.

**Research Focus**:
- Depends() with authentication functions
- Extracting Authorization header
- Raising HTTPException(401) vs custom exceptions
- Passing user info to route handlers
- Optional vs required authentication

### Research Task 5: Security Logging Best Practices

**Question**: What security events should be logged and what format should we use?

**Why**: FR-021 requires logging authorization failures, and SC-010 requires audit logging.

**Research Focus**:
- Events to log (login, logout, failed attempts, authorization failures)
- Log format (structured JSON for SIEM integration)
- Sensitive data handling (never log passwords, mask tokens)
- Log levels for security events
- Request ID correlation for tracing

---

## Phase 1 Design Outputs

### data-model.md Preview

The data-model.md file will document:

**Entity: User (NEW)**
- Primary key: id (UUID, auto-generated)
- Attributes: email (string, unique, case-insensitive), name (string), password_hash (string)
- Timestamps: created_at (auto), updated_at (auto)
- Indexes: email (unique)
- Validation rules: Email format, password min 8 characters (validated on frontend)

**Entity: Task (UPDATED)**
- Foreign key: user_id changed from string to UUID
- Constraint: user_id REFERENCES users(id) ON DELETE CASCADE
- Index: user_id (existing)

**Relationships**:
- User has many Tasks (one-to-many)
- Task belongs to User (FK constraint)
- Cascade delete: Deleting user removes all their tasks

### contracts/ Preview

The contracts directory will contain:

**openapi.yaml** - OpenAPI 3.0 specification additions:
- Security scheme: Bearer JWT authentication
- Updated task endpoints with 401/403 responses
- Token verification patterns

**README.md** - Authentication API documentation:
- JWT token structure and claims
- Authorization header format
- Error responses for auth failures
- Protected vs public endpoints

### quickstart.md Preview

The quickstart.md file will provide:

1. **Prerequisites**: Module 1 complete, JWT_SECRET configured
2. **Environment Setup**: New environment variables (JWT_SECRET, JWT_ALGORITHM, JWT_EXPIRATION_DAYS)
3. **Database Migration**: Run migration to create users table and update tasks FK
4. **Testing**: Manual testing checklist for auth flows
5. **Frontend Integration**: Notes on Better Auth configuration (covered in Module 3)

---

## Next Steps

1. **Complete Phase 0**: Execute research tasks and consolidate findings in research.md
2. **Complete Phase 1**: Generate data-model.md, contracts/openapi.yaml, quickstart.md
3. **Update Agent Context**: Run `.specify/scripts/powershell/update-agent-context.ps1 -AgentType claude`
4. **Proceed to /sp.tasks**: Generate executable task list for implementation
5. **Implementation**: Follow spec-driven development workflow (tasks → implementation → testing)

---

## Design Decisions Log

**Decision 1**: Use PyJWT for Backend Verification Only
- **Rationale**: Better Auth handles token creation on frontend; backend only needs to verify
- **Alternatives Considered**: Implement full auth on backend (rejected - duplicates Better Auth functionality)
- **Impact**: Simpler backend, relies on shared JWT_SECRET between frontend and backend

**Decision 2**: UUID for User IDs
- **Rationale**: Industry standard, prevents sequential ID enumeration, better security
- **Alternatives Considered**: Auto-increment integers (rejected - security concern), ULIDs (rejected - less common)
- **Impact**: Requires migration from string user_id in tasks table

**Decision 3**: JWT Middleware as FastAPI Dependency
- **Rationale**: Declarative protection, clean route handlers, standard FastAPI pattern
- **Alternatives Considered**: Manual header extraction in each route (rejected - boilerplate), Global middleware (rejected - less flexible)
- **Impact**: Auth injected via Depends(), user info available in route handlers

**Decision 4**: Cascade Delete for User Tasks
- **Rationale**: Maintain referential integrity, simplify user deletion
- **Alternatives Considered**: Orphan tasks (rejected - data integrity), Soft delete (rejected - out of scope)
- **Impact**: Deleting user removes all their tasks permanently

**Decision 5**: Generic Error Messages for Auth Failures
- **Rationale**: Security best practice - prevents user enumeration attacks
- **Alternatives Considered**: Specific messages like "Email not found" (rejected - security risk)
- **Impact**: Same "Invalid credentials" message for wrong email or wrong password
