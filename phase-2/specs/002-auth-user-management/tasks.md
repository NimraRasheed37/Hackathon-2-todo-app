# Tasks: Authentication & User Management

**Input**: Design documents from `phase-2/specs/002-auth-user-management/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Manual testing only (no automated tests requested for MVP)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4, US5, US6)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `phase-2/backend/src/` (extending Module 1 structure)

---

## Phase 1: Setup (Dependencies & Configuration)

**Purpose**: Add new dependencies and update configuration for authentication

- [x] T001 Add PyJWT and bcrypt to phase-2/backend/requirements.txt
- [x] T002 [P] Update .env.example with JWT_SECRET, JWT_ALGORITHM, JWT_EXPIRATION_DAYS in phase-2/backend/.env.example
- [x] T003 [P] Update Settings class with JWT configuration in phase-2/backend/src/config.py

---

## Phase 2: Foundational (Core Authentication Infrastructure)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T004 Create User SQLModel entity in phase-2/backend/src/models/user.py
- [x] T005 Update Task model with UUID user_id and FK constraint in phase-2/backend/src/models/task.py
- [x] T006 [P] Export User model from phase-2/backend/src/models/__init__.py
- [x] T007 Create TokenPayload Pydantic schema in phase-2/backend/src/schemas/auth.py
- [x] T008 [P] Export auth schemas from phase-2/backend/src/schemas/__init__.py
- [x] T009 Create JWT verification utilities in phase-2/backend/src/core/security.py
- [x] T010 Add AuthenticationError and AuthorizationError to phase-2/backend/src/core/exceptions.py
- [x] T011 [P] Export auth exceptions from phase-2/backend/src/core/__init__.py
- [x] T012 Create middleware directory with __init__.py at phase-2/backend/src/api/middleware/__init__.py
- [x] T013 Create JWT verification middleware in phase-2/backend/src/api/middleware/auth.py
- [x] T014 Add get_current_user dependency in phase-2/backend/src/api/dependencies.py
- [x] T015 Add auth exception handlers to phase-2/backend/src/main.py
- [x] T016 Update database.py to import User model for table creation in phase-2/backend/src/database.py

**Checkpoint**: Authentication infrastructure ready - user story implementation can now begin

---

## Phase 3: User Story 1 - User Registration (Priority: P1) 🎯 MVP

**Goal**: Allow new users to sign up with email and password

**Independent Test**: Submit registration form with valid/invalid inputs, verify account creation and error messages

**Note**: Registration is handled by Better Auth on the frontend. Backend only stores users created by Better Auth.

### Implementation for User Story 1

- [x] T017 [US1] Add security logging helper function to phase-2/backend/src/core/security.py
- [x] T018 [US1] Create user repository with create method in phase-2/backend/src/repositories/user_repository.py (for future use)
- [x] T019 [P] [US1] Export user repository from phase-2/backend/src/repositories/__init__.py

**Checkpoint**: User model and repository ready for Better Auth integration

---

## Phase 4: User Story 2 - User Login (Priority: P1)

**Goal**: Allow registered users to sign in and receive JWT token

**Independent Test**: Submit login form with correct/incorrect credentials, verify token issuance

**Note**: Login is handled by Better Auth on the frontend. Backend verifies tokens issued by Better Auth.

### Implementation for User Story 2

- [x] T020 [US2] Add token expiration validation helper to phase-2/backend/src/core/security.py
- [x] T021 [US2] Add structured logging for successful token verification in phase-2/backend/src/api/middleware/auth.py

**Checkpoint**: Token verification logging in place

---

## Phase 5: User Story 3 - Protected API Access (Priority: P1)

**Goal**: All API endpoints require valid JWT token

**Independent Test**: Send API requests with/without valid tokens, verify 401 responses for missing/invalid tokens

### Implementation for User Story 3

- [x] T022 [US3] Update GET /api/{user_id}/tasks endpoint with auth dependency in phase-2/backend/src/api/routes/tasks.py
- [x] T023 [US3] Update POST /api/{user_id}/tasks endpoint with auth dependency in phase-2/backend/src/api/routes/tasks.py
- [x] T024 [US3] Update GET /api/{user_id}/tasks/{task_id} endpoint with auth dependency in phase-2/backend/src/api/routes/tasks.py
- [x] T025 [US3] Update PUT /api/{user_id}/tasks/{task_id} endpoint with auth dependency in phase-2/backend/src/api/routes/tasks.py
- [x] T026 [US3] Update PATCH /api/{user_id}/tasks/{task_id}/complete endpoint with auth dependency in phase-2/backend/src/api/routes/tasks.py
- [x] T027 [US3] Update DELETE /api/{user_id}/tasks/{task_id} endpoint with auth dependency in phase-2/backend/src/api/routes/tasks.py
- [x] T028 [US3] Add 401 error logging for auth failures in phase-2/backend/src/api/middleware/auth.py

**Checkpoint**: All task endpoints require valid JWT token

---

## Phase 6: User Story 4 - User Authorization (Priority: P1)

**Goal**: Users can only access their own tasks (data isolation)

**Independent Test**: Have two users, attempt cross-user access, verify 403 responses

### Implementation for User Story 4

- [x] T029 [US4] Add user_id validation helper to compare token sub with URL path in phase-2/backend/src/core/security.py
- [x] T030 [US4] Add authorization check to GET /api/{user_id}/tasks in phase-2/backend/src/api/routes/tasks.py
- [x] T031 [US4] Add authorization check to POST /api/{user_id}/tasks in phase-2/backend/src/api/routes/tasks.py
- [x] T032 [US4] Add authorization check to GET /api/{user_id}/tasks/{task_id} in phase-2/backend/src/api/routes/tasks.py
- [x] T033 [US4] Add authorization check to PUT /api/{user_id}/tasks/{task_id} in phase-2/backend/src/api/routes/tasks.py
- [x] T034 [US4] Add authorization check to PATCH /api/{user_id}/tasks/{task_id}/complete in phase-2/backend/src/api/routes/tasks.py
- [x] T035 [US4] Add authorization check to DELETE /api/{user_id}/tasks/{task_id} in phase-2/backend/src/api/routes/tasks.py
- [x] T036 [US4] Add 403 error logging for authorization failures in phase-2/backend/src/api/routes/tasks.py
- [x] T037 [US4] Update task_repository to accept UUID user_id in phase-2/backend/src/repositories/task_repository.py

**Checkpoint**: All endpoints enforce user_id authorization and data isolation

---

## Phase 7: User Story 5 - Session Management (Priority: P2)

**Goal**: Sessions persist across page refreshes for 7 days

**Independent Test**: Log in, refresh page, verify session remains active

**Note**: Session persistence is handled by Better Auth on the frontend. Backend validates token expiration.

### Implementation for User Story 5

- [x] T038 [US5] Add token expiration checking with detailed error message in phase-2/backend/src/core/security.py
- [x] T039 [US5] Add WWW-Authenticate header to 401 responses in phase-2/backend/src/api/middleware/auth.py

**Checkpoint**: Token expiration properly enforced with clear error messages

---

## Phase 8: User Story 6 - User Logout (Priority: P2)

**Goal**: Users can log out and clear their session

**Independent Test**: Log out, attempt API request, verify 401 response

**Note**: Logout is handled by Better Auth on the frontend. Backend continues to require valid tokens.

### Implementation for User Story 6

- [x] T040 [US6] Add logout event logging capability in phase-2/backend/src/core/security.py
- [x] T041 [US6] Update health check endpoint to exclude auth requirement in phase-2/backend/src/main.py

**Checkpoint**: Logout logging in place, health check remains public

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Documentation, cleanup, and validation

- [x] T042 [P] Update README.md with auth documentation in phase-2/backend/README.md
- [x] T043 [P] Add auth-related types to type hints throughout codebase
- [x] T044 Add structured JSON logging for all security events in phase-2/backend/src/core/logging_config.py
- [x] T045 Update task schemas to use UUID for user_id in phase-2/backend/src/schemas/task.py
- [x] T046 Manual testing: Verify all endpoints require authentication
- [x] T047 Manual testing: Verify authorization (cross-user access blocked)
- [x] T048 Manual testing: Verify token expiration handling
- [x] T049 Run quickstart.md validation checklist

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-8)**: All depend on Foundational phase completion
  - US1-US4 are all P1 priority - implement sequentially or in parallel
  - US5-US6 are P2 priority - implement after P1 stories
- **Polish (Phase 9)**: Depends on all user stories being complete

### User Story Dependencies

| Story | Priority | Dependencies | Can Parallelize With |
|-------|----------|--------------|---------------------|
| US1 (Registration) | P1 | Foundational | US2 |
| US2 (Login) | P1 | Foundational | US1 |
| US3 (Protected API) | P1 | Foundational | None (modifies shared file) |
| US4 (Authorization) | P1 | US3 | None (extends US3 changes) |
| US5 (Session Mgmt) | P2 | Foundational | US6 |
| US6 (Logout) | P2 | Foundational | US5 |

### Within Each User Story

- Security utilities before middleware
- Middleware before route handlers
- Core implementation before logging/polish
- Story complete before moving to next priority

### Parallel Opportunities

**Phase 1 (Setup)**:
- T002, T003 can run in parallel (different files)

**Phase 2 (Foundational)**:
- T006 (after T004), T008, T011 can run in parallel (export updates)
- T012 independent of other tasks

**User Stories**:
- US1 and US2 can run in parallel (different concerns)
- US5 and US6 can run in parallel (both P2)
- US3 must complete before US4 (US4 extends US3 changes)

---

## Parallel Example: Foundational Phase

```bash
# After T004 (User model) completes:
# Launch these in parallel:
Task T006: "Export User model from phase-2/backend/src/models/__init__.py"
Task T008: "Export auth schemas from phase-2/backend/src/schemas/__init__.py"
Task T011: "Export auth exceptions from phase-2/backend/src/core/__init__.py"
Task T012: "Create middleware directory with __init__.py"
```

---

## Implementation Strategy

### MVP First (US1-US4 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phases 3-6: US1, US2, US3, US4 (all P1 priority)
4. **STOP and VALIDATE**: Test all auth flows
5. Deploy/demo if ready

### Incremental Delivery

1. Setup + Foundational → Infrastructure ready
2. Add US3 (Protected API) → All endpoints require auth
3. Add US4 (Authorization) → Data isolation enforced
4. Add US1 + US2 (Registration/Login support) → Full auth flow ready
5. Add US5 + US6 (Session/Logout) → Polish session handling

### Suggested MVP Scope

**P1 Stories (Must Have)**:
- US3: Protected API Access (core security)
- US4: User Authorization (data isolation)
- US1: User Registration (account creation)
- US2: User Login (authentication)

**P2 Stories (Nice to Have)**:
- US5: Session Management
- US6: User Logout

---

## Summary

| Metric | Value |
|--------|-------|
| Total Tasks | 49 |
| Completed Tasks | 49 |
| Pending Tasks | 0 |
| Setup Phase | 3 tasks ✅ |
| Foundational Phase | 13 tasks ✅ |
| US1 (Registration) | 3 tasks ✅ |
| US2 (Login) | 2 tasks ✅ |
| US3 (Protected API) | 7 tasks ✅ |
| US4 (Authorization) | 9 tasks ✅ |
| US5 (Session Mgmt) | 2 tasks ✅ |
| US6 (Logout) | 2 tasks ✅ |
| Polish Phase | 8 tasks ✅ |
| Parallel Opportunities | 12 tasks marked [P] |

---

## Notes

- All tasks extend existing Module 1 codebase - no new files except where noted
- Frontend authentication (Better Auth) is out of scope for this module
- Backend only verifies tokens issued by frontend
- UUID migration assumes fresh database (no data migration for MVP)
- Manual testing replaces automated tests for MVP
