# Research: Phase 5 - Advanced Cloud Deployment

**Feature**: `005-advanced-cloud-deployment`
**Date**: 2026-02-05
**Status**: Complete

## Research Questions

### RQ-001: Kafka Provider Selection

**Question**: Which Kafka provider best fits the $25-80/month budget and production requirements?

**Decision**: Redpanda Cloud (Serverless tier) or Strimzi (self-hosted on K8s)

**Rationale**:
- Redpanda Cloud Serverless: $0 for up to 1GB/day throughput, Kafka-compatible API, zero ops overhead
- Strimzi: Self-hosted Kafka operator for Kubernetes, no additional cost but requires cluster resources
- Confluent Cloud: Minimum $1/hour, exceeds budget at ~$720/month

**Alternatives Considered**:
| Provider | Monthly Cost | Pros | Cons |
|----------|-------------|------|------|
| Redpanda Cloud Serverless | $0-25 | Zero ops, Kafka-compatible, fast | Limited to 1GB/day free |
| Strimzi (self-hosted) | $0 (K8s resources) | Full control, no vendor lock | Ops overhead, uses cluster RAM |
| Amazon MSK Serverless | $50+ | AWS managed | Exceeds budget |
| Confluent Cloud | $720+ | Feature-rich | Far exceeds budget |

**Recommendation**: Start with Redpanda Cloud Serverless for development/staging. Evaluate Strimzi for production if traffic exceeds free tier.

---

### RQ-002: Cloud Kubernetes Provider Selection

**Question**: Which cloud Kubernetes provider offers the best cost-performance for the budget?

**Decision**: DigitalOcean Kubernetes (DOKS) as primary, with manifests for AKS and GKE

**Rationale**:
- DOKS: $36/month for 3-node cluster (2 vCPU, 4GB each), simple pricing, good docs
- AKS: Free control plane, pay only for VMs (~$40-60/month for similar specs)
- GKE: Free control plane (Autopilot), pay for nodes (~$50-70/month)

**Alternatives Considered**:
| Provider | 3-Node Cost | Control Plane | Notes |
|----------|-------------|---------------|-------|
| DigitalOcean DOKS | $36/month | Free | Simplest, predictable |
| Azure AKS | $40-60/month | Free | Good for enterprise |
| Google GKE | $50-70/month | Free (Autopilot) | Best autoscaling |
| AWS EKS | $72/month + nodes | $72/month | Most expensive |

**Recommendation**: Use DOKS for primary deployment. Provide Kustomize overlays for AKS/GKE to support multi-cloud.

---

### RQ-003: Dapr Integration Patterns

**Question**: How should Dapr be integrated with the existing FastAPI backend?

**Decision**: Dapr sidecar pattern with HTTP API calls from FastAPI

**Rationale**:
- Dapr sidecar runs alongside each service pod
- FastAPI makes HTTP calls to localhost:3500 (Dapr HTTP port)
- No SDK dependency required (HTTP API is language-agnostic)
- Dapr handles Kafka, Redis, secrets transparently

**Integration Pattern**:
```python
# Publish event via Dapr
import httpx

async def publish_event(topic: str, data: dict):
    async with httpx.AsyncClient() as client:
        await client.post(
            f"http://localhost:3500/v1.0/publish/pubsub/{topic}",
            json=data
        )
```

**Alternatives Considered**:
| Approach | Pros | Cons |
|----------|------|------|
| Dapr HTTP API | No SDK, portable | Slightly more verbose |
| Dapr Python SDK | Type hints, async | SDK dependency |
| Direct Kafka (aiokafka) | Full control | Vendor lock-in, more code |

**Recommendation**: Use Dapr HTTP API for pub/sub and state. Direct HTTP keeps code portable and testable.

---

### RQ-004: Recurring Task Implementation

**Question**: How should recurring task generation be implemented?

**Decision**: Event-driven with Dapr cron binding

**Rationale**:
- Dapr cron binding triggers Recurring Service every minute
- Service checks for tasks with `recurrence_pattern` where `next_occurrence <= now()`
- On match, publishes `RecurrenceTriggered` event
- Task Service consumes event and creates new task instance

**Pattern**:
```
Dapr Cron (every minute)
    → Recurring Service (check due recurrences)
    → Kafka: RecurrenceTriggered event
    → Task Service (create new task instance)
    → Kafka: TaskCreated event
```

**Alternatives Considered**:
| Approach | Pros | Cons |
|----------|------|------|
| Dapr Cron + Events | Decoupled, scalable | Slight complexity |
| APScheduler in-process | Simple | Doesn't scale, single point of failure |
| Celery Beat | Proven | Heavy dependency, Redis required anyway |
| PostgreSQL pg_cron | DB-native | Tight coupling to DB |

**Recommendation**: Dapr cron binding for scheduling, events for task creation. Clean separation of concerns.

---

### RQ-005: Reminder Notification Delivery

**Question**: How should reminders be delivered to users?

**Decision**: In-app notifications as MVP, with event-driven architecture for future email/push

**Rationale**:
- Phase 5 scope specifies in-app notifications as required (FR-004)
- Email and push are optional (can be added later without code changes)
- Notification Service consumes `ReminderDue` events and writes to `notifications` table
- Frontend polls or uses WebSocket for real-time notifications

**Architecture**:
```
Dapr Cron (every minute)
    → Reminder Service (check scheduled_at <= now())
    → Kafka: ReminderDue event
    → Notification Service
        → Insert into notifications table
        → (Future: Send email, push)
    → Frontend fetches notifications via API
```

**Alternatives Considered**:
| Approach | Pros | Cons |
|----------|------|------|
| Polling + DB | Simple, works offline | Not real-time |
| WebSocket | Real-time | Complexity, connection management |
| Server-Sent Events | Simpler than WS | Less browser support |
| Firebase Cloud Messaging | Push notifications | External dependency |

**Recommendation**: Start with polling (GET /notifications every 30s). Add WebSocket in polish phase if needed.

---

### RQ-006: Full-Text Search Implementation

**Question**: How should full-text search be implemented for tasks?

**Decision**: PostgreSQL native full-text search with tsvector

**Rationale**:
- PostgreSQL tsvector provides good full-text search for our scale (10k tasks)
- No additional infrastructure (Elasticsearch would exceed budget)
- GIN index ensures fast queries (<100ms requirement)
- Already using Neon PostgreSQL

**Implementation**:
```sql
ALTER TABLE tasks ADD COLUMN search_vector tsvector;
CREATE INDEX idx_tasks_search ON tasks USING GIN(search_vector);

-- Update trigger
CREATE OR REPLACE FUNCTION update_search_vector()
RETURNS TRIGGER AS $$
BEGIN
  NEW.search_vector := to_tsvector('english',
    COALESCE(NEW.title, '') || ' ' || COALESCE(NEW.description, ''));
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER task_search_trigger
  BEFORE INSERT OR UPDATE ON tasks
  FOR EACH ROW EXECUTE FUNCTION update_search_vector();
```

**Alternatives Considered**:
| Approach | Pros | Cons |
|----------|------|------|
| PostgreSQL tsvector | Built-in, free | Limited features |
| Elasticsearch | Powerful | $100+/month, complex |
| Meilisearch | Fast, easy | Another service to manage |
| LIKE queries | Simplest | Slow, no relevance ranking |

**Recommendation**: PostgreSQL full-text search meets requirements without additional cost.

---

### RQ-007: CI/CD Pipeline Design

**Question**: What CI/CD pipeline structure best supports the deployment requirements?

**Decision**: GitHub Actions with environment-based deployment gates

**Rationale**:
- GitHub Actions is free for public repos, generous minutes for private
- Environment protection rules provide approval gates
- Native Kubernetes integration via kubectl
- Matrix builds for multi-architecture images

**Pipeline Structure**:
```yaml
Workflows:
  ci.yml:
    - Trigger: push, pull_request
    - Jobs: lint, test, build-image, security-scan

  cd-staging.yml:
    - Trigger: push to main
    - Jobs: deploy-staging, smoke-test

  cd-production.yml:
    - Trigger: workflow_dispatch (manual)
    - Jobs: deploy-production (requires approval)
```

**Alternatives Considered**:
| Approach | Pros | Cons |
|----------|------|------|
| GitHub Actions | Free, integrated | Learning curve |
| GitLab CI | Full DevOps platform | Migration effort |
| ArgoCD | GitOps native | Additional operator |
| Jenkins | Flexible | Self-hosted overhead |

**Recommendation**: GitHub Actions with reusable workflows for DRY deployment logic.

---

### RQ-008: Monitoring Stack Selection

**Question**: Which monitoring stack fits the budget and requirements?

**Decision**: Prometheus + Grafana + Loki (self-hosted on K8s)

**Rationale**:
- All three are open-source and can run on the same K8s cluster
- Prometheus scrapes metrics from all pods
- Grafana provides dashboards
- Loki provides log aggregation
- Total additional resource cost: ~$10/month (1 small node for monitoring)

**Stack Configuration**:
```yaml
Prometheus:
  - Scrape interval: 15s
  - Retention: 15 days
  - Resource: 500Mi RAM, 200m CPU

Grafana:
  - Dashboards: service health, Kafka metrics, request latency
  - Resource: 256Mi RAM, 100m CPU

Loki:
  - Retention: 7 days
  - Resource: 512Mi RAM, 200m CPU
```

**Alternatives Considered**:
| Approach | Pros | Cons |
|----------|------|------|
| Self-hosted PLG | Free, full control | Ops overhead |
| Datadog | Easy, powerful | $15/host/month = $45+ |
| New Relic | Good free tier | Limited features |
| Cloud provider native | Integrated | Vendor lock-in |

**Recommendation**: Self-hosted PLG stack. Consider Grafana Cloud free tier (10k metrics) as alternative.

---

## Technology Decisions Summary

| Decision | Choice | Cost Impact |
|----------|--------|-------------|
| Kafka Provider | Redpanda Cloud Serverless | $0-25/month |
| Cloud Kubernetes | DigitalOcean DOKS | $36/month |
| Distributed Runtime | Dapr (HTTP API) | $0 |
| Recurring Tasks | Dapr Cron + Events | $0 |
| Notifications | In-app (polling) | $0 |
| Search | PostgreSQL tsvector | $0 |
| CI/CD | GitHub Actions | $0 |
| Monitoring | Prometheus + Grafana + Loki | ~$10/month |
| **Total** | | **$46-71/month** |

**Budget Compliance**: ✅ Within $25-80/month target

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Redpanda free tier exceeded | Medium | Service disruption | Monitor usage, have Strimzi fallback ready |
| Dapr learning curve | Low | Delayed delivery | Use HTTP API (simpler), good docs available |
| Cloud cost overrun | Low | Budget exceeded | Set billing alerts at $50, auto-scaling limits |
| Kafka message loss | Low | Data inconsistency | Dapr retry policies, DLQ pattern |

---

## Next Steps

1. **Phase 1**: Create data-model.md with entity definitions
2. **Phase 1**: Create API contracts in contracts/ directory
3. **Phase 1**: Create quickstart.md for local development
4. **Phase 2**: Generate tasks.md with /sp.tasks
