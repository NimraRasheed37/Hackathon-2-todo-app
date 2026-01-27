# Tasks: Integration, Testing & Deployment

**Input**: Design documents from `phase-2/specs/004-integration-deployment/`
**Prerequisites**: plan.md (complete), spec.md (complete), research.md (complete), data-model.md (complete), quickstart.md (complete), contracts/README.md (complete)

**Tests**: Manual testing included. Automated tests deferred (infrastructure/deployment module).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Root**: Repository root (Hackathon-2-todo-app/)
- **Backend**: `phase-2/backend/`
- **Frontend**: `phase-2/frontend/`
- **Specs**: `phase-2/specs/004-integration-deployment/`

---

## Progress Summary

| Metric | Count |
|--------|-------|
| Total Tasks | 39 |
| Completed Tasks | 22 |
| Pending Tasks | 17 |

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Verify existing structure and prepare for integration

- [x] T001 Verify project structure matches plan.md (phase-1/, phase-2/backend/, phase-2/frontend/ exist)
- [x] T002 [P] Verify backend .env.example exists at phase-2/backend/.env.example
- [x] T003 [P] Verify frontend .env.example exists at phase-2/frontend/.env.example

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before user stories

**⚠️ CRITICAL**: All user stories depend on this phase

- [x] T004 Update root .gitignore to include both Python and Node.js artifacts at .gitignore
- [x] T005 [P] Create root .env.example with shared variables (JWT_SECRET, DATABASE_URL) at .env.example

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Monorepo Setup (Priority: P1) 🎯 MVP

**Goal**: Well-organized monorepo structure that's easy to understand and navigate

**Independent Test**: Clone repo, verify directory structure matches spec, confirm documentation files exist at root

### Implementation for User Story 1

- [x] T006 [US1] Verify and update directory structure documentation in README.md placeholder at README.md
- [x] T007 [US1] Ensure phase-1/ and phase-2/ separation is clear (verify no mixing of legacy and new code)

**Checkpoint**: Monorepo structure is clean and documented

---

## Phase 4: User Story 2 - End-to-End Integration (Priority: P1) 🎯 MVP

**Goal**: Frontend and backend work together seamlessly

**Independent Test**: Start both services, register user, login, create/edit/delete tasks, verify persistence

### Implementation for User Story 2

- [x] T008 [US2] Verify CORS configuration in phase-2/backend/src/main.py allows frontend origin
- [x] T009 [US2] Verify JWT token flow from Better Auth to backend API in phase-2/frontend/src/lib/api.ts
- [ ] T010 [US2] Test authentication end-to-end (register → login → API call → logout)
- [ ] T011 [US2] Test CRUD operations end-to-end (create → read → update → delete tasks)

**Checkpoint**: Full-stack integration verified

---

## Phase 5: User Story 3 - Local Development Environment (Priority: P1) 🎯 MVP

**Goal**: Docker Compose setup for easy local development

**Independent Test**: Run `docker-compose up` and access app at localhost:3000

### Implementation for User Story 3

- [x] T012 [P] [US3] Create Dockerfile for backend at phase-2/backend/Dockerfile
- [x] T013 [P] [US3] Create Dockerfile for frontend at phase-2/frontend/Dockerfile
- [x] T014 [US3] Create docker-compose.yml with backend, frontend, and postgres services at docker-compose.yml
- [x] T015 [US3] Add Docker setup instructions to README.md at README.md
- [ ] T016 [US3] Test docker-compose up starts all services correctly
- [ ] T017 [US3] Verify hot reloading works in Docker (modify file, see change)

**Checkpoint**: Docker Compose works for local development

---

## Phase 6: User Story 4 - Production Deployment (Priority: P1)

**Goal**: Application deployed to production with public URLs

**Independent Test**: Visit production URLs, perform all CRUD operations

### Implementation for User Story 4

- [ ] T018 [US4] Deploy backend to Railway at https://railway.app (configure env vars)
- [ ] T019 [US4] Deploy frontend to Vercel at https://vercel.com (configure env vars)
- [ ] T020 [US4] Update CORS_ORIGINS in backend to include Vercel frontend URL
- [ ] T021 [US4] Test production end-to-end (register → login → CRUD → logout)
- [ ] T022 [US4] Verify HTTPS is enabled on both production URLs

**Checkpoint**: Production deployment complete and tested

---

## Phase 7: User Story 5 - Documentation (Priority: P1)

**Goal**: Comprehensive documentation for hackathon judges and future developers

**Independent Test**: New developer can set up project by following README only

### Implementation for User Story 5

- [x] T023 [P] [US5] Create comprehensive README.md with all required sections at README.md
- [x] T024 [P] [US5] Update CLAUDE.md with project architecture and conventions at CLAUDE.md
- [x] T025 [P] [US5] Create AGENTS.md documenting spec-driven development workflow at AGENTS.md
- [x] T026 [US5] Create DEPLOYMENT.md with production deployment guide at DEPLOYMENT.md
- [x] T027 [US5] Add API endpoint documentation summary to README.md at README.md
- [x] T028 [US5] Add technology stack section to README.md at README.md

**Checkpoint**: All documentation complete and comprehensive

---

## Phase 8: User Story 6 - Demo Video (Priority: P2)

**Goal**: 2-3 minute video showcasing all features

**Independent Test**: Watch video and understand features without running app

### Implementation for User Story 6

- [ ] T029 [US6] Record demo video showing all features (register, login, CRUD, filter, logout)
- [ ] T030 [US6] Upload video to YouTube or Loom
- [ ] T031 [US6] Add video link to README.md at README.md

**Checkpoint**: Demo video complete and linked

---

## Phase 9: User Story 7 - Hackathon Submission (Priority: P1)

**Goal**: Complete submission package meeting all hackathon requirements

**Independent Test**: Review against hackathon checklist

### Implementation for User Story 7

- [x] T032 [US7] Final review: verify no secrets in repo, all .env.example files present
- [ ] T033 [US7] Update live demo URLs in README.md with actual production URLs
- [ ] T034 [US7] Add screenshots/GIFs of the application to README.md
- [ ] T035 [US7] Verify repository is public on GitHub
- [ ] T036 [US7] Run final end-to-end test on production

**Checkpoint**: Hackathon submission ready

---

## Phase 10: Polish & Cross-Cutting Concerns

**Purpose**: Final cleanup and quality checks

- [x] T037 Verify all checklist items in phase-2/specs/004-integration-deployment/checklists/requirements.md
- [x] T038 Run `git grep -i secret` to verify no exposed secrets
- [ ] T039 Clean up any temporary or debug code

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - verification only
- **Foundational (Phase 2)**: Depends on Setup verification
- **User Story 1 (Phase 3)**: Depends on Foundational - Monorepo structure
- **User Story 2 (Phase 4)**: Depends on Foundational - Integration testing
- **User Story 3 (Phase 5)**: Depends on US1, US2 - Docker Compose
- **User Story 4 (Phase 6)**: Depends on US2, US3 - Production deployment
- **User Story 5 (Phase 7)**: Depends on US4 - Documentation with URLs
- **User Story 6 (Phase 8)**: Depends on US4 - Demo video of production
- **User Story 7 (Phase 9)**: Depends on all previous stories - Final submission
- **Polish (Phase 10)**: Depends on all user stories

### User Story Dependencies

```
US1 (Monorepo) ──────────────────────────────┐
                                              │
US2 (Integration) ───────────────────────────┼──► US5 (Documentation) ──► US7 (Submission)
                                              │
US3 (Docker) ─────────► US4 (Deployment) ────┤
                                              │
                                              └──► US6 (Demo Video) ─────►
```

### Parallel Opportunities

- **Phase 1**: T002 and T003 can run in parallel
- **Phase 2**: T004 and T005 can run in parallel
- **Phase 5**: T012 and T013 can run in parallel (Dockerfiles)
- **Phase 7**: T023, T024, and T025 can run in parallel (doc files)

---

## Implementation Strategy

### MVP First (US1 + US2 + US3)

1. Complete Phase 1: Setup verification
2. Complete Phase 2: Foundational (gitignore, env.example)
3. Complete Phase 3: User Story 1 - Monorepo Structure
4. Complete Phase 4: User Story 2 - End-to-End Integration
5. Complete Phase 5: User Story 3 - Docker Compose
6. **STOP and VALIDATE**: Local development works with docker-compose up

### Production Ready (+ US4 + US5)

7. Complete Phase 6: User Story 4 - Production Deployment
8. Complete Phase 7: User Story 5 - Documentation
9. **STOP and VALIDATE**: Production accessible, documentation complete

### Full Submission (+ US6 + US7)

10. Complete Phase 8: User Story 6 - Demo Video (optional)
11. Complete Phase 9: User Story 7 - Hackathon Submission
12. Complete Phase 10: Polish
13. **FINAL**: Submit to hackathon

---

## Manual Testing Checklist

After all tasks complete, verify:

### Integration
- [ ] Frontend registers new user successfully
- [ ] Frontend logs in with registered user
- [ ] JWT token sent to backend API
- [ ] Backend validates JWT and returns user's tasks
- [ ] Create, edit, complete, delete tasks work end-to-end
- [ ] Logout clears session and redirects to login

### Docker Compose
- [ ] `docker-compose up` starts all services
- [ ] Frontend accessible at http://localhost:3000
- [ ] Backend accessible at http://localhost:8000
- [ ] Database persists data between restarts
- [ ] Hot reloading works for development

### Production
- [ ] Backend accessible via HTTPS
- [ ] Frontend accessible via HTTPS
- [ ] CORS configured correctly (no console errors)
- [ ] All CRUD operations work in production
- [ ] Environment variables configured correctly

### Documentation
- [ ] README has all required sections
- [ ] CLAUDE.md describes project architecture
- [ ] AGENTS.md explains spec-driven workflow
- [ ] DEPLOYMENT.md guides production setup
- [ ] Live demo URLs are working

### Security
- [ ] No secrets in repository
- [ ] All .env files have .example counterparts
- [ ] Production uses HTTPS

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Many tasks are verification/integration rather than new code
- Commit after each logical group of tasks
- Document any issues found during integration testing
- Update URLs in documentation after production deployment
