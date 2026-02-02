# Tasks: AI-Powered Todo Chatbot (Phase 3)

**Input**: Design documents from `/specs/003-ai-chatbot/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1-US7)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `phase-2/backend/src/`
- **Frontend**: `phase-2/frontend/src/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Add OpenAI dependency and configure environment

- [x] T001 Add `openai>=1.0.0` to phase-2/backend/requirements.txt
- [x] T002 [P] Add OpenAI configuration settings (OPENAI_API_KEY, OPENAI_MODEL, MAX_CONVERSATION_MESSAGES) in phase-2/backend/src/config.py
- [x] T003 [P] Update phase-2/backend/.env.example with new OpenAI environment variables

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Database models, schemas, and repository that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T004 [P] Create Conversation SQLModel in phase-2/backend/src/models/conversation.py
- [x] T005 [P] Create Message SQLModel in phase-2/backend/src/models/message.py
- [x] T006 Update phase-2/backend/src/models/__init__.py to export Conversation and Message models
- [x] T007 [P] Create ChatRequest and ChatResponse schemas in phase-2/backend/src/schemas/chat.py
- [x] T008 Create ConversationRepository with CRUD operations in phase-2/backend/src/repositories/conversation_repository.py
- [x] T009 Create agents module __init__.py in phase-2/backend/src/agents/__init__.py
- [x] T010 [P] Create OpenAI agent configuration with system prompt in phase-2/backend/src/agents/task_agent.py
- [x] T011 Run database migration to create conversations and messages tables

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Create Tasks via Chat (Priority: P1) 🎯 MVP

**Goal**: Users can tell the AI "add buy milk to my tasks" and have it create a task

**Independent Test**: Send chat message "add buy groceries" and verify task appears in database with correct title and user_id

### Implementation for User Story 1

- [x] T012 [US1] Implement add_task tool function in phase-2/backend/src/agents/tools.py
- [x] T013 [US1] Register add_task tool in OpenAI tools array in phase-2/backend/src/agents/task_agent.py
- [x] T014 [US1] Create POST /api/chat endpoint with JWT auth in phase-2/backend/src/api/routes/chat.py
- [x] T015 [US1] Implement conversation create/load logic in chat endpoint in phase-2/backend/src/api/routes/chat.py
- [x] T016 [US1] Implement OpenAI API call with tool execution loop in phase-2/backend/src/api/routes/chat.py
- [x] T017 [US1] Implement message persistence (save user + assistant messages) in phase-2/backend/src/api/routes/chat.py
- [x] T018 [US1] Register chat router in main.py in phase-2/backend/src/main.py
- [x] T019 [P] [US1] Create chat types (ChatMessage, Conversation) in phase-2/frontend/src/types/index.ts
- [x] T020 [P] [US1] Create chat API client with sendMessage function in phase-2/frontend/src/lib/chat-api.ts
- [x] T021 [US1] Create MessageInput component with text input and send button in phase-2/frontend/src/components/chat/MessageInput.tsx
- [x] T022 [US1] Create MessageList component to display messages in phase-2/frontend/src/components/chat/MessageList.tsx
- [x] T023 [US1] Create ChatInterface container component in phase-2/frontend/src/components/chat/ChatInterface.tsx
- [x] T024 [US1] Create chat page at /chat route in phase-2/frontend/src/app/(protected)/chat/page.tsx

**Checkpoint**: User Story 1 complete - users can create tasks via chat

---

## Phase 4: User Story 2 - List Tasks via Chat (Priority: P1)

**Goal**: Users can ask "what are my tasks?" and see their task list in chat

**Independent Test**: Send "show my tasks" and verify response includes all user's tasks from database

### Implementation for User Story 2

- [x] T025 [US2] Implement list_tasks tool function with status filter in phase-2/backend/src/agents/tools.py
- [x] T026 [US2] Register list_tasks tool in OpenAI tools array in phase-2/backend/src/agents/task_agent.py

**Checkpoint**: User Story 2 complete - users can view tasks via chat

---

## Phase 5: User Story 3 - Complete Tasks via Chat (Priority: P1)

**Goal**: Users can say "mark buy milk as done" and have the AI complete that task

**Independent Test**: Create a task, send "complete buy milk", verify task status changes to completed

### Implementation for User Story 3

- [x] T027 [US3] Implement complete_task tool function with fuzzy matching in phase-2/backend/src/agents/tools.py
- [x] T028 [US3] Register complete_task tool in OpenAI tools array in phase-2/backend/src/agents/task_agent.py
- [x] T029 [US3] Add task matching helper function (by ID or title substring) in phase-2/backend/src/agents/tools.py

**Checkpoint**: User Story 3 complete - users can complete tasks via chat (Core MVP Done!)

---

## Phase 6: User Story 4 - Delete Tasks via Chat (Priority: P2)

**Goal**: Users can say "delete the buy milk task" and have it removed

**Independent Test**: Create a task, send "delete buy milk", verify task is removed from database

### Implementation for User Story 4

- [x] T030 [US4] Implement delete_task tool function in phase-2/backend/src/agents/tools.py
- [x] T031 [US4] Register delete_task tool in OpenAI tools array in phase-2/backend/src/agents/task_agent.py

**Checkpoint**: User Story 4 complete - users can delete tasks via chat

---

## Phase 7: User Story 5 - Update Tasks via Chat (Priority: P2)

**Goal**: Users can say "rename buy milk to buy groceries" and have the AI update the task

**Independent Test**: Create a task, send "change buy milk to buy groceries", verify title is updated

### Implementation for User Story 5

- [x] T032 [US5] Implement update_task tool function in phase-2/backend/src/agents/tools.py
- [x] T033 [US5] Register update_task tool in OpenAI tools array in phase-2/backend/src/agents/task_agent.py

**Checkpoint**: User Story 5 complete - users can update tasks via chat

---

## Phase 8: User Story 6 - Conversation Persistence (Priority: P2)

**Goal**: Chat history persists across sessions so users can continue conversations

**Independent Test**: Have a conversation, refresh page, verify previous messages appear

### Implementation for User Story 6

- [x] T034 [US6] Implement GET /api/conversations endpoint to list user's conversations in phase-2/backend/src/api/routes/chat.py
- [x] T035 [US6] Implement GET /api/conversations/{id} endpoint to load conversation with messages in phase-2/backend/src/api/routes/chat.py
- [x] T036 [US6] Add message history loading (last 50 messages) in chat endpoint in phase-2/backend/src/api/routes/chat.py
- [x] T037 [P] [US6] Add getConversations and getConversation functions to chat API client in phase-2/frontend/src/lib/chat-api.ts
- [x] T038 [US6] Update ChatInterface to load existing conversation on mount in phase-2/frontend/src/components/chat/ChatInterface.tsx
- [x] T039 [US6] Add conversation title auto-generation from first message in phase-2/backend/src/api/routes/chat.py

**Checkpoint**: User Story 6 complete - conversation history persists

---

## Phase 9: User Story 7 - Tab Navigation (Priority: P3)

**Goal**: Users can switch between Dashboard and Chat using tabs

**Independent Test**: Click Dashboard/Chat tabs and verify correct content loads

### Implementation for User Story 7

- [x] T040 [P] [US7] Create TabNavigation component with Dashboard/Chat tabs in phase-2/frontend/src/components/layout/TabNavigation.tsx
- [x] T041 [US7] Update protected layout to include TabNavigation in phase-2/frontend/src/app/(protected)/layout.tsx
- [x] T042 [US7] Style active tab indicator and ensure navigation works in phase-2/frontend/src/components/layout/TabNavigation.tsx

**Checkpoint**: User Story 7 complete - tab navigation between Dashboard and Chat

---

## Phase 10: Polish & Cross-Cutting Concerns

**Purpose**: Error handling, loading states, and final integration

- [x] T043 Add loading state (spinner/disabled input) during AI response in phase-2/frontend/src/components/chat/ChatInterface.tsx
- [x] T044 Add error handling for OpenAI API failures with user-friendly messages in phase-2/backend/src/api/routes/chat.py
- [x] T045 [P] Add ChatError exception class in phase-2/backend/src/core/exceptions.py
- [x] T046 Implement retry with exponential backoff for OpenAI API calls in phase-2/backend/src/agents/task_agent.py
- [x] T047 Add input validation (2000 char limit, empty message check) in phase-2/backend/src/api/routes/chat.py
- [x] T048 [P] Add empty state with welcome message when no conversation exists in phase-2/frontend/src/components/chat/ChatInterface.tsx
- [x] T049 Verify user isolation - ensure all tools filter by user_id from JWT in phase-2/backend/src/agents/tools.py
- [ ] T050 Run quickstart.md validation - test full flow from login to task creation via chat

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup - BLOCKS all user stories
- **User Stories (Phase 3-9)**: All depend on Foundational phase completion
  - US1 (Create) must complete before testing other stories
  - US2-US5 can proceed in any order after US1
  - US6 (Persistence) can proceed after US1
  - US7 (Navigation) is independent of other stories
- **Polish (Phase 10)**: Depends on all desired user stories being complete

### User Story Dependencies

| Story | Depends On | Can Parallelize With |
|-------|------------|----------------------|
| US1 (Create) | Foundational | - |
| US2 (List) | US1 (shares tools.py) | US3-US5 |
| US3 (Complete) | US1 (shares tools.py) | US2, US4-US5 |
| US4 (Delete) | US1 (shares tools.py) | US2-US3, US5 |
| US5 (Update) | US1 (shares tools.py) | US2-US4 |
| US6 (Persistence) | US1 (needs chat endpoint) | US2-US5 |
| US7 (Navigation) | Foundational | US1-US6 |

### Parallel Opportunities

**Within Phase 2 (Foundational)**:
```bash
# These can run in parallel:
Task: T004 "Create Conversation model"
Task: T005 "Create Message model"
Task: T007 "Create chat schemas"
Task: T010 "Create OpenAI agent configuration"
```

**Within Phase 3 (User Story 1)**:
```bash
# Frontend tasks can run in parallel:
Task: T019 "Create chat types"
Task: T020 "Create chat API client"

# Components can run in parallel:
Task: T021 "Create MessageInput component"
Task: T022 "Create MessageList component"
```

**Across User Stories** (after US1 complete):
```bash
# Tools can be added in parallel by different developers:
Developer A: US2 (list_tasks tool)
Developer B: US3 (complete_task tool)
Developer C: US4 (delete_task tool)
```

---

## Implementation Strategy

### MVP First (User Stories 1-3 Only)

1. Complete Phase 1: Setup (T001-T003)
2. Complete Phase 2: Foundational (T004-T011)
3. Complete Phase 3: User Story 1 - Create Tasks (T012-T024)
4. Complete Phase 4: User Story 2 - List Tasks (T025-T026)
5. Complete Phase 5: User Story 3 - Complete Tasks (T027-T029)
6. **STOP and VALIDATE**: Test core chat functionality
7. Deploy/demo core MVP

### Incremental Delivery

1. **MVP**: Setup + Foundational + US1-3 → Core chat works
2. **+Delete/Update**: Add US4-5 → Full CRUD via chat
3. **+Persistence**: Add US6 → History persists
4. **+Navigation**: Add US7 → Tab-based UI
5. **+Polish**: Add Phase 10 → Production-ready

### Task Count Summary

| Phase | Tasks | Parallelizable |
|-------|-------|----------------|
| Setup | 3 | 2 |
| Foundational | 8 | 4 |
| US1 (Create) | 13 | 4 |
| US2 (List) | 2 | 0 |
| US3 (Complete) | 3 | 0 |
| US4 (Delete) | 2 | 0 |
| US5 (Update) | 2 | 0 |
| US6 (Persistence) | 6 | 1 |
| US7 (Navigation) | 3 | 1 |
| Polish | 8 | 3 |
| **Total** | **50** | **15** |

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- MVP scope: US1-US3 (Create, List, Complete tasks via chat)
