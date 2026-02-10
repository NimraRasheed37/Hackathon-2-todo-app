# Feature Specification: Phase 5 - Advanced Cloud Deployment

**Feature Branch**: `005-advanced-cloud-deployment`
**Created**: 2026-02-05
**Status**: Draft
**Input**: Phase 5 - Advanced Cloud Deployment with Kafka, Dapr & Advanced Features

## Overview

Phase 5 transforms the local Kubernetes deployment into a production-grade, event-driven distributed system with advanced task management features. This phase introduces:

- **Advanced Task Features**: Recurring tasks, reminders, priorities, tags, and search
- **Event-Driven Architecture**: Kafka for event streaming
- **Dapr Integration**: Distributed runtime for microservices
- **Cloud Kubernetes**: Production deployment on AKS/GKE/DOKS
- **CI/CD Pipeline**: GitHub Actions with automated deployment
- **Monitoring Stack**: Prometheus, Grafana, and Loki

**Total Points**: 300 MVP + 100 Bonus = 400 Maximum

---

## User Scenarios & Testing

### User Story 1 - Recurring Tasks (Priority: P1) - 40 points

Users need to create tasks that automatically recur on a schedule (daily, weekly, monthly, custom).

**Why this priority**: Core feature enabling productivity workflows. Most requested feature for task management applications.

**Independent Test**: Create a daily recurring task, complete it, verify a new instance is created for the next day.

**Acceptance Scenarios**:

1. **Given** a user creates a task with recurrence "daily", **When** the task is completed, **Then** a new task instance is created for the next day with the same properties
2. **Given** a recurring task with pattern "every Monday and Wednesday", **When** completed on Monday, **Then** next instance is scheduled for Wednesday
3. **Given** a recurring task with end date, **When** completed on the last occurrence, **Then** no new instance is created
4. **Given** a user views recurring tasks, **When** listing tasks, **Then** both the pattern and next occurrence are displayed

**Technical Requirements**:

```typescript
// Recurrence Pattern Types
type RecurrenceFrequency = 'daily' | 'weekly' | 'monthly' | 'yearly' | 'custom';

interface RecurrencePattern {
  frequency: RecurrenceFrequency;
  interval: number;           // Every N days/weeks/months
  daysOfWeek?: number[];      // 0-6 for weekly
  dayOfMonth?: number;        // 1-31 for monthly
  endDate?: Date;             // Optional end date
  maxOccurrences?: number;    // Optional occurrence limit
}
```

**Database Schema**:

```sql
-- Add to tasks table or create separate table
ALTER TABLE tasks ADD COLUMN recurrence_pattern JSONB;
ALTER TABLE tasks ADD COLUMN parent_task_id UUID REFERENCES tasks(id);
ALTER TABLE tasks ADD COLUMN occurrence_number INTEGER DEFAULT 1;

-- Recurrence tracking
CREATE TABLE task_recurrences (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  task_id UUID NOT NULL REFERENCES tasks(id),
  pattern JSONB NOT NULL,
  next_occurrence TIMESTAMPTZ,
  last_generated TIMESTAMPTZ,
  total_occurrences INTEGER DEFAULT 0,
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

---

### User Story 2 - Task Reminders (Priority: P1) - 35 points

Users need to receive notifications before task due dates.

**Why this priority**: Critical for task management effectiveness. Enables proactive task completion.

**Independent Test**: Set a reminder for 15 minutes before due date, verify notification is triggered.

**Acceptance Scenarios**:

1. **Given** a task with due date and reminder "15 minutes before", **When** the reminder time arrives, **Then** user receives a notification
2. **Given** multiple reminders on a task (1 hour, 15 minutes), **When** each time arrives, **Then** each reminder fires independently
3. **Given** a completed task with pending reminder, **When** reminder time arrives, **Then** no notification is sent
4. **Given** a user modifies due date, **When** saved, **Then** reminder times are recalculated

**Technical Requirements**:

```typescript
interface TaskReminder {
  id: string;
  taskId: string;
  userId: string;
  reminderType: 'relative' | 'absolute';
  relativeMinutes?: number;  // Minutes before due date
  absoluteTime?: Date;       // Specific time
  channels: ('in_app' | 'email' | 'push')[];
  status: 'pending' | 'sent' | 'cancelled';
}
```

**Database Schema**:

```sql
CREATE TABLE task_reminders (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  task_id UUID NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES users(id),
  reminder_type VARCHAR(20) NOT NULL,
  relative_minutes INTEGER,
  absolute_time TIMESTAMPTZ,
  channels TEXT[] NOT NULL DEFAULT ARRAY['in_app'],
  status VARCHAR(20) DEFAULT 'pending',
  scheduled_at TIMESTAMPTZ NOT NULL,
  sent_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_reminders_scheduled ON task_reminders(scheduled_at) WHERE status = 'pending';
```

---

### User Story 3 - Task Priorities (Priority: P1) - 25 points

Users need to assign priority levels to tasks for better organization.

**Why this priority**: Essential for task triage and focus management.

**Independent Test**: Create tasks with different priorities, verify sorting and visual indicators work correctly.

**Acceptance Scenarios**:

1. **Given** a user creates a task, **When** selecting priority "high", **Then** task is displayed with high priority indicator
2. **Given** tasks with mixed priorities, **When** sorting by priority, **Then** tasks are ordered: critical > high > medium > low > none
3. **Given** a user filters by priority, **When** selecting "high and above", **Then** only critical and high tasks are shown

**Technical Requirements**:

```typescript
type TaskPriority = 'critical' | 'high' | 'medium' | 'low' | 'none';

// Priority values for sorting (higher = more urgent)
const PRIORITY_VALUES: Record<TaskPriority, number> = {
  critical: 4,
  high: 3,
  medium: 2,
  low: 1,
  none: 0
};
```

**Database Schema**:

```sql
ALTER TABLE tasks ADD COLUMN priority VARCHAR(20) DEFAULT 'none';
CREATE INDEX idx_tasks_priority ON tasks(priority);
```

---

### User Story 4 - Task Tags (Priority: P2) - 25 points

Users need to organize tasks with custom tags/labels.

**Why this priority**: Enables flexible categorization beyond fixed categories.

**Independent Test**: Create tags, assign to tasks, filter by tags.

**Acceptance Scenarios**:

1. **Given** a user creates a tag "work", **When** assigning to a task, **Then** task displays the tag
2. **Given** a task with multiple tags, **When** viewing task, **Then** all tags are displayed
3. **Given** a user filters by tag "urgent", **When** applied, **Then** only tasks with that tag are shown
4. **Given** a user deletes a tag, **When** confirmed, **Then** tag is removed from all tasks

**Technical Requirements**:

```typescript
interface Tag {
  id: string;
  userId: string;
  name: string;
  color: string;      // Hex color code
  icon?: string;      // Optional emoji/icon
  usageCount: number; // For sorting by popularity
}
```

**Database Schema**:

```sql
CREATE TABLE tags (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id),
  name VARCHAR(50) NOT NULL,
  color VARCHAR(7) DEFAULT '#808080',
  icon VARCHAR(10),
  usage_count INTEGER DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(user_id, name)
);

CREATE TABLE task_tags (
  task_id UUID REFERENCES tasks(id) ON DELETE CASCADE,
  tag_id UUID REFERENCES tags(id) ON DELETE CASCADE,
  PRIMARY KEY (task_id, tag_id)
);
```

---

### User Story 5 - Advanced Search (Priority: P2) - 25 points

Users need to search tasks with filters and full-text search.

**Why this priority**: Enables quick task discovery as task count grows.

**Independent Test**: Search for task by title, filter by status and priority combined.

**Acceptance Scenarios**:

1. **Given** tasks exist, **When** searching "meeting", **Then** tasks containing "meeting" in title or description are returned
2. **Given** a user applies filters (status: pending, priority: high), **When** combined with search, **Then** results match all criteria
3. **Given** search results, **When** sorting by relevance, **Then** best matches appear first

**Technical Requirements**:

```typescript
interface SearchQuery {
  text?: string;
  status?: TaskStatus[];
  priority?: TaskPriority[];
  tags?: string[];
  dueDateFrom?: Date;
  dueDateTo?: Date;
  hasRecurrence?: boolean;
  sortBy?: 'relevance' | 'dueDate' | 'priority' | 'createdAt';
  sortOrder?: 'asc' | 'desc';
  limit?: number;
  offset?: number;
}
```

**Database Schema**:

```sql
-- Full-text search index
ALTER TABLE tasks ADD COLUMN search_vector tsvector;

CREATE INDEX idx_tasks_search ON tasks USING GIN(search_vector);

-- Trigger to update search vector
CREATE OR REPLACE FUNCTION update_task_search_vector()
RETURNS TRIGGER AS $$
BEGIN
  NEW.search_vector := to_tsvector('english', COALESCE(NEW.title, '') || ' ' || COALESCE(NEW.description, ''));
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER task_search_update
  BEFORE INSERT OR UPDATE ON tasks
  FOR EACH ROW EXECUTE FUNCTION update_task_search_vector();
```

---

### User Story 6 - Event-Driven Architecture with Kafka (Priority: P1) - 50 points

System must use Kafka for event streaming between services.

**Why this priority**: Foundation for scalable, decoupled microservices architecture.

**Independent Test**: Create a task, verify event is published to Kafka and consumed by audit service.

**Acceptance Scenarios**:

1. **Given** a task is created, **When** saved to database, **Then** TaskCreated event is published to Kafka
2. **Given** Kafka consumer is running, **When** event is published, **Then** consumer processes event within 100ms
3. **Given** a consumer fails to process, **When** retries exhausted, **Then** event is sent to DLQ
4. **Given** high load (1000 events/sec), **When** processing, **Then** system maintains ordering within partition

**Technical Requirements**:

```typescript
// Event Schema
interface TaskEvent {
  eventId: string;
  eventType: 'TaskCreated' | 'TaskUpdated' | 'TaskCompleted' | 'TaskDeleted';
  aggregateId: string;  // Task ID
  aggregateType: 'Task';
  timestamp: string;    // ISO 8601
  version: number;
  userId: string;
  correlationId: string;
  payload: Record<string, unknown>;
  metadata: {
    source: string;
    schemaVersion: string;
  };
}
```

**Kafka Topics**:

| Topic | Partitions | Replication | Retention |
|-------|------------|-------------|-----------|
| todo.tasks.events | 3 | 2 | 7 days |
| todo.reminders.scheduled | 3 | 2 | 1 day |
| todo.notifications.outbound | 3 | 2 | 1 day |
| todo.audit.log | 6 | 2 | 30 days |
| todo.dlq | 1 | 2 | 30 days |

---

### User Story 7 - Dapr Integration (Priority: P1) - 50 points

System must use Dapr for service-to-service communication, state management, and pub/sub.

**Why this priority**: Provides portable, cloud-native building blocks for microservices.

**Independent Test**: Make service invocation via Dapr sidecar, verify request is routed correctly.

**Acceptance Scenarios**:

1. **Given** Task Service needs to call User Service, **When** using Dapr service invocation, **Then** request is routed through sidecars
2. **Given** Dapr pub/sub configured, **When** publishing event, **Then** all subscribers receive the event
3. **Given** Dapr state store configured, **When** saving state, **Then** state is persisted to Redis
4. **Given** Dapr secrets configured, **When** requesting secret, **Then** secret is retrieved from configured store

**Dapr Components**:

```yaml
# Pub/Sub Component
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: pubsub
spec:
  type: pubsub.kafka
  version: v1
  metadata:
    - name: brokers
      value: "kafka:9092"
    - name: consumerGroup
      value: "todo-app"
    - name: authType
      value: "none"

# State Store Component
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: statestore
spec:
  type: state.redis
  version: v1
  metadata:
    - name: redisHost
      value: "redis:6379"
    - name: redisPassword
      secretKeyRef:
        name: redis-secret
        key: password
```

---

### User Story 8 - Microservices Architecture (Priority: P1) - 30 points

System must be decomposed into independent microservices.

**Why this priority**: Enables independent scaling, deployment, and development.

**Independent Test**: Deploy each service independently, verify system functions correctly.

**Acceptance Scenarios**:

1. **Given** Task Service is deployed, **When** other services are down, **Then** core CRUD operations still work
2. **Given** services communicate via events, **When** one service is slow, **Then** other services are not blocked
3. **Given** each service has its own database schema, **When** querying, **Then** no cross-service database access occurs

**Service Decomposition**:

| Service | Responsibility | Database | Events Produced | Events Consumed |
|---------|---------------|----------|-----------------|-----------------|
| Task Service | CRUD, search | tasks, tags | TaskCreated, TaskUpdated, TaskCompleted, TaskDeleted | - |
| Recurring Service | Recurrence logic | task_recurrences | RecurrenceTriggered | TaskCompleted |
| Reminder Service | Reminder scheduling | task_reminders | ReminderDue | TaskCreated, TaskUpdated, TaskCompleted |
| Notification Service | Delivery | notifications | NotificationSent | ReminderDue |
| Audit Service | Event logging | audit_log | - | All events |

---

### User Story 9 - Cloud Kubernetes Deployment (Priority: P1) - 30 points

System must be deployable to production cloud Kubernetes (AKS/GKE/DOKS).

**Why this priority**: Production-ready deployment is essential for real-world usage.

**Independent Test**: Deploy to cloud provider, verify all services are healthy and accessible.

**Acceptance Scenarios**:

1. **Given** Kubernetes manifests, **When** applied to AKS/GKE/DOKS, **Then** all pods reach Ready state
2. **Given** Ingress configured with TLS, **When** accessing via HTTPS, **Then** certificate is valid
3. **Given** HPA configured, **When** load increases, **Then** pods scale up automatically
4. **Given** PodDisruptionBudget configured, **When** node drains, **Then** at least 1 replica remains available

**Cloud Requirements**:

- **Supported Providers**: Azure AKS, Google GKE, DigitalOcean DOKS
- **Minimum Cluster**: 3 nodes, 2 vCPU, 4GB RAM each
- **Storage**: Cloud-native persistent volumes
- **Networking**: LoadBalancer service, Ingress with TLS
- **Security**: mTLS between services, secrets management

---

### User Story 10 - CI/CD Pipeline (Priority: P2) - 30 points

System must have automated CI/CD with GitHub Actions.

**Why this priority**: Automation ensures consistent, reliable deployments.

**Independent Test**: Push code change, verify pipeline runs and deploys to staging.

**Acceptance Scenarios**:

1. **Given** code pushed to main, **When** CI runs, **Then** tests pass and images are built
2. **Given** PR created, **When** CI completes, **Then** preview environment is deployed
3. **Given** release tag created, **When** CD runs, **Then** production deployment occurs with approval gate
4. **Given** deployment fails, **When** rollback triggered, **Then** previous version is restored within 5 minutes

**Pipeline Stages**:

```yaml
# .github/workflows/ci-cd.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run tests
        run: |
          cd phase-2/backend && pytest
          cd ../frontend && npm test

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Build and push images
        uses: docker/build-push-action@v5
        with:
          push: true
          tags: ${{ secrets.REGISTRY }}/todo-backend:${{ github.sha }}

  deploy-staging:
    needs: build
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - name: Deploy to staging
        run: kubectl apply -k k8s/overlays/staging

  deploy-production:
    needs: deploy-staging
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: production
    steps:
      - name: Deploy to production
        run: kubectl apply -k k8s/overlays/production
```

---

### User Story 11 - Monitoring & Observability (Priority: P2) - 30 points

System must have comprehensive monitoring with Prometheus, Grafana, and Loki.

**Why this priority**: Production systems require observability for reliability.

**Independent Test**: Generate load, view metrics in Grafana dashboard.

**Acceptance Scenarios**:

1. **Given** application running, **When** Prometheus scrapes, **Then** metrics are collected
2. **Given** Grafana dashboard, **When** viewing, **Then** request rate, latency, errors are displayed
3. **Given** application logs, **When** querying Loki, **Then** logs are searchable and correlated
4. **Given** alert rule triggered, **When** threshold exceeded, **Then** notification is sent

**Metrics to Collect**:

| Metric | Type | Description |
|--------|------|-------------|
| http_requests_total | Counter | Total HTTP requests by method, path, status |
| http_request_duration_seconds | Histogram | Request latency distribution |
| kafka_messages_produced_total | Counter | Kafka messages produced |
| kafka_messages_consumed_total | Counter | Kafka messages consumed |
| kafka_consumer_lag | Gauge | Consumer lag per partition |
| task_operations_total | Counter | Task CRUD operations |
| active_users | Gauge | Currently active users |

---

### Edge Cases

- **Recurring task with past due date**: Create next occurrence based on current time, not past date
- **Reminder for completed task**: Cancel pending reminders when task is completed
- **Tag deletion with assigned tasks**: Remove tag from tasks, don't delete tasks
- **Kafka broker failure**: Use Dapr retry policies, fall back to synchronous processing
- **Cloud provider outage**: Multi-AZ deployment ensures partial availability
- **Concurrent task updates**: Use optimistic locking with version numbers
- **Search with special characters**: Escape and sanitize search input
- **Timezone handling for reminders**: Store in UTC, convert on display

---

## Requirements

### Functional Requirements

- **FR-001**: System MUST support creating recurring tasks with daily, weekly, monthly, yearly, and custom patterns
- **FR-002**: System MUST automatically generate new task instances when recurring tasks are completed
- **FR-003**: System MUST support task reminders with relative (before due date) and absolute time options
- **FR-004**: System MUST deliver reminders via in-app notification (email and push are optional)
- **FR-005**: System MUST support task priorities: critical, high, medium, low, none
- **FR-006**: System MUST support user-defined tags with custom colors
- **FR-007**: System MUST support full-text search across task title and description
- **FR-008**: System MUST publish all task mutations as events to Kafka
- **FR-009**: System MUST use Dapr for service invocation, pub/sub, and state management
- **FR-010**: System MUST deploy to cloud Kubernetes with TLS termination
- **FR-011**: System MUST have CI/CD pipeline with automated testing and deployment
- **FR-012**: System MUST expose Prometheus metrics and support Grafana dashboards

### Non-Functional Requirements

- **NFR-001**: API response time p50 < 100ms, p99 < 500ms
- **NFR-002**: System availability 99.5% (21.9 hours downtime/month max)
- **NFR-003**: Kafka event processing latency < 100ms p95
- **NFR-004**: Support 100 concurrent users minimum
- **NFR-005**: Monthly cloud cost budget: $25-80

### Key Entities

- **Task**: Core entity with title, description, status, priority, due date, recurrence pattern, tags
- **Recurrence**: Pattern definition (frequency, interval, days, end condition)
- **Reminder**: Scheduled notification linked to task and user
- **Tag**: User-defined label with name, color, icon
- **Event**: Immutable record of task state change
- **Notification**: Delivered message to user

---

## Success Criteria

### Measurable Outcomes

- **SC-001**: Users can create and complete recurring tasks with correct next instance generation
- **SC-002**: Reminders are delivered within 1 minute of scheduled time
- **SC-003**: Search returns relevant results within 200ms for 10,000 tasks
- **SC-004**: All task mutations produce corresponding Kafka events
- **SC-005**: Services communicate exclusively via Dapr (no direct HTTP between services)
- **SC-006**: Application deploys to cloud Kubernetes with zero-downtime rolling updates
- **SC-007**: CI/CD pipeline completes in under 10 minutes
- **SC-008**: Grafana dashboard shows real-time metrics with < 30 second delay

### Point Allocation

| Category | Item | Points |
|----------|------|--------|
| **Advanced Features** | Recurring Tasks | 40 |
| | Reminders | 35 |
| | Priorities | 25 |
| | Tags | 25 |
| | Search | 25 |
| **Event Architecture** | Kafka Integration | 50 |
| | Dapr Integration | 50 |
| **Microservices** | Service Decomposition | 30 |
| **Cloud Deployment** | Production K8s | 30 |
| **DevOps** | CI/CD Pipeline | 30 |
| | Monitoring Stack | 30 |
| **Bonus** | Multi-cloud Support | +25 |
| | Canary Deployments | +25 |
| | Chaos Engineering | +25 |
| | Service Mesh (Istio) | +25 |
| **Total** | MVP | 370 |
| | Maximum with Bonus | 470 |

---

## Technical Architecture

### System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              Cloud Kubernetes (AKS/GKE/DOKS)                │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐     │
│  │   Ingress   │   │   Ingress   │   │   Grafana   │   │ Prometheus  │     │
│  │  (Frontend) │   │  (Backend)  │   │             │   │             │     │
│  └──────┬──────┘   └──────┬──────┘   └─────────────┘   └─────────────┘     │
│         │                 │                                                 │
│  ┌──────▼──────┐   ┌──────▼──────┐                                         │
│  │  Frontend   │   │    Task     │◄──────Dapr Sidecar──────┐               │
│  │   (Next.js) │   │   Service   │                         │               │
│  └─────────────┘   └──────┬──────┘                         │               │
│                           │                                │               │
│         ┌─────────────────┼─────────────────┐              │               │
│         │                 │                 │              │               │
│  ┌──────▼──────┐   ┌──────▼──────┐   ┌──────▼──────┐      │               │
│  │  Recurring  │   │  Reminder   │   │Notification │◄─────┤               │
│  │   Service   │   │   Service   │   │   Service   │      │               │
│  └──────┬──────┘   └──────┬──────┘   └─────────────┘      │               │
│         │                 │                               │               │
│         └─────────────────┼───────────────────────────────┘               │
│                           │                                               │
│                    ┌──────▼──────┐                                        │
│                    │    Kafka    │                                        │
│                    │  (Redpanda) │                                        │
│                    └──────┬──────┘                                        │
│                           │                                               │
│  ┌─────────────┐   ┌──────▼──────┐   ┌─────────────┐                     │
│  │  PostgreSQL │   │    Audit    │   │    Redis    │                     │
│  │             │   │   Service   │   │ (Dapr State)│                     │
│  └─────────────┘   └─────────────┘   └─────────────┘                     │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Event Flow

```
Task Created → TaskService → Kafka[todo.tasks.events]
                                    │
                    ┌───────────────┼───────────────┐
                    ▼               ▼               ▼
             RecurringService  ReminderService  AuditService
                    │               │               │
                    ▼               ▼               ▼
            Store recurrence  Schedule reminder  Log event
                pattern            │
                                   ▼
                          Kafka[todo.reminders.scheduled]
                                   │
                                   ▼
                          NotificationService
                                   │
                                   ▼
                          Deliver notification
```

---

## File Structure

```
phase-2/
├── backend/
│   ├── src/
│   │   ├── events/
│   │   │   ├── producers/
│   │   │   │   └── task_event_producer.py
│   │   │   ├── consumers/
│   │   │   │   ├── recurring_consumer.py
│   │   │   │   ├── reminder_consumer.py
│   │   │   │   └── audit_consumer.py
│   │   │   └── schemas/
│   │   │       └── task_events.py
│   │   ├── services/
│   │   │   ├── recurring_service.py
│   │   │   ├── reminder_service.py
│   │   │   ├── notification_service.py
│   │   │   └── search_service.py
│   │   ├── models/
│   │   │   ├── recurrence.py
│   │   │   ├── reminder.py
│   │   │   └── tag.py
│   │   └── api/
│   │       ├── recurring.py
│   │       ├── reminders.py
│   │       ├── tags.py
│   │       └── search.py
│   └── tests/
│       ├── test_recurring.py
│       ├── test_reminders.py
│       └── test_search.py
├── frontend/
│   └── src/
│       ├── components/
│       │   ├── RecurrenceSelector.tsx
│       │   ├── ReminderPicker.tsx
│       │   ├── PrioritySelector.tsx
│       │   ├── TagManager.tsx
│       │   └── SearchBar.tsx
│       └── hooks/
│           └── useSearch.ts
k8s/
├── dapr/
│   ├── components/
│   │   ├── pubsub.yaml
│   │   ├── statestore.yaml
│   │   └── secrets.yaml
│   └── config/
│       └── config.yaml
├── cloud/
│   ├── base/
│   │   ├── namespace.yaml
│   │   ├── secrets.yaml
│   │   └── configmap.yaml
│   ├── overlays/
│   │   ├── staging/
│   │   └── production/
│   └── providers/
│       ├── aks/
│       ├── gke/
│       └── doks/
├── monitoring/
│   ├── prometheus/
│   │   ├── prometheus.yaml
│   │   └── rules/
│   ├── grafana/
│   │   ├── grafana.yaml
│   │   └── dashboards/
│   └── loki/
│       └── loki.yaml
.github/
└── workflows/
    ├── ci.yml
    ├── cd-staging.yml
    └── cd-production.yml
scripts/
├── deploy.sh
├── rollback.sh
└── setup-cloud.sh
```

---

## API Contracts

### Recurring Tasks API

```yaml
POST /api/tasks/{task_id}/recurrence:
  requestBody:
    content:
      application/json:
        schema:
          type: object
          properties:
            frequency:
              type: string
              enum: [daily, weekly, monthly, yearly, custom]
            interval:
              type: integer
              minimum: 1
            daysOfWeek:
              type: array
              items:
                type: integer
                minimum: 0
                maximum: 6
            endDate:
              type: string
              format: date
            maxOccurrences:
              type: integer
  responses:
    201:
      description: Recurrence pattern created
    400:
      description: Invalid recurrence pattern

DELETE /api/tasks/{task_id}/recurrence:
  responses:
    204:
      description: Recurrence removed
```

### Reminders API

```yaml
POST /api/tasks/{task_id}/reminders:
  requestBody:
    content:
      application/json:
        schema:
          type: object
          properties:
            reminderType:
              type: string
              enum: [relative, absolute]
            relativeMinutes:
              type: integer
            absoluteTime:
              type: string
              format: date-time
            channels:
              type: array
              items:
                type: string
                enum: [in_app, email, push]
  responses:
    201:
      description: Reminder created
    400:
      description: Invalid reminder configuration

GET /api/tasks/{task_id}/reminders:
  responses:
    200:
      description: List of reminders for task
```

### Tags API

```yaml
GET /api/tags:
  responses:
    200:
      description: List of user's tags

POST /api/tags:
  requestBody:
    content:
      application/json:
        schema:
          type: object
          required: [name]
          properties:
            name:
              type: string
              maxLength: 50
            color:
              type: string
              pattern: ^#[0-9A-Fa-f]{6}$
            icon:
              type: string
              maxLength: 10
  responses:
    201:
      description: Tag created

POST /api/tasks/{task_id}/tags:
  requestBody:
    content:
      application/json:
        schema:
          type: object
          properties:
            tagIds:
              type: array
              items:
                type: string
                format: uuid
  responses:
    200:
      description: Tags assigned to task
```

### Search API

```yaml
POST /api/tasks/search:
  requestBody:
    content:
      application/json:
        schema:
          type: object
          properties:
            text:
              type: string
            status:
              type: array
              items:
                type: string
            priority:
              type: array
              items:
                type: string
            tags:
              type: array
              items:
                type: string
            dueDateFrom:
              type: string
              format: date
            dueDateTo:
              type: string
              format: date
            sortBy:
              type: string
              enum: [relevance, dueDate, priority, createdAt]
            sortOrder:
              type: string
              enum: [asc, desc]
            limit:
              type: integer
              default: 20
            offset:
              type: integer
              default: 0
  responses:
    200:
      description: Search results
      content:
        application/json:
          schema:
            type: object
            properties:
              results:
                type: array
              total:
                type: integer
              hasMore:
                type: boolean
```
