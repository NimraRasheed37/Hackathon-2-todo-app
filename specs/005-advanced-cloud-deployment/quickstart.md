# Quickstart: Phase 5 - Advanced Cloud Deployment

**Feature**: `005-advanced-cloud-deployment`
**Date**: 2026-02-05

This guide helps developers set up a local development environment for Phase 5 features.

## Prerequisites

- Docker Desktop 4.x
- Kubernetes (minikube, kind, or Docker Desktop K8s)
- kubectl CLI
- Dapr CLI (v1.12+)
- Python 3.11+
- Node.js 18+
- PostgreSQL client (psql)

## 1. Install Dapr CLI

```bash
# macOS/Linux
wget -q https://raw.githubusercontent.com/dapr/cli/master/install/install.sh -O - | /bin/bash

# Windows (PowerShell)
powershell -Command "iwr -useb https://raw.githubusercontent.com/dapr/cli/master/install/install.ps1 | iex"

# Verify installation
dapr --version
```

## 2. Initialize Dapr on Kubernetes

```bash
# Start local Kubernetes (if using minikube)
minikube start --cpus=4 --memory=8192

# Initialize Dapr
dapr init -k

# Verify Dapr is running
dapr status -k
kubectl get pods -n dapr-system
```

## 3. Deploy Infrastructure Components

### Redis (Dapr State Store)

```bash
# Create namespace
kubectl create namespace todo-app

# Deploy Redis
kubectl apply -f - <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis
  namespace: todo-app
spec:
  selector:
    matchLabels:
      app: redis
  template:
    metadata:
      labels:
        app: redis
    spec:
      containers:
      - name: redis
        image: redis:7-alpine
        ports:
        - containerPort: 6379
---
apiVersion: v1
kind: Service
metadata:
  name: redis
  namespace: todo-app
spec:
  selector:
    app: redis
  ports:
  - port: 6379
EOF
```

### Redpanda (Kafka-compatible)

```bash
# Deploy Redpanda
kubectl apply -f - <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redpanda
  namespace: todo-app
spec:
  selector:
    matchLabels:
      app: redpanda
  template:
    metadata:
      labels:
        app: redpanda
    spec:
      containers:
      - name: redpanda
        image: vectorized/redpanda:v23.3.5
        args:
        - redpanda
        - start
        - --smp 1
        - --memory 512M
        - --overprovisioned
        - --kafka-addr PLAINTEXT://0.0.0.0:9092
        ports:
        - containerPort: 9092
---
apiVersion: v1
kind: Service
metadata:
  name: kafka
  namespace: todo-app
spec:
  selector:
    app: redpanda
  ports:
  - port: 9092
EOF
```

## 4. Configure Dapr Components

```bash
# Create Dapr components
kubectl apply -f - <<EOF
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: pubsub
  namespace: todo-app
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
---
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: statestore
  namespace: todo-app
spec:
  type: state.redis
  version: v1
  metadata:
  - name: redisHost
    value: "redis:6379"
EOF
```

## 5. Set Up Local Database

```bash
# Option 1: Use existing Neon PostgreSQL
export DATABASE_URL="postgresql://user:pass@host/db?sslmode=require"

# Option 2: Run PostgreSQL locally
docker run -d \
  --name postgres \
  -e POSTGRES_USER=todo \
  -e POSTGRES_PASSWORD=todo \
  -e POSTGRES_DB=todo \
  -p 5432:5432 \
  postgres:15

export DATABASE_URL="postgresql://todo:todo@localhost:5432/todo"
```

## 6. Run Database Migrations

```bash
cd phase-2/backend

# Install dependencies
pip install -r requirements.txt

# Run migrations
alembic upgrade head
```

## 7. Start Backend with Dapr Sidecar

```bash
# Option 1: Using dapr run (development)
cd phase-2/backend
dapr run --app-id task-service \
         --app-port 8000 \
         --dapr-http-port 3500 \
         --resources-path ./dapr/components \
         -- uvicorn src.main:app --host 0.0.0.0 --port 8000

# Option 2: Without Dapr (for debugging)
cd phase-2/backend
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

## 8. Start Frontend

```bash
cd phase-2/frontend
npm install
npm run dev
```

## 9. Verify Setup

```bash
# Check Dapr sidecar
curl http://localhost:3500/v1.0/healthz

# Check backend health
curl http://localhost:8000/health

# Check frontend
open http://localhost:3000

# Publish test event via Dapr
curl -X POST http://localhost:3500/v1.0/publish/pubsub/todo.tasks.events \
  -H "Content-Type: application/json" \
  -d '{"eventType": "test", "data": {"message": "hello"}}'
```

## 10. Local Development Workflow

### Running Tests

```bash
# Backend tests
cd phase-2/backend
pytest tests/ -v

# Frontend tests
cd phase-2/frontend
npm test
```

### Viewing Logs

```bash
# Dapr sidecar logs
dapr logs --app-id task-service

# Kafka messages (using Redpanda Console)
kubectl port-forward svc/redpanda 8080:8080 -n todo-app
open http://localhost:8080
```

### Debugging Events

```bash
# Consume messages from topic
kubectl exec -it deploy/redpanda -n todo-app -- \
  rpk topic consume todo.tasks.events --brokers localhost:9092
```

## Environment Variables

Create `.env` file in `phase-2/backend/`:

```bash
DATABASE_URL=postgresql://todo:todo@localhost:5432/todo
DAPR_HTTP_PORT=3500
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
REDIS_HOST=localhost
REDIS_PORT=6379
JWT_SECRET=your-secret-key
LOG_LEVEL=DEBUG
```

## Common Issues

### Dapr sidecar not connecting

```bash
# Check Dapr status
dapr status -k
# Restart Dapr
dapr uninstall -k && dapr init -k
```

### Kafka connection refused

```bash
# Check Redpanda is running
kubectl get pods -n todo-app
kubectl logs deploy/redpanda -n todo-app
```

### Database migration errors

```bash
# Check database connection
psql $DATABASE_URL -c "SELECT 1"
# Reset migrations (CAUTION: destroys data)
alembic downgrade base && alembic upgrade head
```

## Next Steps

1. Implement recurring tasks (US1)
2. Implement reminders (US2)
3. Add priorities and tags (US3, US4)
4. Implement search (US5)
5. Configure monitoring (US11)
6. Set up CI/CD (US10)
7. Deploy to cloud (US9)
