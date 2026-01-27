# Tasks: Backend API & Database Layer

**Input**: Design documents from `phase-2/specs/001-backend-api-database/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Tests are NOT included as they are deferred to post-MVP per spec assumptions

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story

## Format: `- [ ] [ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app structure**: `phase-2/backend/src/` for backend code
- All file paths shown below are relative to repository root

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure for Phase 2 backend

- [x] T001 Create Phase 2 backend directory structure per plan.md at phase-2/backend/
- [x] T002 Create Python package structure with __init__.py files in phase-2/backend/src/ and subdirectories
- [x] T003 [P] Create requirements.txt with dependencies: FastAPI (0.109.0+), SQLModel (0.0.14+), Uvicorn (0.27.0+), Pydantic v2 (2.5.0+), psycopg2-binary (2.9.9+) in phase-2/backend/
- [x] T004 [P] Create .env.example template with DATABASE_URL, API_PORT, API_HOST, CORS_ORIGINS in phase-2/backend/
- [x] T005 [P] Create .gitignore for Python project (include .env, __pycache__, *.pyc, venv/) in phase-2/backend/
- [x] T006 [P] Create README.md with setup instructions and API overview in phase-2/backend/

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T007 Implement configuration management in phase-2/backend/src/config.py to load DATABASE_URL, API_PORT, API_HOST, CORS_ORIGINS from environment variables
- [x] T008 [P] Implement database connection and session management in phase-2/backend/src/database.py with SQLModel engine, SessionLocal factory, get_session() dependency with pool_pre_ping=True
- [x] T009 [P] Implement logging configuration in phase-2/backend/src/core/logging_config.py with structured logging (JSON for production, readable for development)
- [x] T010 [P] Create custom exception classes in phase-2/backend/src/core/exceptions.py (TaskNotFoundError, ValidationError, DatabaseError)
- [x] T011 Create Task SQLModel entity in phase-2/backend/src/models/task.py with fields: id, user_id (indexed), title, description, completed (indexed), created_at, updated_at per data-model.md
- [x] T012 [P] Create Pydantic request schemas in phase-2/backend/src/schemas/task.py: TaskCreate (title required, description optional), TaskUpdate (all fields optional)
- [x] T013 [P] Create Pydantic response schema in phase-2/backend/src/schemas/task.py: TaskRead with all fields including timestamps
- [x] T014 [P] Create error response schema in phase-2/backend/src/schemas/task.py: ErrorResponse with detail, error_code, field
- [x] T015 Implement database session dependency injection in phase-2/backend/src/api/dependencies.py with get_session() using Depends()
- [x] T016 Create FastAPI application entry point in phase-2/backend/src/main.py with app initialization, CORS middleware configuration from CORS_ORIGINS env var (allow_credentials=True)
- [x] T017 Add startup event handler in phase-2/backend/src/main.py to create database tables with SQLModel.metadata.create_all(engine) and verify connection
- [x] T018 [P] Implement global exception handlers in phase-2/backend/src/main.py for HTTPException and generic Exception with standardized error response format
- [x] T019 Create TaskRepository class in phase-2/backend/src/repositories/task_repository.py with __init__(session) constructor

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Database Connection and Initialization (Priority: P1) 🎯 MVP

**Goal**: Backend application automatically connects to Neon PostgreSQL and initializes schema on startup

**Independent Test**: Start backend application and verify: (1) successful database connection logged, (2) tasks table created with indexes, (3) application responds to health check requests

### Implementation for User Story 1

- [x] T020 [US1] Add health check endpoint GET / in phase-2/backend/src/main.py returning {"status": "healthy", "database": "connected"}
- [x] T021 [US1] Implement database connection validation in startup event handler with try/except block, log success or exit with clear error message
- [x] T022 [US1] Add connection pool monitoring to log pool status (connections in use, idle connections) on startup
- [x] T023 [US1] Verify indexes are created on tasks.user_id and tasks.completed fields in startup event handler

**Checkpoint**: At this point, backend starts successfully, connects to database, creates schema with indexes

---

## Phase 4: User Story 2 - List User Tasks (Priority: P1)

**Goal**: Retrieve all tasks for a specific user via GET endpoint with filtering and sorting

**Independent Test**: Send GET requests with different user IDs and query parameters, verify only that user's tasks are returned with correct filtering and sorting

### Implementation for User Story 2

- [x] T024 [P] [US2] Implement get_all_by_user(user_id, status, sort) method in TaskRepository at phase-2/backend/src/repositories/task_repository.py with filtering logic (status: all/pending/completed) and sorting (created/title/updated)
- [x] T025 [P] [US2] Implement get_task_repository() dependency in phase-2/backend/src/api/dependencies.py that creates TaskRepository instance with injected session
- [x] T026 [US2] Implement GET /api/{user_id}/tasks endpoint in phase-2/backend/src/api/routes/tasks.py with query parameters status (default="all") and sort (default="created")
- [x] T027 [US2] Add input validation for status and sort query parameters in GET /api/{user_id}/tasks endpoint, return 400 Bad Request for invalid values
- [x] T028 [US2] Register tasks router in phase-2/backend/src/main.py with app.include_router()

**Checkpoint**: At this point, GET /api/{user_id}/tasks endpoint works with filtering and sorting, data isolation enforced

---

## Phase 5: User Story 3 - Create New Task (Priority: P1)

**Goal**: Create new tasks by posting task data to the API with validation

**Independent Test**: Send POST requests with various task data, verify tasks are created in database with auto-generated IDs and timestamps, validation errors return clear messages

### Implementation for User Story 3

- [x] T029 [P] [US3] Implement create(user_id, task_data) method in TaskRepository at phase-2/backend/src/repositories/task_repository.py that creates Task entity, commits to database, and refreshes to get auto-generated fields
- [x] T030 [US3] Implement POST /api/{user_id}/tasks endpoint in phase-2/backend/src/api/routes/tasks.py accepting TaskCreate schema, calling repository create method
- [x] T031 [US3] Add Pydantic validation error handler to convert ValidationError to standardized error response format with field-specific messages
- [x] T032 [US3] Add title trimming validation using @field_validator in TaskCreate schema to strip whitespace and reject empty titles
- [x] T033 [US3] Return HTTP 201 Created with TaskRead response including auto-generated id, created_at, updated_at timestamps

**Checkpoint**: At this point, POST /api/{user_id}/tasks endpoint creates tasks with validation, returns 201 Created or 400 Bad Request with clear error messages

---

## Phase 6: User Story 4 - Update Existing Task (Priority: P2)

**Goal**: Update task title and/or description via PUT endpoint with ownership validation

**Independent Test**: Create tasks, update them via PUT requests, verify changes are persisted and updated_at timestamp refreshes, cross-user attempts return 404

### Implementation for User Story 4

- [x] T034 [P] [US4] Implement get_by_id_and_user(task_id, user_id) method in TaskRepository at phase-2/backend/src/repositories/task_repository.py that queries task with ownership check
- [x] T035 [US4] Implement update(task_id, user_id, task_update) method in TaskRepository that validates ownership, updates fields from TaskUpdate schema (exclude_unset=True), sets updated_at to current timestamp, commits
- [x] T036 [US4] Implement PUT /api/{user_id}/tasks/{id} endpoint in phase-2/backend/src/api/routes/tasks.py accepting TaskUpdate schema, calling repository update method
- [x] T037 [US4] Add model validator to TaskUpdate schema to ensure at least one field is provided for update, raise ValueError if all fields are None
- [x] T038 [US4] Return HTTP 200 OK with updated TaskRead response, or 404 Not Found if task doesn't exist or doesn't belong to user

**Checkpoint**: At this point, PUT /api/{user_id}/tasks/{id} endpoint updates tasks with ownership validation, returns 200 OK or 404 Not Found

---

## Phase 7: User Story 5 - Toggle Task Completion (Priority: P2)

**Goal**: Toggle task completion status via PATCH endpoint with simple toggle behavior

**Independent Test**: Create tasks, repeatedly toggle completion status, verify boolean field toggles between true/false and timestamps update

### Implementation for User Story 5

- [x] T039 [US5] Implement toggle_complete(task_id, user_id) method in TaskRepository at phase-2/backend/src/repositories/task_repository.py that validates ownership, toggles completed field, sets updated_at to current timestamp, commits
- [x] T040 [US5] Implement PATCH /api/{user_id}/tasks/{id}/complete endpoint in phase-2/backend/src/api/routes/tasks.py with no request body, calling repository toggle_complete method
- [x] T041 [US5] Return HTTP 200 OK with updated TaskRead response showing new completion status, or 404 Not Found if task doesn't exist or doesn't belong to user

**Checkpoint**: At this point, PATCH /api/{user_id}/tasks/{id}/complete endpoint toggles completion status, returns 200 OK or 404 Not Found

---

## Phase 8: User Story 6 - Delete Task (Priority: P3)

**Goal**: Permanently delete tasks via DELETE endpoint with ownership validation

**Independent Test**: Create tasks, delete them, verify they no longer appear in list requests and are removed from database

### Implementation for User Story 6

- [x] T042 [US6] Implement delete(task_id, user_id) method in TaskRepository at phase-2/backend/src/repositories/task_repository.py that validates ownership, deletes task from database, commits, returns boolean success status
- [x] T043 [US6] Implement DELETE /api/{user_id}/tasks/{id} endpoint in phase-2/backend/src/api/routes/tasks.py calling repository delete method
- [x] T044 [US6] Return HTTP 204 No Content on successful deletion, or 404 Not Found if task doesn't exist or doesn't belong to user

**Checkpoint**: At this point, DELETE /api/{user_id}/tasks/{id} endpoint permanently removes tasks, returns 204 No Content or 404 Not Found

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and final validation

- [x] T045 [P] Add GET /api/{user_id}/tasks/{id} endpoint in phase-2/backend/src/api/routes/tasks.py for single task retrieval with ownership validation
- [x] T046 [P] Add request ID middleware in phase-2/backend/src/main.py to generate unique request IDs and include in response headers (X-Request-ID)
- [x] T047 [P] Enhance logging to include request ID in all log statements for request correlation
- [x] T048 [P] Add comprehensive docstrings to all public functions and classes following Google/NumPy docstring format
- [x] T049 Verify all error responses follow standardized format with detail, error_code, field per FR-036
- [x] T050 Validate CORS configuration allows credentials and accepts origins from CORS_ORIGINS environment variable
- [ ] T051 Run manual testing checklist from quickstart.md covering all 6 endpoints with valid and invalid data
- [x] T052 [P] Create Dockerfile for containerization with Python 3.13+ base image, install dependencies, expose port 8000 in phase-2/backend/
- [x] T053 [P] Update README.md with API endpoint documentation, environment variable requirements, testing instructions in phase-2/backend/

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-8)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Phase 9)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 3 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 4 (P2)**: Depends on User Story 2 (needs get_by_id_and_user method)
- **User Story 5 (P2)**: Depends on User Story 2 (needs get_by_id_and_user method)
- **User Story 6 (P3)**: Depends on User Story 2 (needs get_by_id_and_user method)

### Within Each User Story

- Repository methods before endpoint implementation
- Validation before error handling
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel (T003, T004, T005, T006)
- All Foundational tasks marked [P] can run in parallel after T007-T008 complete:
  - T009 (logging), T010 (exceptions), T012-T014 (schemas), T018 (error handlers)
- Once Foundational phase completes:
  - User Stories 1, 2, 3 can start in parallel (independent P1 stories)
  - After US2 completes, US4, US5, US6 can start in parallel (depend on US2 repository method)
- Within each story:
  - Repository methods marked [P] can run in parallel
  - Schemas marked [P] can run in parallel

---

## Parallel Example: Foundational Phase

```bash
# After T007-T008 complete, launch these in parallel:
Task T009: "Implement logging configuration in phase-2/backend/src/core/logging_config.py"
Task T010: "Create custom exception classes in phase-2/backend/src/core/exceptions.py"
Task T012: "Create Pydantic request schemas in phase-2/backend/src/schemas/task.py"
Task T013: "Create Pydantic response schema in phase-2/backend/src/schemas/task.py"
Task T014: "Create error response schema in phase-2/backend/src/schemas/task.py"
Task T018: "Implement global exception handlers in phase-2/backend/src/main.py"
```

## Parallel Example: Priority 1 User Stories

```bash
# After Foundational phase complete, launch P1 stories in parallel:
Task: "User Story 1 - Database Connection (T020-T023)"
Task: "User Story 2 - List Tasks (T024-T028)"
Task: "User Story 3 - Create Task (T029-T033)"
```

## Parallel Example: Priority 2 User Stories

```bash
# After US2 completes, launch P2 stories in parallel:
Task: "User Story 4 - Update Task (T034-T038)"
Task: "User Story 5 - Toggle Completion (T039-T041)"
```

---

## Implementation Strategy

### MVP First (User Stories 1-3 Only)

1. Complete Phase 1: Setup (T001-T006)
2. Complete Phase 2: Foundational (T007-T019) - CRITICAL, blocks all stories
3. Complete Phase 3: User Story 1 - Database Connection (T020-T023)
4. Complete Phase 4: User Story 2 - List Tasks (T024-T028)
5. Complete Phase 5: User Story 3 - Create Task (T029-T033)
6. **STOP and VALIDATE**: Test all three P1 user stories independently
7. Deploy/demo if ready - this is a functional MVP (view, create, list tasks)

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Verify database connection
3. Add User Story 2 → Test independently → List tasks works
4. Add User Story 3 → Test independently → Create tasks works (MVP!)
5. Add User Story 4 → Test independently → Update tasks works
6. Add User Story 5 → Test independently → Toggle completion works
7. Add User Story 6 → Test independently → Delete tasks works
8. Add Polish (Phase 9) → Final validation and deployment

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together (T001-T019)
2. Once Foundational is done:
   - Developer A: User Story 1 (T020-T023)
   - Developer B: User Story 2 (T024-T028)
   - Developer C: User Story 3 (T029-T033)
3. After US2 completes:
   - Developer A: User Story 4 (T034-T038)
   - Developer B: User Story 5 (T039-T041)
   - Developer C: User Story 6 (T042-T044)
4. All developers: Polish tasks in parallel (T045-T053)

---

## Notes

- [P] tasks = different files, no dependencies within phase
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Tests deferred to post-MVP per spec assumptions - manual testing via quickstart.md
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence

---

## Summary

- **Total Tasks**: 53 tasks
- **Setup**: 6 tasks
- **Foundational**: 13 tasks (BLOCKS all user stories)
- **User Story 1 (P1)**: 4 tasks - Database Connection
- **User Story 2 (P1)**: 5 tasks - List Tasks
- **User Story 3 (P1)**: 5 tasks - Create Task
- **User Story 4 (P2)**: 5 tasks - Update Task
- **User Story 5 (P2)**: 3 tasks - Toggle Completion
- **User Story 6 (P3)**: 3 tasks - Delete Task
- **Polish**: 9 tasks - Cross-cutting concerns

**Parallelization Opportunities**:
- 4 parallel tasks in Setup phase
- 6 parallel tasks in Foundational phase
- 3 parallel user stories after Foundational complete (US1, US2, US3)
- 3 parallel user stories after US2 complete (US4, US5, US6)
- 4 parallel tasks in Polish phase

**Suggested MVP Scope**: Complete through Phase 5 (User Story 3) for functional task management (database connection, list tasks, create tasks)
