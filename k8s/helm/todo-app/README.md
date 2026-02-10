# Todo App Helm Chart

A Helm chart for deploying the Todo App (frontend + backend) to Kubernetes.

## Prerequisites

- Kubernetes 1.19+
- Helm 3.2.0+
- Minikube (for local development)
- NGINX Ingress Controller

## Installation

### Quick Start (Local Development)

1. Start Minikube with ingress addon:
   ```bash
   minikube start --driver=docker
   minikube addons enable ingress
   ```

2. Build Docker images:
   ```bash
   eval $(minikube docker-env)
   docker build -t todo-frontend:local ./phase-2/frontend
   docker build -t todo-backend:local ./phase-2/backend
   ```

3. Create local values file with your secrets:
   ```bash
   cp k8s/helm/todo-app/values.yaml k8s/helm/todo-app/values-local.yaml
   # Edit values-local.yaml with your secrets
   ```

4. Install the chart:
   ```bash
   helm install todo-app ./k8s/helm/todo-app -f ./k8s/helm/todo-app/values-local.yaml
   ```

5. Add hosts entry:
   ```bash
   echo "$(minikube ip) todo.local" | sudo tee -a /etc/hosts
   ```

6. Access the application at `http://todo.local`

### Upgrading

```bash
helm upgrade todo-app ./k8s/helm/todo-app -f ./k8s/helm/todo-app/values-local.yaml
```

### Uninstalling

```bash
helm uninstall todo-app
```

## Configuration

### Global Settings

| Parameter | Description | Default |
|-----------|-------------|---------|
| `global.environment` | Environment name | `development` |
| `nameOverride` | Override chart name | `""` |
| `fullnameOverride` | Override full name | `""` |

### Frontend Configuration

| Parameter | Description | Default |
|-----------|-------------|---------|
| `frontend.replicas` | Number of replicas | `1` |
| `frontend.image.repository` | Image repository | `todo-frontend` |
| `frontend.image.tag` | Image tag | `local` |
| `frontend.image.pullPolicy` | Image pull policy | `IfNotPresent` |
| `frontend.service.type` | Service type | `ClusterIP` |
| `frontend.service.port` | Service port | `3000` |
| `frontend.resources.limits.cpu` | CPU limit | `500m` |
| `frontend.resources.limits.memory` | Memory limit | `512Mi` |
| `frontend.resources.requests.cpu` | CPU request | `100m` |
| `frontend.resources.requests.memory` | Memory request | `128Mi` |

### Backend Configuration

| Parameter | Description | Default |
|-----------|-------------|---------|
| `backend.replicas` | Number of replicas | `1` |
| `backend.image.repository` | Image repository | `todo-backend` |
| `backend.image.tag` | Image tag | `local` |
| `backend.image.pullPolicy` | Image pull policy | `IfNotPresent` |
| `backend.service.type` | Service type | `ClusterIP` |
| `backend.service.port` | Service port | `8000` |
| `backend.resources.limits.cpu` | CPU limit | `500m` |
| `backend.resources.limits.memory` | Memory limit | `512Mi` |
| `backend.resources.requests.cpu` | CPU request | `100m` |
| `backend.resources.requests.memory` | Memory request | `128Mi` |

### Ingress Configuration

| Parameter | Description | Default |
|-----------|-------------|---------|
| `ingress.enabled` | Enable ingress | `true` |
| `ingress.className` | Ingress class name | `nginx` |
| `ingress.host` | Ingress hostname | `todo.local` |
| `ingress.annotations` | Ingress annotations | `{}` |
| `ingress.tls` | TLS configuration | `[]` |

### Secrets

| Parameter | Description | Required |
|-----------|-------------|----------|
| `secrets.databaseUrl` | PostgreSQL connection string | Yes |
| `secrets.openaiApiKey` | OpenAI API key | Yes |
| `secrets.jwtSecret` | JWT signing secret | Yes |
| `secrets.betterAuthSecret` | Better Auth secret | Yes |

### Config

| Parameter | Description | Default |
|-----------|-------------|---------|
| `config.apiUrl` | Backend API URL | `http://todo.local/api` |
| `config.frontendUrl` | Frontend URL | `http://todo.local` |
| `config.corsOrigins` | CORS allowed origins | `http://todo.local` |
| `config.logLevel` | Logging level | `info` |

## Health Checks

The chart configures liveness and readiness probes for both services:

- **Frontend**: `/api/health`
- **Backend**: `/health` (liveness), `/ready` (readiness)

## Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Ingress   │────▶│  Frontend   │────▶│   Backend   │
│  (NGINX)    │     │  (Next.js)  │     │  (FastAPI)  │
└─────────────┘     └─────────────┘     └─────────────┘
                                              │
                                              ▼
                                        ┌─────────────┐
                                        │  PostgreSQL │
                                        │   (Neon)    │
                                        └─────────────┘
```

## Troubleshooting

### Pods not starting

Check pod status and logs:
```bash
kubectl get pods
kubectl describe pod <pod-name>
kubectl logs <pod-name>
```

### Ingress not working

Verify ingress controller is running:
```bash
kubectl get pods -n ingress-nginx
minikube addons list | grep ingress
```

### Database connection issues

Verify the DATABASE_URL secret is correct and the database is accessible from within the cluster.
