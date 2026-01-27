---
id: 005
title: Manual Testing T046-T049
stage: green
date: 2026-01-26
surface: agent
model: claude-opus-4-5
feature: 002-auth-user-management
branch: 002-auth-user-management
user: user
command: manual testing
labels: ["testing", "authentication", "authorization", "jwt", "manual-testing"]
links:
  spec: phase-2/specs/002-auth-user-management/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - phase-2/backend/src/main.py
  - phase-2/specs/002-auth-user-management/tasks.md
tests:
  - T046: All endpoints require authentication (401 without token) - PASS
  - T047: Authorization/cross-user access blocked (403) - PASS
  - T048: Token expiration handling with WWW-Authenticate header - PASS
  - T049: Quickstart validation checklist (CRUD operations) - PASS
---

## Prompt

complete manual testing by yourself

## Response snapshot

Executed comprehensive manual testing for authentication and authorization:

**Setup:**
- Installed missing dependencies (pydantic-settings, PyJWT, psycopg2-binary, requests)
- Fixed DATABASE_URL in .env with correct Neon credentials
- Created test users in database (user1, user2 with UUIDs)
- Generated JWT tokens for testing

**T046: Authentication Required (7/7 tests passed)**
- GET/POST/PUT/PATCH/DELETE endpoints return 401 without token
- Health check (/) remains public with 200 response

**T047: Authorization/Data Isolation (7/7 tests passed)**
- User1 can access own tasks (200)
- User2 blocked from User1's tasks (403 on all 6 endpoints)

**T048: Token Expiration (3/3 tests passed)**
- Expired token returns 401
- Invalid token returns 401
- WWW-Authenticate: Bearer header present (fixed bug in HTTPException handler)

**T049: Quickstart Checklist (8/8 tests passed)**
- Health check, Create, List, Get, Update, Toggle, Delete, Verify deletion

**Bug Fixed:**
- HTTPException handler was not passing headers to JSONResponse
- Added `headers=exc.headers` to preserve WWW-Authenticate header

All 49/49 tasks for Module 2 now complete.

## Outcome

- Impact: Module 2 (Authentication & User Management) fully tested and validated
- Tests: 25 test cases executed, all passed
- Files: 2 files modified (main.py bug fix, tasks.md status update)
- Next prompts: Proceed to Module 3 (Frontend UI) with Better Auth integration
- Reflection: Manual testing caught a real bug (missing WWW-Authenticate header) that automated tests might have missed

## Evaluation notes (flywheel)

- Failure modes observed: WWW-Authenticate header was missing from 401 responses due to HTTPException handler not passing headers
- Graders run and results (PASS/FAIL): All 4 manual test suites PASS (T046-T049)
- Prompt variant (if applicable): Direct testing execution without user intervention
- Next experiment (smallest change to try): Add automated integration tests for auth flows in future module
