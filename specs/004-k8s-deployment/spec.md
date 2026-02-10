# Feature Specification: Phase 4 Local Kubernetes Deployment

**Feature Branch**: `004-k8s-deployment`
**Created**: 2026-02-03
**Status**: Draft
**Phase**: Phase 4 - Local Kubernetes Deployment
**Builds Upon**: Phase 3 (AI-Powered Todo Chatbot)
**Input**: User description: "Phase 4 Local Kubernetes Deployment with Minikube & Helm"

## Overview

Phase 4 containerizes and deploys the complete Phase 3 application (Next.js frontend + FastAPI backend with AI chatbot) on a local Kubernetes cluster using Minikube, Helm charts, and AIOps tools.

**Scope**:
- Docker containers for frontend and backend
- Kubernetes deployments on Minikube (local cluster)
- Helm charts for package management
- ConfigMaps and Secrets for configuration
- Ingress for traffic routing
- AIOps workflow using Gordon, kubectl-ai, and kagent
- All Phase 3 features working in Kubernetes

**Out of Scope** (Phase 5):
- Cloud deployment (AWS/GCP/Azure)
- Kafka event streaming
- Dapr integration
- CI/CD pipelines
- Production monitoring

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Docker Containerization (Priority: P1)

As a developer, I want to containerize the frontend and backend applications so that they can be deployed consistently across environments.

**Why this priority**: Containers are the foundation for all Kubernetes deployment. Without proper Docker images, no subsequent work is possible.

**Independent Test**: Can be fully tested by building Docker images and running containers locally with `docker run`, verifying both applications start and respond to health checks.

**Acceptance Scenarios**:

1. **Given** the frontend source code exists, **When** I run `docker build -t todo-frontend:latest ./frontend`, **Then** the image builds successfully with size < 200MB
2. **Given** the backend source code exists, **When** I run `docker build -t todo-backend:latest ./backend`, **Then** the image builds successfully with size < 150MB
3. **Given** both images are built, **When** I run `docker run -p 3000:3000 todo-frontend:latest`, **Then** the frontend starts and responds on port 3000
4. **Given** both images are built, **When** I run `docker run -p 8000:8000 todo-backend:latest`, **Then** the backend starts and responds on port 8000
5. **Given** containers are running, **When** I check container user, **Then** both containers run as non-root users

---

### User Story 2 - Minikube Cluster Setup (Priority: P2)

As a developer, I want to set up a local Kubernetes cluster with Minikube so that I can test Kubernetes deployments locally.

**Why this priority**: The Kubernetes cluster is required before any manifests can be applied. This story enables all subsequent Kubernetes work.

**Independent Test**: Can be fully tested by starting Minikube, enabling required addons, and verifying cluster health with `kubectl cluster-info`.

**Acceptance Scenarios**:

1. **Given** Minikube is installed, **When** I run `minikube start`, **Then** a local Kubernetes cluster starts successfully
2. **Given** Minikube is running, **When** I run `minikube addons enable ingress`, **Then** the NGINX Ingress controller is installed
3. **Given** Minikube is running, **When** I run `kubectl cluster-info`, **Then** I see cluster endpoints for Kubernetes control plane
4. **Given** Docker images exist locally, **When** I run `minikube image load todo-frontend:latest todo-backend:latest`, **Then** images are available in Minikube's container runtime

---

### User Story 3 - Kubernetes Manifests (Priority: P3)

As a developer, I want to create Kubernetes manifests for all resources so that the application can be deployed declaratively.

**Why this priority**: Raw manifests provide the foundation for understanding Kubernetes concepts before abstracting to Helm charts.

**Independent Test**: Can be fully tested by applying manifests with `kubectl apply -f k8s/manifests/` and verifying all pods reach Running state.

**Acceptance Scenarios**:

1. **Given** manifests exist in `k8s/manifests/`, **When** I run `kubectl apply -f k8s/manifests/`, **Then** all resources are created without errors
2. **Given** deployments are applied, **When** I run `kubectl get pods`, **Then** frontend and backend pods show Running status
3. **Given** services are applied, **When** I run `kubectl get services`, **Then** todo-frontend and todo-backend services exist with correct ports
4. **Given** ConfigMap is applied, **When** I run `kubectl describe configmap todo-config`, **Then** all non-sensitive configuration values are present
5. **Given** Secrets are applied, **When** I run `kubectl get secret todo-secrets`, **Then** the secret exists with encoded sensitive values

---

### User Story 4 - Helm Chart Creation (Priority: P4)

As a developer, I want to package the application as a Helm chart so that deployment is repeatable, configurable, and follows best practices.

**Why this priority**: Helm charts provide templating and versioning, making deployments professional and manageable.

**Independent Test**: Can be fully tested by running `helm lint` and `helm install` to deploy the application via Helm.

**Acceptance Scenarios**:

1. **Given** Helm chart exists in `k8s/helm/todo-app/`, **When** I run `helm lint k8s/helm/todo-app`, **Then** no errors or warnings are reported
2. **Given** Helm chart is valid, **When** I run `helm install todo k8s/helm/todo-app`, **Then** the release is deployed successfully
3. **Given** Helm release is installed, **When** I run `helm list`, **Then** the `todo` release shows status "deployed"
4. **Given** values need customization, **When** I run `helm upgrade todo k8s/helm/todo-app --set frontend.replicas=3`, **Then** the frontend scales to 3 replicas
5. **Given** templates use helpers, **When** I examine resource names, **Then** all resources follow consistent naming conventions

---

### User Story 5 - Deployment & Testing (Priority: P5)

As a developer, I want to deploy the application and verify all Phase 3 features work in Kubernetes so that I confirm successful containerization.

**Why this priority**: Validates that the entire application stack functions correctly in the Kubernetes environment.

**Independent Test**: Can be fully tested by accessing http://todo.local and performing CRUD operations plus AI chatbot interactions.

**Acceptance Scenarios**:

1. **Given** Ingress is configured, **When** I access `http://todo.local`, **Then** the frontend loads successfully
2. **Given** the application is running, **When** I create a new todo via the UI, **Then** the todo appears in my list
3. **Given** todos exist, **When** I use the AI chatbot to ask "What are my pending todos?", **Then** the chatbot responds with accurate information
4. **Given** pods are running, **When** I run `kubectl logs -f <frontend-pod>`, **Then** I see application logs streaming
5. **Given** health probes are configured, **When** I run `kubectl describe pod <pod>`, **Then** liveness and readiness probes show passing status

---

### User Story 6 - AIOps & Optimization (Priority: P6)

As a developer, I want to use AIOps tools to analyze and optimize my deployment so that I learn modern operational practices.

**Why this priority**: AIOps tools enhance learning and provide operational insights, but are not required for basic functionality.

**Independent Test**: Can be fully tested by running AIOps commands and documenting the insights received.

**Acceptance Scenarios**:

1. **Given** Gordon is available, **When** I ask "How can I optimize my Dockerfile?", **Then** I receive actionable suggestions
2. **Given** kubectl-ai is installed, **When** I ask "Show me pods that are not ready", **Then** I get a valid kubectl command
3. **Given** kagent is available, **When** I ask "Analyze my cluster health", **Then** I receive a cluster health report
4. **Given** AIOps tools are used, **When** I complete deployment, **Then** I have documented my AI interactions

---

### Edge Cases

- What happens when Minikube runs out of resources? (CPU/memory exhausted)
- How does the system handle database connection failures? (Neon unavailable)
- What happens when image pull fails? (Image not loaded into Minikube)
- How does Ingress behave when backend is unhealthy? (503 errors)
- What happens during rolling update? (Zero-downtime deployment)
- How does the system handle secrets not being created? (Pod fails to start)

## Requirements *(mandatory)*

### Functional Requirements

#### Docker Requirements
- **FR-001**: Frontend Dockerfile MUST use multi-stage build with node:18-alpine base
- **FR-002**: Backend Dockerfile MUST use multi-stage build with python:3.13-slim base
- **FR-003**: All containers MUST run as non-root users
- **FR-004**: Frontend image size MUST be < 200MB
- **FR-005**: Backend image size MUST be < 150MB
- **FR-006**: Both Dockerfiles MUST have corresponding .dockerignore files

#### Kubernetes Requirements
- **FR-007**: Deployments MUST specify resource requests and limits
- **FR-008**: All pods MUST have liveness and readiness probes
- **FR-009**: Deployments MUST have at least 2 replicas for availability
- **FR-010**: Services MUST use ClusterIP type for internal communication
- **FR-011**: ConfigMaps MUST contain all non-sensitive configuration
- **FR-012**: Secrets MUST contain all sensitive configuration (base64 encoded)
- **FR-013**: Secrets MUST NOT be committed to git repository

#### Helm Requirements
- **FR-014**: Helm chart MUST pass `helm lint` without errors
- **FR-015**: All resource names MUST use template helpers for consistency
- **FR-016**: Replica counts MUST be configurable via values.yaml
- **FR-017**: Image repositories and tags MUST be configurable
- **FR-018**: Resource limits MUST be defined in values.yaml

#### Networking Requirements
- **FR-019**: Ingress MUST route `/` to frontend service
- **FR-020**: Ingress MUST route `/api` to backend service
- **FR-021**: Ingress MUST use host `todo.local`
- **FR-022**: CORS MUST be configured to allow Ingress host

#### Health Check Requirements
- **FR-023**: Frontend MUST expose `/api/health` endpoint returning 200
- **FR-024**: Backend MUST expose `/health` endpoint returning 200
- **FR-025**: Backend MUST expose `/ready` endpoint for readiness checks

### Key Entities

- **Docker Image**: Container image with application code, dependencies, and runtime
- **Deployment**: Kubernetes resource managing pod replicas and updates
- **Service**: Kubernetes resource providing network access to pods
- **ConfigMap**: Kubernetes resource storing non-sensitive configuration
- **Secret**: Kubernetes resource storing sensitive configuration
- **Ingress**: Kubernetes resource routing external traffic to services
- **Helm Chart**: Package containing Kubernetes manifests with templating
- **Release**: Installed instance of a Helm chart

## Technical Implementation

### Docker Configuration

#### Frontend Dockerfile (frontend/Dockerfile)

```dockerfile
# Stage 1: Dependencies
FROM node:18-alpine AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --only=production

# Stage 2: Builder
FROM node:18-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
ENV NEXT_TELEMETRY_DISABLED=1
RUN npm run build

# Stage 3: Runner
FROM node:18-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs
EXPOSE 3000
ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

CMD ["node", "server.js"]
```

#### Backend Dockerfile (backend/Dockerfile)

```dockerfile
# Stage 1: Builder
FROM python:3.13-slim AS builder
WORKDIR /app
RUN pip install --no-cache-dir poetry
COPY pyproject.toml poetry.lock ./
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes
COPY . .

# Stage 2: Runner
FROM python:3.13-slim AS runner
WORKDIR /app

RUN groupadd --gid 1001 appgroup && \
    useradd --uid 1001 --gid appgroup --shell /bin/false appuser

COPY --from=builder /app/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY --from=builder --chown=appuser:appgroup /app/src ./src

USER appuser
EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Kubernetes Manifests Structure

```
k8s/
├── manifests/
│   ├── namespace.yaml           # Optional: dedicated namespace
│   ├── configmap.yaml           # Non-sensitive configuration
│   ├── secret.yaml.example      # Template (never commit actual secrets)
│   ├── deployment-frontend.yaml # Frontend deployment
│   ├── deployment-backend.yaml  # Backend deployment
│   ├── service-frontend.yaml    # Frontend service
│   ├── service-backend.yaml     # Backend service
│   └── ingress.yaml             # Ingress routing rules
└── helm/
    └── todo-app/
        ├── Chart.yaml
        ├── values.yaml
        ├── values-local.yaml
        ├── templates/
        │   ├── _helpers.tpl
        │   ├── configmap.yaml
        │   ├── secret.yaml
        │   ├── deployment-frontend.yaml
        │   ├── deployment-backend.yaml
        │   ├── service-frontend.yaml
        │   ├── service-backend.yaml
        │   └── ingress.yaml
        └── README.md
```

### Helm Chart values.yaml Structure

```yaml
# Global settings
global:
  environment: local

# Frontend configuration
frontend:
  name: todo-frontend
  replicas: 2
  image:
    repository: todo-frontend
    tag: latest
    pullPolicy: IfNotPresent
  service:
    type: ClusterIP
    port: 3000
  resources:
    requests:
      memory: "128Mi"
      cpu: "100m"
    limits:
      memory: "256Mi"
      cpu: "200m"
  probes:
    liveness:
      path: /api/health
      initialDelaySeconds: 10
      periodSeconds: 10
    readiness:
      path: /api/health
      initialDelaySeconds: 5
      periodSeconds: 5

# Backend configuration
backend:
  name: todo-backend
  replicas: 2
  image:
    repository: todo-backend
    tag: latest
    pullPolicy: IfNotPresent
  service:
    type: ClusterIP
    port: 8000
  resources:
    requests:
      memory: "256Mi"
      cpu: "200m"
    limits:
      memory: "512Mi"
      cpu: "400m"
  probes:
    liveness:
      path: /health
      initialDelaySeconds: 15
      periodSeconds: 10
    readiness:
      path: /ready
      initialDelaySeconds: 10
      periodSeconds: 5

# Ingress configuration
ingress:
  enabled: true
  className: nginx
  host: todo.local
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /

# ConfigMap values
config:
  apiUrl: http://todo-backend:8000
  frontendUrl: http://todo.local
  corsOrigins: http://todo.local
  logLevel: info

# Secret references (values provided at install time)
secrets:
  databaseUrl: ""
  openaiApiKey: ""
  jwtSecret: ""
  betterAuthSecret: ""
```

### Deployment Scripts

#### scripts/build-images.sh
```bash
#!/bin/bash
set -e

VERSION=${1:-latest}

echo "Building frontend image..."
docker build -t todo-frontend:$VERSION ./frontend

echo "Building backend image..."
docker build -t todo-backend:$VERSION ./backend

echo "Images built successfully!"
docker images | grep todo
```

#### scripts/deploy-local.sh
```bash
#!/bin/bash
set -e

# Start Minikube if not running
if ! minikube status | grep -q "Running"; then
    echo "Starting Minikube..."
    minikube start --memory=4096 --cpus=2
fi

# Enable ingress addon
minikube addons enable ingress

# Load images into Minikube
echo "Loading images into Minikube..."
minikube image load todo-frontend:latest
minikube image load todo-backend:latest

# Deploy with Helm
echo "Deploying with Helm..."
helm upgrade --install todo ./k8s/helm/todo-app \
    --set secrets.databaseUrl="$DATABASE_URL" \
    --set secrets.openaiApiKey="$OPENAI_API_KEY" \
    --set secrets.jwtSecret="$JWT_SECRET" \
    --set secrets.betterAuthSecret="$BETTER_AUTH_SECRET"

# Wait for pods
echo "Waiting for pods to be ready..."
kubectl wait --for=condition=ready pod -l app.kubernetes.io/instance=todo --timeout=120s

echo "Deployment complete!"
echo "Add '127.0.0.1 todo.local' to your hosts file"
echo "Then access: http://todo.local"
```

#### scripts/test-deployment.sh
```bash
#!/bin/bash
set -e

echo "=== Testing Kubernetes Deployment ==="

# Test 1: Pod Status
echo -e "\n1. Checking pod status..."
kubectl get pods -l app.kubernetes.io/instance=todo

# Test 2: Service Endpoints
echo -e "\n2. Checking services..."
kubectl get services -l app.kubernetes.io/instance=todo

# Test 3: Ingress
echo -e "\n3. Checking ingress..."
kubectl get ingress

# Test 4: Health endpoints via port-forward
echo -e "\n4. Testing health endpoints..."
kubectl port-forward svc/todo-backend 8000:8000 &
PF_PID=$!
sleep 3
curl -s http://localhost:8000/health && echo " - Backend health: OK"
kill $PF_PID 2>/dev/null

# Test 5: Logs check
echo -e "\n5. Checking for errors in logs..."
kubectl logs -l app.kubernetes.io/instance=todo --tail=10 | grep -i error || echo "No errors found"

echo -e "\n=== All tests completed ==="
```

## Success Criteria *(mandatory)*

### Measurable Outcomes

#### MVP Criteria
- **SC-001**: Docker images build successfully (`docker build` exits 0)
- **SC-002**: Frontend image size < 200MB, Backend image size < 150MB
- **SC-003**: Containers run as non-root (`docker exec <container> whoami` returns non-root)
- **SC-004**: Minikube cluster starts and is healthy (`kubectl cluster-info` succeeds)
- **SC-005**: Helm chart passes linting (`helm lint` exits 0)
- **SC-006**: Application deploys via Helm (`helm install` exits 0)
- **SC-007**: All pods reach Running state within 120 seconds
- **SC-008**: Services have active endpoints (`kubectl get endpoints` shows IPs)
- **SC-009**: Application accessible via http://todo.local
- **SC-010**: All Phase 3 features functional (CRUD + AI chatbot)

#### Excellence Criteria
- **SC-011**: Multi-stage Docker builds implemented (verified in Dockerfiles)
- **SC-012**: Resource requests and limits configured for all containers
- **SC-013**: Liveness and readiness probes passing for all pods
- **SC-014**: Helm chart uses template helpers for all resource names
- **SC-015**: AIOps tools documented with examples of usage
- **SC-016**: Automated deployment scripts working (`scripts/*.sh` executable)
- **SC-017**: Zero errors in `kubectl logs` after deployment

## Quality Gates

### Pre-Deployment Checklist
- [x] Docker images build successfully
- [ ] Image sizes within targets (frontend: 296MB, backend: 317MB - above targets)
- [x] Containers run as non-root (nextjs, appuser)
- [x] Health endpoints respond correctly (/health, /ready, /api/health)
- [x] ConfigMaps created with correct values
- [x] Secrets template created (not committed to git)
- [x] Helm chart validates (`helm lint`)
- [x] values.yaml properly configured

### Post-Deployment Checklist
- [ ] All pods in Running state (pending - requires cluster)
- [ ] Liveness probes passing (pending - requires cluster)
- [ ] Readiness probes passing (pending - requires cluster)
- [ ] Services have endpoints (pending - requires cluster)
- [ ] Ingress configured correctly (pending - requires cluster)
- [ ] Application accessible via browser at http://todo.local (pending - requires cluster)
- [ ] All Phase 3 features functional (pending - requires cluster)
- [ ] Logs show no errors (pending - requires cluster)
