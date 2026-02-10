# Implementation Plan: Phase 5 - Advanced Cloud Deployment

**Branch**: `005-advanced-cloud-deployment` | **Date**: 2026-02-05 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/005-advanced-cloud-deployment/spec.md`

## Summary

Phase 5 transforms the local Kubernetes deployment into a production-grade, event-driven distributed system. The implementation introduces:
1. Advanced task features (recurring tasks, reminders, priorities, tags, search)
2. Event-driven architecture with Kafka for inter-service communication
3. Dapr as the distributed runtime abstraction layer
4. Cloud Kubernetes deployment (AKS/GKE/DOKS)
5. CI/CD automation with GitHub Actions
6. Comprehensive monitoring with Prometheus, Grafana, and Loki

## Technical Context

**Language/Version**: Python 3.11 (Backend), TypeScript 5.x (Frontend)
**Primary Dependencies**: FastAPI, SQLAlchemy, aiokafka, dapr-client, Next.js 14, React 18
**Storage**: Neon PostgreSQL (primary), Redis (Dapr state store)
**Testing**: pytest (backend), Jest/Vitest (frontend)
**Target Platform**: Cloud Kubernetes (Azure AKS / GCP GKE / DigitalOcean DOKS)
**Project Type**: Web application (backend + frontend)
**Performance Goals**: p50 < 100ms, p99 < 500ms, 99.5% availability
**Constraints**: $25-80/month cloud budget, 100 concurrent users minimum
**Scale/Scope**: 5 microservices, 11 user stories, 370+ points

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Article | Requirement | Status | Notes |
|---------|-------------|--------|-------|
| I - Event-Driven | All mutations as events to Kafka | ✅ PASS | Spec defines 5 Kafka topics |
| II - Dapr Runtime | Service communication via Dapr | ✅ PASS | Dapr components specified |
| III - Advanced Features | Recurring, reminders, priorities, tags | ✅ PASS | US1-5 cover all features |
| IV - Cloud Production | TLS, secrets, HA, HPA | ✅ PASS | Cloud requirements defined |
| V - CI/CD Pipeline | GitHub Actions, rolling updates | ✅ PASS | Pipeline stages specified |
| VI - Cost Optimization | $25-80/month budget | ✅ PASS | NFR-005 enforces budget |
| VII - Kafka Topics | Naming, partitions, DLQ | ✅ PASS | Topic config in spec |
| VIII - Data Migration | Zero-downtime migrations | ✅ PASS | Schema changes documented |
| IX - Service Architecture | Microservices decomposition | ✅ PASS | 5 services defined |
| X - Performance Targets | SLOs defined | ✅ PASS | NFR-001 through NFR-004 |

**Gate Result**: ✅ ALL PASS - Proceed to Phase 0

## Project Structure

### Documentation (this feature)

```text
specs/005-advanced-cloud-deployment/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (OpenAPI specs)
│   ├── recurring-api.yaml
│   ├── reminders-api.yaml
│   ├── tags-api.yaml
│   └── search-api.yaml
└── tasks.md             # Phase 2 output (from /sp.tasks)
```

### Source Code (repository root)

```text
phase-2/
├── backend/
│   ├── src/
│   │   ├── main.py                    # FastAPI app entry
│   │   ├── models/                    # SQLAlchemy models
│   │   │   ├── task.py               # UPDATE: add new fields
│   │   │   ├── recurrence.py         # NEW
│   │   │   ├── reminder.py           # NEW
│   │   │   └── tag.py                # NEW
│   │   ├── api/                       # API endpoints
│   │   │   ├── recurring.py          # NEW
│   │   │   ├── reminders.py          # NEW
│   │   │   ├── tags.py               # NEW
│   │   │   └── search.py             # NEW
│   │   ├── services/                  # Business logic
│   │   │   ├── recurring_service.py  # NEW
│   │   │   ├── reminder_service.py   # NEW
│   │   │   ├── notification_service.py # NEW
│   │   │   └── search_service.py     # NEW
│   │   └── events/                    # Kafka integration
│   │       ├── producer.py           # NEW
│   │       ├── consumer.py           # NEW
│   │       └── schemas.py            # NEW
│   ├── tests/
│   │   ├── test_recurring.py         # NEW
│   │   ├── test_reminders.py         # NEW
│   │   ├── test_tags.py              # NEW
│   │   └── test_search.py            # NEW
│   ├── alembic/
│   │   └── versions/                  # Database migrations
│   └── Dockerfile                     # UPDATE: add Dapr support

├── frontend/
│   └── src/
│       ├── components/
│       │   ├── RecurrenceSelector.tsx # NEW
│       │   ├── ReminderPicker.tsx     # NEW
│       │   ├── PrioritySelector.tsx   # NEW
│       │   ├── TagManager.tsx         # NEW
│       │   └── SearchBar.tsx          # NEW
│       ├── hooks/
│       │   └── useSearch.ts           # NEW
│       └── types/
│           └── task.ts                # UPDATE: add new fields

k8s/
├── dapr/
│   ├── components/
│   │   ├── pubsub-kafka.yaml          # NEW
│   │   ├── statestore-redis.yaml      # NEW
│   │   ├── secrets.yaml               # NEW
│   │   └── bindings-cron.yaml         # NEW
│   └── config/
│       └── config.yaml                # NEW
├── cloud/
│   ├── base/
│   │   ├── namespace.yaml             # NEW
│   │   ├── secrets.yaml               # NEW
│   │   └── configmap.yaml             # NEW
│   ├── overlays/
│   │   ├── staging/
│   │   │   └── kustomization.yaml    # NEW
│   │   └── production/
│   │       └── kustomization.yaml    # NEW
│   └── providers/
│       ├── aks/                       # NEW
│       ├── gke/                       # NEW
│       └── doks/                      # NEW
├── monitoring/
│   ├── prometheus/
│   │   ├── prometheus.yaml            # NEW
│   │   └── rules/
│   │       └── alerts.yaml           # NEW
│   ├── grafana/
│   │   ├── grafana.yaml               # NEW
│   │   └── dashboards/
│   │       └── todo-app.json         # NEW
│   └── loki/
│       └── loki.yaml                  # NEW

.github/
└── workflows/
    ├── ci.yml                         # NEW
    ├── cd-staging.yml                 # NEW
    └── cd-production.yml              # NEW

scripts/
├── deploy.sh                          # NEW
├── rollback.sh                        # NEW
└── setup-cloud.sh                     # NEW
```

**Structure Decision**: Web application with microservices architecture. Backend services communicate via Kafka events abstracted through Dapr. Frontend remains a monolith calling the Task Service API.

## Complexity Tracking

No constitution violations requiring justification.
