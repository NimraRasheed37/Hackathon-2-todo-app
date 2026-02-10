# Tasks: Phase 5 - Advanced Cloud Deployment

**Input**: Design documents from `/specs/005-advanced-cloud-deployment/`
**Prerequisites**: plan.md, spec.md, data-model.md, contracts/, research.md, quickstart.md

**Tests**: Tests are OPTIONAL - include only if explicitly requested.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create directory structure for k8s/dapr/, k8s/cloud/, k8s/monitoring/, .github/workflows/
- [x] T002 [P] Add aiokafka and dapr-client to phase-2/backend/requirements.txt
- [x] T003 [P] Create phase-2/backend/src/events/ package with __init__.py
- [x] T004 [P] Create phase-2/backend/src/services/ directory if not exists
- [x] T005 [P] Update phase-2/frontend/src/types/task.ts with priority, dueDate, tags, recurrence fields

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Database Migrations

- [x] T006 Create Alembic migration 001: Add priority, due_date, recurrence_pattern, parent_task_id, occurrence_number, search_vector, version columns to tasks table in phase-2/backend/alembic/versions/
- [x] T007 Create Alembic migration 002: Create tags table in phase-2/backend/alembic/versions/
- [x] T008 Create Alembic migration 003: Create task_tags junction table in phase-2/backend/alembic/versions/
- [x] T009 Create Alembic migration 004: Create task_recurrences table in phase-2/backend/alembic/versions/
- [x] T010 Create Alembic migration 005: Create task_reminders table in phase-2/backend/alembic/versions/
- [x] T011 Create Alembic migration 006: Create notifications table in phase-2/backend/alembic/versions/
- [x] T012 Create Alembic migration 007: Create audit_log table in phase-2/backend/alembic/versions/
- [x] T013 Create Alembic migration 008: Add full-text search trigger for tasks in phase-2/backend/alembic/versions/
- [x] T014 Create Alembic migration 009: Add all indexes in phase-2/backend/alembic/versions/

### Event Infrastructure (US6 Foundation)

- [x] T015 Create event schema definitions in phase-2/backend/src/events/schemas.py with TaskEvent, ReminderEvent base classes
- [x] T016 Create Dapr HTTP client wrapper in phase-2/backend/src/events/dapr_client.py for pub/sub and state operations
- [x] T017 Create event producer in phase-2/backend/src/events/producer.py with publish_event() function using Dapr pub/sub

### Dapr Components (US7 Foundation)

- [x] T018 [P] Create Dapr pub/sub component for Kafka in k8s/dapr/components/pubsub-kafka.yaml
- [x] T019 [P] Create Dapr state store component for Redis in k8s/dapr/components/statestore-redis.yaml
- [x] T020 [P] Create Dapr secrets component in k8s/dapr/components/secrets.yaml
- [x] T021 [P] Create Dapr cron binding for recurring tasks in k8s/dapr/components/bindings-cron.yaml
- [x] T022 Create Dapr configuration in k8s/dapr/config/config.yaml

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Recurring Tasks (Priority: P1) 🎯 MVP - 40 points

**Goal**: Users can create tasks that automatically recur on a schedule

**Independent Test**: Create a daily recurring task, complete it, verify a new instance is created for the next day

### Implementation for User Story 1

- [x] T023 [P] [US1] Create TaskRecurrence SQLAlchemy model in phase-2/backend/src/models/recurrence.py
- [x] T024 [P] [US1] Create RecurrencePattern Pydantic schema in phase-2/backend/src/schemas/recurrence.py
- [x] T025 [US1] Create RecurringService with calculate_next_occurrence() and spawn_next_task() in phase-2/backend/src/services/recurring_service.py
- [x] T026 [US1] Create recurring tasks API router with POST/GET/PUT/DELETE /tasks/{task_id}/recurrence in phase-2/backend/src/api/routes/recurring.py
- [x] T027 [US1] Create recurring consumer to handle TaskCompleted events in phase-2/backend/src/events/consumers/recurring_consumer.py
- [x] T028 [US1] Register recurring router in phase-2/backend/src/main.py
- [x] T029 [P] [US1] Create RecurrenceSelector React component in phase-2/frontend/src/components/tasks/RecurrenceSelector.tsx
- [x] T030 [US1] Integrate RecurrenceSelector into task create/edit form in phase-2/frontend/src/components/tasks/TaskForm.tsx

**Checkpoint**: User Story 1 (Recurring Tasks) is fully functional and testable independently

---

## Phase 4: User Story 2 - Task Reminders (Priority: P1) - 35 points

**Goal**: Users receive notifications before task due dates

**Independent Test**: Set a reminder for 15 minutes before due date, verify notification is triggered

### Implementation for User Story 2

- [x] T031 [P] [US2] Create TaskReminder SQLAlchemy model in phase-2/backend/src/models/reminder.py
- [x] T032 [P] [US2] Create Notification SQLAlchemy model in phase-2/backend/src/models/notification.py
- [x] T033 [P] [US2] Create ReminderSchema and NotificationSchema Pydantic models in phase-2/backend/src/schemas/reminder.py
- [x] T034 [US2] Create ReminderService with schedule_reminder() and check_due_reminders() in phase-2/backend/src/services/reminder_service.py
- [x] T035 [US2] Create NotificationService with create_notification() and get_user_notifications() in phase-2/backend/src/services/notification_service.py
- [x] T036 [US2] Create reminders API router with POST/GET/DELETE /tasks/{task_id}/reminders in phase-2/backend/src/api/routes/reminders.py
- [x] T037 [US2] Create notifications API router with GET /notifications in phase-2/backend/src/api/routes/notifications.py
- [x] T038 [US2] Create reminder consumer to handle ReminderDue events in phase-2/backend/src/events/consumers/reminder_consumer.py
- [x] T039 [US2] Register reminder and notification routers in phase-2/backend/src/main.py
- [x] T040 [P] [US2] Create ReminderPicker React component in phase-2/frontend/src/components/tasks/ReminderPicker.tsx
- [x] T041 [P] [US2] Create NotificationBell component for header in phase-2/frontend/src/components/notifications/NotificationBell.tsx
- [x] T042 [US2] Create useNotifications hook for polling notifications in phase-2/frontend/src/hooks/useNotifications.ts

**Checkpoint**: User Story 2 (Reminders) is fully functional and testable independently

---

## Phase 5: User Story 3 - Task Priorities (Priority: P1) - 25 points

**Goal**: Users can assign priority levels to tasks for better organization

**Independent Test**: Create tasks with different priorities, verify sorting and visual indicators work correctly

### Implementation for User Story 3

- [x] T043 [US3] Add priority field handling to existing Task model in phase-2/backend/src/models/task.py
- [x] T044 [US3] Update TaskSchema with priority field and validation in phase-2/backend/src/schemas/task.py
- [x] T045 [US3] Add priority sorting to task list endpoint in phase-2/backend/src/api/routes/tasks.py
- [x] T046 [P] [US3] Create PrioritySelector React component with visual indicators in phase-2/frontend/src/components/tasks/PrioritySelector.tsx
- [x] T047 [US3] Integrate PrioritySelector into TaskForm and update TaskList sorting in phase-2/frontend/src/components/tasks/TaskForm.tsx

**Checkpoint**: User Story 3 (Priorities) is fully functional and testable independently

---

## Phase 6: User Story 4 - Task Tags (Priority: P2) - 25 points

**Goal**: Users can organize tasks with custom tags/labels

**Independent Test**: Create tags, assign to tasks, filter by tags

### Implementation for User Story 4

- [x] T048 [P] [US4] Create Tag SQLAlchemy model in phase-2/backend/src/models/tag.py
- [x] T049 [P] [US4] Create TaskTag association model in phase-2/backend/src/models/tag.py (combined with Tag)
- [x] T050 [P] [US4] Create TagSchema and TaskTagsUpdate Pydantic models in phase-2/backend/src/schemas/tag.py
- [x] T051 [US4] Create TagService with CRUD operations and usage tracking in phase-2/backend/src/services/tag_service.py
- [x] T052 [US4] Create tags API router with GET/POST/PUT/DELETE /tags and POST /tasks/{task_id}/tags in phase-2/backend/src/api/routes/tags.py
- [x] T053 [US4] Register tags router in phase-2/backend/src/main.py
- [x] T054 [P] [US4] Create TagManager React component with color picker in phase-2/frontend/src/components/tasks/TagManager.tsx
- [x] T055 [P] [US4] Create TagBadge component for displaying tags in phase-2/frontend/src/components/tasks/TagManager.tsx (included in TagManager)
- [x] T056 [US4] Integrate TagManager into TaskForm and add tag filter to TaskList in phase-2/frontend/src/components/tasks/TaskForm.tsx

**Checkpoint**: User Story 4 (Tags) is fully functional and testable independently

---

## Phase 7: User Story 5 - Advanced Search (Priority: P2) - 25 points

**Goal**: Users can search tasks with filters and full-text search

**Independent Test**: Search for task by title, filter by status and priority combined

### Implementation for User Story 5

- [x] T057 [P] [US5] Create SearchQuery and SearchResults Pydantic schemas in phase-2/backend/src/schemas/search.py
- [x] T058 [US5] Create SearchService with full-text search using PostgreSQL tsvector in phase-2/backend/src/services/search_service.py
- [x] T059 [US5] Create search API router with POST /tasks/search in phase-2/backend/src/api/routes/search.py
- [x] T060 [US5] Register search router in phase-2/backend/src/main.py
- [x] T061 [P] [US5] Create SearchBar component with filter dropdowns in phase-2/frontend/src/components/search/SearchBar.tsx
- [x] T062 [US5] Create useSearch hook with debounced search in phase-2/frontend/src/hooks/useSearch.ts
- [x] T063 [US5] Integrate SearchBar into dashboard page in phase-2/frontend/src/app/(protected)/dashboard/page.tsx

**Checkpoint**: User Story 5 (Search) is fully functional and testable independently

---

## Phase 8: User Story 6 - Kafka Event Architecture (Priority: P1) - 50 points

**Goal**: All task mutations publish events to Kafka, consumed by services

**Independent Test**: Create a task, verify event is published to Kafka and consumed by audit service

### Implementation for User Story 6

- [x] T064 [US6] Integrate event publishing into task CRUD operations in phase-2/backend/src/api/routes/tasks.py (TaskCreated, TaskUpdated, TaskCompleted, TaskDeleted)
- [x] T065 [US6] Create audit consumer to log all events in phase-2/backend/src/events/consumers/audit_consumer.py
- [x] T066 [US6] Create AuditService to write events to audit_log table in phase-2/backend/src/services/audit_service.py
- [x] T067 [US6] Create consumer startup script to run all Kafka consumers in phase-2/backend/src/events/consumer_runner.py
- [x] T068 [US6] Add consumer runner to Dockerfile and create separate consumer deployment in phase-2/backend/Dockerfile

**Checkpoint**: User Story 6 (Kafka Events) is fully functional with events flowing through system

---

## Phase 9: User Story 7 - Dapr Integration (Priority: P1) - 50 points

**Goal**: Services communicate via Dapr sidecar for pub/sub, state, and invocation

**Independent Test**: Make service invocation via Dapr sidecar, verify request is routed correctly

### Implementation for User Story 7

- [x] T069 [US7] Add Dapr annotations to backend deployment in k8s/cloud/base/backend-deployment.yaml
- [x] T070 [US7] Configure Dapr pub/sub subscription endpoints in phase-2/backend/src/api/routes/subscriptions.py
- [x] T071 [US7] Create Dapr state store client for caching in phase-2/backend/src/services/cache_service.py
- [x] T072 [US7] Update docker-compose.yml to include Dapr sidecar for local development in phase-2/docker-compose.yml
- [x] T073 [US7] Create Dapr app configuration for backend in phase-2/backend/dapr/

**Checkpoint**: User Story 7 (Dapr) is integrated with all services using Dapr building blocks

---

## Phase 10: User Story 8 - Microservices Architecture (Priority: P1) - 30 points

**Goal**: System decomposed into independent, loosely-coupled services

**Independent Test**: Deploy Task Service independently, verify core CRUD works when other services are down

### Implementation for User Story 8

- [ ] T074 [US8] Extract Recurring Service into separate module with own Dockerfile in phase-2/recurring-service/
- [ ] T075 [US8] Extract Reminder Service into separate module with own Dockerfile in phase-2/reminder-service/
- [ ] T076 [US8] Create Kubernetes deployment for Recurring Service in k8s/cloud/base/recurring-deployment.yaml
- [ ] T077 [US8] Create Kubernetes deployment for Reminder Service in k8s/cloud/base/reminder-deployment.yaml
- [ ] T078 [US8] Update k8s/cloud/base/kustomization.yaml to include all service deployments

**Checkpoint**: User Story 8 (Microservices) all services deploy and communicate independently

---

## Phase 11: User Story 9 - Cloud Kubernetes Deployment (Priority: P1) - 30 points

**Goal**: Application deploys to cloud Kubernetes (AKS/GKE/DOKS) with production configuration

**Independent Test**: Deploy to cloud provider, verify all services are healthy and accessible via HTTPS

### Implementation for User Story 9

- [x] T079 [P] [US9] Create Kubernetes namespace and base resources in k8s/cloud/base/namespace.yaml
- [x] T080 [P] [US9] Create Kubernetes secrets manifest (template) in k8s/cloud/base/secrets.yaml
- [x] T081 [P] [US9] Create ConfigMap for environment config in k8s/cloud/base/configmap.yaml
- [x] T082 [US9] Create staging Kustomize overlay with staging-specific config in k8s/cloud/overlays/staging/kustomization.yaml
- [x] T083 [US9] Create production Kustomize overlay with HPA, PDB in k8s/cloud/overlays/production/kustomization.yaml
- [x] T084 [P] [US9] Create DigitalOcean-specific ingress and storage class in k8s/cloud/providers/doks/
- [x] T085 [P] [US9] Create Azure AKS-specific ingress and storage class in k8s/cloud/providers/aks/
- [x] T086 [P] [US9] Create Google GKE-specific ingress and storage class in k8s/cloud/providers/gke/
- [x] T087 [US9] Create deploy.sh script for cloud deployment in scripts/deploy.sh
- [x] T088 [US9] Create rollback.sh script for quick rollback in scripts/rollback.sh

**Checkpoint**: User Story 9 (Cloud K8s) application deploys to cloud with TLS and all services healthy

---

## Phase 12: User Story 10 - CI/CD Pipeline (Priority: P2) - 30 points

**Goal**: Automated CI/CD with GitHub Actions for testing, building, and deploying

**Independent Test**: Push code change, verify pipeline runs and deploys to staging

### Implementation for User Story 10

- [x] T089 [P] [US10] Create CI workflow with test, lint, build stages in .github/workflows/ci.yml
- [x] T090 [P] [US10] Create CD staging workflow with auto-deploy on main in .github/workflows/cd-staging.yml
- [x] T091 [US10] Create CD production workflow with manual approval gate in .github/workflows/cd-production.yml
- [x] T092 [US10] Add GitHub environment secrets documentation in docs/deployment.md

**Checkpoint**: User Story 10 (CI/CD) pipeline runs on push and deploys successfully

---

## Phase 13: User Story 11 - Monitoring & Observability (Priority: P2) - 30 points

**Goal**: Comprehensive monitoring with Prometheus, Grafana, and Loki

**Independent Test**: Generate load, view metrics in Grafana dashboard

### Implementation for User Story 11

- [x] T093 [P] [US11] Create Prometheus deployment and ServiceMonitor in k8s/monitoring/prometheus/prometheus.yaml
- [x] T094 [P] [US11] Create Prometheus alerting rules in k8s/monitoring/prometheus/rules/alerts.yaml
- [x] T095 [P] [US11] Create Grafana deployment with persistence in k8s/monitoring/grafana/grafana.yaml
- [x] T096 [P] [US11] Create Todo App Grafana dashboard JSON in k8s/monitoring/grafana/dashboards/todo-app.json
- [x] T097 [P] [US11] Create Loki deployment for log aggregation in k8s/monitoring/loki/loki.yaml
- [x] T098 [US11] Add Prometheus metrics endpoint to FastAPI in phase-2/backend/src/middleware/metrics.py
- [x] T099 [US11] Register metrics middleware in phase-2/backend/src/main.py
- [x] T100 [US11] Create monitoring kustomization to deploy full stack in k8s/monitoring/kustomization.yaml

**Checkpoint**: User Story 11 (Monitoring) metrics visible in Grafana, logs queryable in Loki

---

## Phase 14: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T101 [P] Update README.md with Phase 5 features and architecture diagram
- [ ] T102 [P] Create docs/architecture.md with system design documentation
- [ ] T103 [P] Create docs/runbook.md with operational procedures
- [ ] T104 Verify all API endpoints have proper error handling and validation
- [ ] T105 Run security scan on container images
- [ ] T106 Validate quickstart.md instructions work end-to-end

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phases 3-13)**: All depend on Foundational phase completion
  - US1-5 (Advanced Features): Can proceed in parallel after Foundational
  - US6-7 (Kafka/Dapr): Can proceed in parallel after Foundational
  - US8 (Microservices): Depends on US6, US7
  - US9 (Cloud K8s): Depends on US8
  - US10 (CI/CD): Depends on US9
  - US11 (Monitoring): Can proceed in parallel with US10
- **Polish (Phase 14)**: Depends on all desired user stories being complete

### User Story Dependencies

```
Foundational (Phase 2)
         │
         ├──► US1 (Recurring) ─────┐
         ├──► US2 (Reminders) ─────┤
         ├──► US3 (Priorities) ────┤
         ├──► US4 (Tags) ──────────┤
         ├──► US5 (Search) ────────┤
         │                         │
         ├──► US6 (Kafka) ─────────┼──► US8 (Microservices) ──► US9 (Cloud K8s) ──► US10 (CI/CD)
         └──► US7 (Dapr) ──────────┘                                    │
                                                                        ├──► US11 (Monitoring)
                                                                        │
                                                                        └──► Polish (Phase 14)
```

### Parallel Opportunities

**Within Phase 1 (Setup)**:
- T002, T003, T004, T005 can all run in parallel

**Within Phase 2 (Foundational)**:
- T018, T019, T020, T021 (Dapr components) can run in parallel
- Database migrations must run sequentially

**Within User Story Phases**:
- Model creation tasks marked [P] can run in parallel
- Frontend component tasks marked [P] can run in parallel
- API routers must wait for models and services

---

## Parallel Example: User Story 1

```bash
# Launch models in parallel:
Task: "Create TaskRecurrence model in phase-2/backend/src/models/recurrence.py"
Task: "Create RecurrencePattern schema in phase-2/backend/src/schemas/recurrence.py"

# Then sequentially:
Task: "Create RecurringService in phase-2/backend/src/services/recurring_service.py"
Task: "Create recurring API router in phase-2/backend/src/api/recurring.py"

# Frontend can start once API exists:
Task: "Create RecurrenceSelector component in phase-2/frontend/src/components/RecurrenceSelector.tsx"
```

---

## Implementation Strategy

### MVP First (P1 Stories Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phases 3-5: US1-3 (Recurring, Reminders, Priorities) - Core features
4. Complete Phases 8-9: US6-7 (Kafka, Dapr) - Event infrastructure
5. Complete Phase 10: US8 (Microservices)
6. Complete Phase 11: US9 (Cloud K8s)
7. **STOP and VALIDATE**: Test all P1 features in cloud environment
8. Deploy/demo MVP

**MVP Points**: 40 + 35 + 25 + 50 + 50 + 30 + 30 = **260 points**

### Incremental Delivery

1. Foundation → US1 (Recurring) → Deploy/Demo
2. Add US2 (Reminders) → Deploy/Demo
3. Add US3 (Priorities) → Deploy/Demo
4. Add US6+7 (Kafka/Dapr) → Deploy/Demo
5. Add US8+9 (Microservices + Cloud) → Deploy/Demo
6. Add US4+5 (Tags, Search) → Deploy/Demo
7. Add US10+11 (CI/CD, Monitoring) → Deploy/Demo
8. Polish → Final Release

---

## Task Summary

| Phase | User Story | Tasks | Points |
|-------|-----------|-------|--------|
| 1 | Setup | 5 | - |
| 2 | Foundational | 17 | - |
| 3 | US1 - Recurring | 8 | 40 |
| 4 | US2 - Reminders | 12 | 35 |
| 5 | US3 - Priorities | 5 | 25 |
| 6 | US4 - Tags | 9 | 25 |
| 7 | US5 - Search | 7 | 25 |
| 8 | US6 - Kafka | 5 | 50 |
| 9 | US7 - Dapr | 5 | 50 |
| 10 | US8 - Microservices | 5 | 30 |
| 11 | US9 - Cloud K8s | 10 | 30 |
| 12 | US10 - CI/CD | 4 | 30 |
| 13 | US11 - Monitoring | 8 | 30 |
| 14 | Polish | 6 | - |
| **Total** | | **106** | **370** |

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Suggested MVP: US1 through US9 (260 points minimum)
