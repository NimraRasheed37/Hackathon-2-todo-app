# Tasks: Frontend UI & Task Management

**Input**: Design documents from `phase-2/specs/003-frontend-ui/`
**Prerequisites**: plan.md (complete), spec.md (complete), research.md (complete), data-model.md (complete), contracts/README.md (complete)

**Tests**: Manual testing included. Automated tests deferred to production phase.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Frontend**: `phase-2/frontend/src/`
- **Components**: `phase-2/frontend/src/components/`
- **Library**: `phase-2/frontend/src/lib/`
- **Types**: `phase-2/frontend/src/types/`
- **App**: `phase-2/frontend/src/app/`

---

## Progress Summary

| Metric | Count |
|--------|-------|
| Total Tasks | 55 |
| Completed Tasks | 55 |
| Pending Tasks | 0 |

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create Next.js 14+ app with TypeScript, Tailwind, ESLint, App Router: `npx create-next-app@latest frontend --typescript --tailwind --eslint --app --src-dir --import-alias "@/*"` in phase-2/
- [x] T002 [P] Install core dependencies: `npm install better-auth swr clsx tailwind-merge` in phase-2/frontend/
- [x] T003 [P] Install UI dependencies: `npm install @radix-ui/react-dialog @radix-ui/react-dropdown-menu @radix-ui/react-checkbox @radix-ui/react-alert-dialog lucide-react sonner` in phase-2/frontend/
- [x] T004 [P] Install pg for Better Auth database: `npm install pg @types/pg` in phase-2/frontend/
- [x] T005 Create environment file phase-2/frontend/.env.local with BETTER_AUTH_SECRET, BETTER_AUTH_URL, DATABASE_URL, NEXT_PUBLIC_API_URL
- [x] T006 [P] Create environment example file phase-2/frontend/.env.example documenting required variables

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T007 Create TypeScript types in phase-2/frontend/src/types/index.ts (User, Session, Task, TaskCreate, TaskUpdate, ErrorResponse, FilterStatus, SortOption)
- [x] T008 Create utility functions in phase-2/frontend/src/lib/utils.ts (cn for className merging, formatDate, formatRelativeTime)
- [x] T009 Create Better Auth server configuration in phase-2/frontend/src/lib/auth.ts with PostgreSQL pool and email/password enabled
- [x] T010 Create Better Auth client in phase-2/frontend/src/lib/auth-client.ts with signIn, signUp, signOut, useSession exports
- [x] T011 Create Better Auth API route handler in phase-2/frontend/src/app/api/auth/[...all]/route.ts
- [x] T012 Create API client class in phase-2/frontend/src/lib/api.ts with token management and typed fetch methods for all task endpoints
- [x] T013 Update root layout phase-2/frontend/src/app/layout.tsx with Sonner Toaster component
- [x] T014 [P] Create base Button component in phase-2/frontend/src/components/ui/Button.tsx with variants (primary, secondary, danger, ghost)
- [x] T015 [P] Create base Input component in phase-2/frontend/src/components/ui/Input.tsx with label, error state, and character counter
- [x] T016 [P] Create base Modal component in phase-2/frontend/src/components/ui/Modal.tsx using Radix Dialog
- [x] T017 [P] Create Skeleton loading component in phase-2/frontend/src/components/ui/Skeleton.tsx for content placeholders
- [x] T018 Create auth layout in phase-2/frontend/src/app/(auth)/layout.tsx with centered card design
- [x] T019 Create protected layout in phase-2/frontend/src/app/(protected)/layout.tsx with auth check and redirect

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: Authentication UI (Priority: P0 - Required for All Stories) 🎯 MVP

**Goal**: Users can register, login, and logout to access their tasks

**Independent Test**: Navigate to /login, /register - forms render. Login with valid credentials redirects to /dashboard. Logout returns to /login.

### Implementation for Authentication

- [x] T020 Create LoginForm component in phase-2/frontend/src/components/auth/LoginForm.tsx with email, password fields, loading state, error display
- [x] T021 Create RegisterForm component in phase-2/frontend/src/components/auth/RegisterForm.tsx with name, email, password fields, loading state, error display
- [x] T022 Create LogoutButton component in phase-2/frontend/src/components/auth/LogoutButton.tsx with session clear and redirect
- [x] T023 Create login page in phase-2/frontend/src/app/(auth)/login/page.tsx using LoginForm component
- [x] T024 Create register page in phase-2/frontend/src/app/(auth)/register/page.tsx using RegisterForm component
- [x] T025 Update home page phase-2/frontend/src/app/page.tsx to redirect to /dashboard if authenticated or /login if not

**Checkpoint**: At this point, authentication flow should be fully functional and testable independently

---

## Phase 4: User Story 1 - View Task Dashboard (Priority: P1) 🎯 MVP

**Goal**: Users can see all their tasks in a clean, organized dashboard

**Independent Test**: Login, navigate to /dashboard - tasks display in cards, counts shown, empty state if no tasks, responsive layout works

### Implementation for User Story 1

- [x] T026 [P] [US1] Create EmptyState component in phase-2/frontend/src/components/ui/EmptyState.tsx with icon, title, description, action button props
- [x] T027 [P] [US1] Create TaskCard component in phase-2/frontend/src/components/tasks/TaskCard.tsx with checkbox, title, description, timestamps, edit/delete buttons (hover)
- [x] T028 [US1] Create TaskList component in phase-2/frontend/src/components/tasks/TaskList.tsx with grid layout, loading skeletons, empty state
- [x] T029 [US1] Create useTasks hook in phase-2/frontend/src/lib/hooks/useTasks.ts using SWR for fetching and caching tasks
- [x] T030 [US1] Create dashboard page in phase-2/frontend/src/app/(protected)/dashboard/page.tsx with header, task counts, TaskList component
- [x] T031 [US1] Add responsive grid layout to TaskList (1 col mobile, 2 col tablet, 2-3 col desktop)
- [x] T032 [US1] Add task count display to dashboard header (X pending, Y completed)

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 5: User Story 2 - Create New Task (Priority: P1) 🎯 MVP

**Goal**: Users can quickly add new tasks without interrupting their flow

**Independent Test**: Click "Add Task" button - modal opens. Fill title, submit - task appears immediately. Success toast shown.

### Implementation for User Story 2

- [x] T033 [P] [US2] Create Textarea component in phase-2/frontend/src/components/ui/Textarea.tsx with character counter for description
- [x] T034 [US2] Create TaskForm component in phase-2/frontend/src/components/tasks/TaskForm.tsx with title (required), description (optional), character counters, submit disabled until valid
- [x] T035 [US2] Create AddTaskModal component in phase-2/frontend/src/components/tasks/AddTaskModal.tsx using Modal and TaskForm
- [x] T036 [US2] Implement createTask in useTasks hook with SWR mutate for optimistic update
- [x] T037 [US2] Add "Add New Task" button to dashboard header that opens AddTaskModal
- [x] T038 [US2] Add success toast on task creation, error toast with retry on failure

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 6: User Story 3 - Edit Existing Task (Priority: P1) 🎯 MVP

**Goal**: Users can update task details as things change

**Independent Test**: Click edit button on task - modal opens with pre-filled data. Update title/description, submit - changes reflect immediately.

### Implementation for User Story 3

- [x] T039 [US3] Create EditTaskModal component in phase-2/frontend/src/components/tasks/EditTaskModal.tsx using Modal and TaskForm with initialData
- [x] T040 [US3] Implement updateTask in useTasks hook with SWR mutate for optimistic update
- [x] T041 [US3] Add edit button to TaskCard that opens EditTaskModal with task data
- [x] T042 [US3] Add success toast on task update, error toast with retry on failure

**Checkpoint**: At this point, User Stories 1, 2, AND 3 should all work independently

---

## Phase 7: User Story 4 - Mark Task Complete/Incomplete (Priority: P1) 🎯 MVP

**Goal**: Users can toggle task completion with a single click

**Independent Test**: Click checkbox on pending task - toggles to completed with strikethrough. Click again - toggles back. Animation plays.

### Implementation for User Story 4

- [x] T043 [US4] Implement toggleComplete in useTasks hook with SWR mutate for optimistic update
- [x] T044 [US4] Add Radix Checkbox to TaskCard with onChange calling toggleComplete
- [x] T045 [US4] Add visual styling for completed tasks (strikethrough title, dimmed text, different background)
- [x] T046 [US4] Add smooth transition animation on completion toggle (opacity, strikethrough)

**Checkpoint**: At this point, User Stories 1-4 should all work independently

---

## Phase 8: User Story 5 - Delete Task (Priority: P2)

**Goal**: Users can remove tasks they no longer need

**Independent Test**: Click delete button - confirmation dialog appears. Confirm - task removed immediately. Cancel - task remains.

### Implementation for User Story 5

- [x] T047 [US5] Create DeleteConfirmDialog component in phase-2/frontend/src/components/tasks/DeleteConfirmDialog.tsx using Radix AlertDialog
- [x] T048 [US5] Implement deleteTask in useTasks hook with SWR mutate for optimistic update
- [x] T049 [US5] Add delete button to TaskCard that opens DeleteConfirmDialog
- [x] T050 [US5] Add success toast on task deletion, error toast with retry on failure

**Checkpoint**: At this point, User Stories 1-5 should all work independently

---

## Phase 9: User Story 6 - Filter and Sort Tasks (Priority: P2)

**Goal**: Users can filter and sort to focus on what matters

**Independent Test**: Click "Pending" filter - only pending tasks shown. Click sort dropdown - tasks reorder. State persists during session.

### Implementation for User Story 6

- [x] T051 [US6] Create TaskFilters component in phase-2/frontend/src/components/tasks/TaskFilters.tsx with All/Pending/Completed buttons showing counts
- [x] T052 [US6] Create SortDropdown component in phase-2/frontend/src/components/tasks/SortDropdown.tsx using Radix DropdownMenu with Newest/Oldest/A-Z options
- [x] T053 [US6] Add filter and sort state to dashboard page with URL search params or React state
- [x] T054 [US6] Update useTasks hook to pass filter and sort params to API call

**Checkpoint**: At this point, User Stories 1-6 should all work independently

---

## Phase 10: User Story 7 - Responsive Design (Priority: P2)

**Goal**: App works beautifully on mobile, tablet, and desktop

**Independent Test**: Resize browser window - layout adapts smoothly. Touch targets are 44x44px minimum on mobile. All features accessible.

### Implementation for User Story 7

- [x] T055 [US7] Audit and fix responsive issues across all components using Tailwind breakpoints (sm, md, lg, xl)

**Checkpoint**: All user stories should now be independently functional

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **Authentication (Phase 3)**: Depends on Foundational - BLOCKS dashboard access
- **User Stories (Phase 4+)**: All depend on Authentication completion
  - US1-US4 are P1/MVP priority - implement first
  - US5-US7 are P2 priority - implement after MVP complete
  - User stories can proceed in parallel (if staffed)
- **Polish (if added)**: Depends on all desired user stories being complete

### User Story Dependencies

- **Authentication (P0)**: BLOCKS all stories - must complete first
- **User Story 1 - Dashboard (P1)**: Can start after Auth - Foundation for other stories
- **User Story 2 - Create (P1)**: Depends on US1 (needs TaskList to show new task)
- **User Story 3 - Edit (P1)**: Depends on US1 (needs TaskCard to add edit button)
- **User Story 4 - Toggle (P1)**: Depends on US1 (needs TaskCard to add checkbox)
- **User Story 5 - Delete (P2)**: Depends on US1 (needs TaskCard to add delete button)
- **User Story 6 - Filter/Sort (P2)**: Depends on US1 (needs TaskList to filter)
- **User Story 7 - Responsive (P2)**: Depends on all UI components existing

### Within Each User Story

- Models/Types before components
- Components before pages
- API integration before user interactions
- Core implementation before polish

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Authentication phase completes, some user story work can overlap
- UI components marked [P] can be built in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: Phase 2 Foundational

```bash
# Launch all UI components together:
Task: "Create base Button component in phase-2/frontend/src/components/ui/Button.tsx"
Task: "Create base Input component in phase-2/frontend/src/components/ui/Input.tsx"
Task: "Create base Modal component in phase-2/frontend/src/components/ui/Modal.tsx"
Task: "Create Skeleton loading component in phase-2/frontend/src/components/ui/Skeleton.tsx"
```

---

## Implementation Strategy

### MVP First (Phase 1-7: Auth + US1-US4)

1. Complete Phase 1: Setup (T001-T006)
2. Complete Phase 2: Foundational (T007-T019)
3. Complete Phase 3: Authentication (T020-T025)
4. Complete Phase 4: User Story 1 - Dashboard (T026-T032)
5. Complete Phases 5-7: User Stories 2-4 (T033-T046)
6. **STOP and VALIDATE**: Test all MVP features end-to-end
7. Deploy/demo if ready

### Full Implementation

1. Complete MVP (above)
2. Add User Story 5 - Delete (T047-T050)
3. Add User Story 6 - Filter/Sort (T051-T054)
4. Add User Story 7 - Responsive Polish (T055)
5. Full end-to-end testing

---

## Manual Testing Checklist

After all tasks complete, verify:

### Authentication
- [ ] Register new user works
- [ ] Login with valid credentials works
- [ ] Login with invalid credentials shows error
- [ ] Logout clears session and redirects
- [ ] Protected routes redirect to login when not authenticated

### Task Operations
- [ ] Dashboard shows task list
- [ ] Empty state shows when no tasks
- [ ] Create task via modal works
- [ ] Edit task via modal works
- [ ] Toggle completion works with animation
- [ ] Delete with confirmation works
- [ ] Success/error toasts appear appropriately

### Filter & Sort
- [ ] All/Pending/Completed filters work
- [ ] Sort options work (Newest/Oldest/A-Z)
- [ ] Counts update correctly

### Responsive Design
- [ ] Mobile layout (< 768px) works
- [ ] Tablet layout (768px-1024px) works
- [ ] Desktop layout (> 1024px) works
- [ ] Touch targets are adequate size

### Accessibility
- [ ] All buttons keyboard accessible
- [ ] Modals close with Escape
- [ ] Focus visible on interactive elements

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
