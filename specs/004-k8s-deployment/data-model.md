# Data Model: Phase 4 Kubernetes Resources

**Feature**: 004-k8s-deployment
**Date**: 2026-02-03

## Overview

Phase 4 introduces Kubernetes resources as the "data model" for infrastructure. These resources define the desired state of the application deployment.

## Kubernetes Resource Hierarchy

```
Cluster
└── default (namespace)
    ├── ConfigMap: todo-config
    ├── Secret: todo-secrets
    ├── Deployment: todo-frontend
    │   └── ReplicaSet
    │       ├── Pod: todo-frontend-xxxxx
    │       └── Pod: todo-frontend-yyyyy
    ├── Deployment: todo-backend
    │   └── ReplicaSet
    │       ├── Pod: todo-backend-xxxxx
    │       └── Pod: todo-backend-yyyyy
    ├── Service: todo-frontend (ClusterIP)
    ├── Service: todo-backend (ClusterIP)
    └── Ingress: todo-ingress
```

## Resource Specifications

### ConfigMap: todo-config

**Purpose**: Store non-sensitive configuration values

| Key | Value | Used By |
|-----|-------|---------|
| API_URL | http://todo-backend:8000 | Frontend |
| FRONTEND_URL | http://todo.local | Backend (CORS) |
| CORS_ORIGINS | http://todo.local | Backend |
| ENVIRONMENT | local | Both |
| LOG_LEVEL | info | Backend |

### Secret: todo-secrets

**Purpose**: Store sensitive configuration values (base64 encoded)

| Key | Description | Used By |
|-----|-------------|---------|
| DATABASE_URL | Neon PostgreSQL connection string | Backend |
| OPENAI_API_KEY | OpenAI API key for AI chatbot | Backend |
| JWT_SECRET | JWT signing secret | Backend |
| BETTER_AUTH_SECRET | Better Auth secret | Frontend |

### Deployment: todo-frontend

**Purpose**: Manage frontend pod replicas

| Field | Value | Rationale |
|-------|-------|-----------|
| replicas | 2 | High availability (Article III) |
| image | todo-frontend:latest | Local image |
| port | 3000 | Next.js default |
| resources.requests.memory | 128Mi | Conservative for local |
| resources.requests.cpu | 100m | Conservative for local |
| resources.limits.memory | 256Mi | Prevent runaway |
| resources.limits.cpu | 200m | Prevent runaway |
| livenessProbe.path | /api/health | App alive check |
| readinessProbe.path | /api/health | App ready check |

### Deployment: todo-backend

**Purpose**: Manage backend pod replicas

| Field | Value | Rationale |
|-------|-------|-----------|
| replicas | 2 | High availability (Article III) |
| image | todo-backend:latest | Local image |
| port | 8000 | FastAPI/Uvicorn default |
| resources.requests.memory | 256Mi | AI operations need more |
| resources.requests.cpu | 200m | AI operations need more |
| resources.limits.memory | 512Mi | AI peak usage |
| resources.limits.cpu | 400m | AI peak usage |
| livenessProbe.path | /health | App alive check |
| readinessProbe.path | /ready | DB connection check |

### Service: todo-frontend

**Purpose**: Internal load balancer for frontend pods

| Field | Value | Rationale |
|-------|-------|-----------|
| type | ClusterIP | Internal only (Article III) |
| port | 3000 | Match container port |
| targetPort | 3000 | Forward to container |
| selector | app: todo-frontend | Select frontend pods |

### Service: todo-backend

**Purpose**: Internal load balancer for backend pods

| Field | Value | Rationale |
|-------|-------|-----------|
| type | ClusterIP | Internal only (Article III) |
| port | 8000 | Match container port |
| targetPort | 8000 | Forward to container |
| selector | app: todo-backend | Select backend pods |

### Ingress: todo-ingress

**Purpose**: External traffic routing

| Field | Value | Rationale |
|-------|-------|-----------|
| ingressClassName | nginx | Minikube addon |
| host | todo.local | Local development |
| path: / | → todo-frontend:3000 | Frontend routes |
| path: /api | → todo-backend:8000 | API routes |

## Label Conventions

All resources use consistent labels per Helm best practices:

```yaml
labels:
  app.kubernetes.io/name: todo-app
  app.kubernetes.io/instance: {{ .Release.Name }}
  app.kubernetes.io/version: {{ .Chart.AppVersion }}
  app.kubernetes.io/component: frontend|backend
  app.kubernetes.io/managed-by: Helm
```

## Resource Relationships

```
┌─────────────┐     ┌─────────────┐
│   Ingress   │────▶│  Services   │
│ todo.local  │     │ frontend/   │
│             │     │ backend     │
└─────────────┘     └──────┬──────┘
                           │
                           ▼
                   ┌───────────────┐
                   │  Deployments  │
                   │ frontend/     │
                   │ backend       │
                   └───────┬───────┘
                           │
                           ▼
                   ┌───────────────┐
                   │     Pods      │
                   │ 2x frontend   │
                   │ 2x backend    │
                   └───────┬───────┘
                           │
                           ▼
              ┌────────────┴────────────┐
              │                         │
              ▼                         ▼
       ┌────────────┐           ┌─────────────┐
       │  ConfigMap │           │   Secret    │
       │ todo-config│           │ todo-secrets│
       └────────────┘           └─────────────┘
```

## Environment Variable Mapping

### Frontend Container

| Env Var | Source | Key |
|---------|--------|-----|
| NEXT_PUBLIC_API_URL | ConfigMap | API_URL |
| BETTER_AUTH_SECRET | Secret | BETTER_AUTH_SECRET |
| BETTER_AUTH_URL | ConfigMap | FRONTEND_URL |
| DATABASE_URL | Secret | DATABASE_URL |

### Backend Container

| Env Var | Source | Key |
|---------|--------|-----|
| DATABASE_URL | Secret | DATABASE_URL |
| OPENAI_API_KEY | Secret | OPENAI_API_KEY |
| JWT_SECRET | Secret | JWT_SECRET |
| CORS_ORIGINS | ConfigMap | CORS_ORIGINS |
| LOG_LEVEL | ConfigMap | LOG_LEVEL |
