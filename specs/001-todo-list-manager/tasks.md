# Tasks: Todo List Manager

**Input**: Design documents from `specs/001-todo-list-manager/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/, quickstart.md

**Tests**: The examples below include test tasks. Tests are MANDATORY as per the constitution.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies on incomplete tasks)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `todo_cli/`, `tests/` at repository root
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project directory `todo_cli/` and `tests/`.
- [X] T002 Create empty `todo_cli/__init__.py` and `tests/__init__.py`.
- [X] T003 Create `requirements.txt` with `pytest` dependency at project root.
- [X] T004 Create `.gitignore` at project root to exclude common Python build/cache files (`__pycache__`, `.pytest_cache`, `*.pyc`, `todos.json`).
- [X] T005 Initialize `todo_cli/main.py` as the application entry point with a basic `if __name__ == "__main__":` block.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T006 [P] Implement `Task` class in `todo_cli/models.py`, including `id`, `title`, `description`, `created_date`, `completed` attributes, and methods for serialization/deserialization to/from a dictionary.
- [X] T007 [P] Implement initial `Storage` class in `todo_cli/storage.py` with placeholder methods for `load_tasks()` (reads `todos.json`) and `save_tasks()` (writes to `todos.json`), handling empty/missing file gracefully.
- [X] T008 Configure initial `pytest` setup (e.g., `pytest.ini` for basic settings, if needed).

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add Task (Priority: P1) 🎯 MVP

**Goal**: Allow users to add a new task with a title and optional description, saving it to `todos.json`.

**Independent Test**: User can add a task via the CLI and then immediately view it in the task list.

### Tests for User Story 1 (MANDATORY) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T009 [P] [US1] Unit test `Task` class creation, attribute assignment, and serialization/deserialization in `tests/unit/test_models.py`.
- [X] T010 [P] [US1] Unit test `Storage.save_tasks` and `Storage.load_tasks` for new tasks and graceful handling of an empty/missing `todos.json` file in `tests/unit/test_storage.py`.
- [X] T011 [US1] Integration test the CLI's "Add Task" flow, verifying new tasks are added and persisted, in `tests/unit/test_cli.py`.

### Implementation for User Story 1

- [X] T012 [P] [US1] Implement `add_task` method in `todo_cli/storage.py` to add a new `Task` object to the in-memory list and persist it to `todos.json`.
- [X] T013 [US1] Implement a CLI function in `todo_cli/cli.py` to prompt the user for a task title and optional description, then call `storage.add_task`.
- [X] T014 [US1] Integrate the "Add Task" option into the main application menu loop in `todo_cli/main.py`.

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - View All Tasks (Priority: P1)

**Goal**: Display all tasks from `todos.json` in a formatted, sorted list via the CLI.

**Independent Test**: User can add multiple tasks and then view them all correctly sorted and formatted in the list.

### Tests for User Story 2 (MANDATORY) ⚠️

- [X] T015 [P] [US2] Unit test the sorting logic for a list of `Task` objects (by `created_date`) in `tests/unit/test_models.py`.
- [X] T016 [P] [US2] Unit test `Storage.load_tasks` when `todos.json` contains multiple tasks, verifying correct loading and deserialization, in `tests/unit/test_storage.py`.
- [X] T017 [US2] Integration test the CLI's "View All Tasks" flow, verifying correct display formatting and handling of an empty task list, in `tests/unit/test_cli.py`.

### Implementation for User Story 2

- [X] T018 [P] [US2] Implement `get_all_tasks` method in `todo_cli/storage.py` to retrieve all tasks from `todos.json`, load them, and return them sorted by `created_date`.
- [X] T019 [US2] Implement a CLI function in `todo_cli/cli.py` to display the formatted list of tasks (ID, title, completion status) obtained from `storage.get_all_tasks`.
- [X] T020 [US2] Integrate the "View All Tasks" option into the main application menu loop in `todo_cli/main.py`.

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Delete Task (Priority: P1)

**Goal**: Allow users to delete a task by its ID with confirmation.

**Independent Test**: User can add a task, then successfully delete it, and verify its absence from the task list.

### Tests for User Story 3 (MANDATORY) ⚠️

- [X] T021 [P] [US3] Unit test `Storage.delete_task` for both existing and non-existent task IDs, verifying state changes in `todos.json`, in `tests/unit/test_storage.py`.
- [X] T022 [US3] Integration test the CLI's "Delete Task" flow, including the confirmation prompt and handling of non-existent IDs, in `tests/unit/test_cli.py`.

### Implementation for User Story 3

- [X] T023 [P] [US3] Implement `delete_task` method in `todo_cli/storage.py` to remove a task by its ID from the in-memory list and `todos.json`.
- [X] T024 [US3] Implement a CLI function for "Delete Task" in `todo_cli/cli.py` to prompt the user for a task ID, ask for confirmation, and call `storage.delete_task`.
- [X] T025 [US3] Integrate the "Delete Task" option into the main application menu loop in `todo_cli/main.py`.

**Checkpoint**: All user stories up to P1 should now be independently functional

---

## Phase 6: User Story 4 - Update Task (Priority: P2)

**Goal**: Enable users to edit the title and/or description of an existing task.

**Independent Test**: User can add a task, update its title and description via the CLI, and confirm the changes are reflected when viewing the task list.

### Tests for User Story 4 (MANDATORY) ⚠️

- [X] T026 [P] [US4] Unit test `Storage.update_task` for updating existing tasks (full and partial updates) and handling non-existent IDs, in `tests/unit/test_storage.py`.
- [X] T027 [US4] Integration test the CLI's "Update Task" flow, verifying correct updates and error handling for invalid IDs, in `tests/unit/test_cli.py`.

### Implementation for User Story 4

- [X] T028 [P] [US4] Implement `update_task` method in `todo_cli/storage.py` to modify an existing task's title and/or description and persist changes.
- [X] T029 [US4] Implement a CLI function for "Update Task" in `todo_cli/cli.py` to prompt for task ID, new title, and new description, then call `storage.update_task`.
- [X] T030 [US4] Integrate the "Update Task" option into the main application menu loop in `todo_cli/main.py`.

**Checkpoint**: User Stories 1, 2, 3, and 4 should all work independently

---

## Phase 7: User Story 5 - Mark as Complete (Priority: P2)

**Goal**: Allow users to toggle the completion status of a task.

**Independent Test**: User can add an incomplete task, mark it complete, then mark it incomplete again via the CLI, and verify status changes in the task list.

### Tests for User Story 5 (MANDATORY) ⚠️

- [X] T031 [P] [US5] Unit test `Task` class method for toggling completion status in `tests/unit/test_models.py`.
- [X] T032 [P] [US5] Unit test `Storage.toggle_task_completion` for existing and non-existent task IDs, verifying state changes in `todos.json`, in `tests/unit/test_storage.py`.
- [X] T033 [US5] Integration test the CLI's "Mark as Complete" flow, verifying status changes and handling of invalid IDs, in `tests/unit/test_cli.py`.

### Implementation for User Story 5

- [X] T034 [P] [US5] Implement `toggle_task_completion` method in `todo_cli/storage.py` to change a task's `completed` status and persist changes.
- [X] T035 [US5] Implement a CLI function for "Mark as Complete" in `todo_cli/cli.py` to prompt for a task ID and call `storage.toggle_task_completion`.
- [X] T036 [US5] Integrate the "Mark as Complete" option into the main application menu loop in `todo_cli/main.py`.

**Checkpoint**: All user stories are now independently functional

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and overall quality.

- [X] T037 [P] Review and refine all user-facing error handling messages and input validation across `todo_cli/cli.py`.
- [X] T038 Refactor common input validation logic into reusable utility functions within `todo_cli/cli.py` or a new `todo_cli/utils.py`.
- [X] T039 Review `specs/001-todo-list-manager/quickstart.md` and update it with final, accurate application usage details, including example inputs/outputs.
- [X] T040 Final code cleanup, ensuring adherence to PEP 8 style guidelines, and adding necessary comments/docstrings for clarity.
- [X] T041 Run all unit tests and generate a code coverage report, ensuring 90%+ coverage for `todo_cli/` components.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately.
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories.
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion.
  - User stories can then proceed sequentially in priority order (P1 → P1 → P1 → P2 → P2).
- **Polish (Phase 8)**: Depends on all desired user stories being complete.

### User Story Dependencies

- All user stories (US1-US5) are designed to be independently testable after the Foundational phase. There are no direct dependencies between user stories that would prevent parallel development, although implementing them in priority order is recommended.

### Within Each User Story

- Tests MUST be written and FAIL before implementation.
- Models and Storage interactions before CLI logic.
- Core implementation before integration into the main menu.
- A user story is considered complete only when its independent test passes.

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel.
- Foundational tasks T006 and T007 can run in parallel.
- Within each user story phase, test tasks marked [P] can run in parallel.
- Within each user story phase, implementation tasks (e.g., model/storage vs. CLI) marked [P] can run in parallel.
- Once the Foundational phase completes, different user stories *could* be worked on in parallel by different team members, though sequential by priority is recommended for a single developer.

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
- [ ] T009 [P] [US1] Unit test `Task` creation and serialization in `tests/unit/test_models.py`
- [ ] T010 [P] [US1] Unit test `Storage.save_tasks` and `load_tasks` methods (including empty file) in `tests/unit/test_storage.py`
- [ ] T011 [US1] Integration test for adding a task via CLI in `tests/unit/test_cli.py`

# Example of parallel implementation tasks for User Story 1:
- [ ] T012 [P] [US1] Implement `add_task` function in `todo_cli/storage.py`
# ... while T013 is being worked on
- [ ] T013 [US1] Implement CLI function for "Add Task" in `todo_cli/cli.py`
```

---

## Implementation Strategy

### MVP First (User Stories 1, 2, 3 Only - P1 features)

1.  Complete Phase 1: Setup
2.  Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3.  Complete Phase 3: User Story 1 (Add Task)
4.  Complete Phase 4: User Story 2 (View All Tasks)
5.  Complete Phase 5: User Story 3 (Delete Task)
6.  **STOP and VALIDATE**: Test User Stories 1, 2, and 3 independently. At this point, the core CRUD operations (Create, Read, Delete) are functional.
7.  Deploy/demo if ready.

### Incremental Delivery

1.  Complete Setup + Foundational → Foundation ready.
2.  Add User Story 1 → Test independently → Deploy/Demo (Basic MVP!).
3.  Add User Story 2 → Test independently → Deploy/Demo.
4.  Add User Story 3 → Test independently → Deploy/Demo.
5.  Add User Story 4 → Test independently → Deploy/Demo.
6.  Add User Story 5 → Test independently → Deploy/Demo.
7.  Each story adds value without breaking previous stories.

### Parallel Team Strategy

With multiple developers:

1.  Team completes Setup + Foundational together.
2.  Once Foundational is done:
    -   Developer A: User Story 1 (Add Task)
    -   Developer B: User Story 2 (View All Tasks)
    -   Developer C: User Story 3 (Delete Task)
    -   Developer D: User Story 4 (Update Task)
    -   Developer E: User Story 5 (Mark as Complete)
3.  Stories complete and integrate independently.

---

## Notes

-   [P] tasks = different files, no dependencies
-   [Story] label maps task to specific user story for traceability
-   Each user story should be independently completable and testable
-   Verify tests fail before implementing
-   Commit after each task or logical group
-   Stop at any checkpoint to validate story independently
-   Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
