# Deployment Guide

This guide covers deploying the Todo App to various cloud Kubernetes providers.

## Prerequisites

- Docker and Docker Compose installed
- kubectl configured
- Access to a container registry (GitHub Container Registry recommended)
- Kubernetes cluster (AKS, GKE, or DOKS)

## GitHub Environment Secrets

Configure these secrets in your GitHub repository settings:

### Required Secrets

| Secret Name | Description | Example |
|-------------|-------------|---------|
| `REGISTRY_USERNAME` | Container registry username | `your-github-username` |
| `REGISTRY_PASSWORD` | Container registry password/token | GitHub PAT with `write:packages` |
| `KUBE_CONFIG` | Base64-encoded kubeconfig | `base64 -w0 ~/.kube/config` |
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@host:5432/db` |
| `JWT_SECRET` | Secret for JWT signing | Randomly generated 256-bit key |

### Optional Secrets

| Secret Name | Description | Default |
|-------------|-------------|---------|
| `SLACK_WEBHOOK_URL` | Slack notifications | - |
| `SENTRY_DSN` | Error tracking | - |
| `OPENAI_API_KEY` | AI chat features | - |

## Local Development with Docker Compose

```bash
# Start all services with Dapr sidecars
cd phase-2
docker-compose up -d

# View logs
docker-compose logs -f backend

# Stop services
docker-compose down
```

## Kubernetes Deployment

### 1. Build and Push Images

```bash
# Login to GitHub Container Registry
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin

# Build and push backend
docker build -t ghcr.io/your-org/todo-backend:latest ./phase-2/backend
docker push ghcr.io/your-org/todo-backend:latest

# Build and push frontend
docker build -t ghcr.io/your-org/todo-frontend:latest ./phase-2/frontend
docker push ghcr.io/your-org/todo-frontend:latest
```

### 2. Create Secrets

```bash
# Create namespace
kubectl apply -f k8s/cloud/base/namespace.yaml

# Create secrets (update values first!)
kubectl apply -f k8s/cloud/base/secrets.yaml

# Create image pull secret for GHCR
kubectl create secret docker-registry ghcr-secret \
  --docker-server=ghcr.io \
  --docker-username=YOUR_USERNAME \
  --docker-password=YOUR_GITHUB_PAT \
  -n todo-app
```

### 3. Deploy to Staging

```bash
# Using the deploy script
./scripts/deploy.sh staging latest

# Or manually with Kustomize
kubectl apply -k k8s/cloud/overlays/staging
```

### 4. Deploy to Production

```bash
# Using the deploy script (with confirmation)
./scripts/deploy.sh production v1.0.0

# Or manually
kubectl apply -k k8s/cloud/overlays/production
```

## Cloud Provider Configuration

### DigitalOcean Kubernetes (DOKS)

```bash
# Install doctl CLI
brew install doctl

# Authenticate
doctl auth init

# Get cluster credentials
doctl kubernetes cluster kubeconfig save your-cluster-name

# Deploy with DOKS overlay
kubectl apply -k k8s/cloud/providers/doks
kubectl apply -k k8s/cloud/overlays/production
```

### Azure Kubernetes Service (AKS)

```bash
# Install Azure CLI
brew install azure-cli

# Login and get credentials
az login
az aks get-credentials --resource-group myResourceGroup --name myAKSCluster

# Deploy with AKS overlay
kubectl apply -k k8s/cloud/providers/aks
kubectl apply -k k8s/cloud/overlays/production
```

### Google Kubernetes Engine (GKE)

```bash
# Install gcloud CLI and authenticate
gcloud auth login
gcloud container clusters get-credentials your-cluster --zone us-central1-a

# Deploy with GKE overlay
kubectl apply -k k8s/cloud/providers/gke
kubectl apply -k k8s/cloud/overlays/production
```

## Monitoring Setup

### Deploy Monitoring Stack

```bash
# Create monitoring namespace
kubectl create namespace monitoring

# Deploy Prometheus, Grafana, and Loki
kubectl apply -k k8s/monitoring
```

### Access Dashboards

```bash
# Port forward Grafana
kubectl port-forward svc/grafana 3000:3000 -n monitoring

# Access at http://localhost:3000
# Default credentials: admin/admin
```

## Rollback Procedure

```bash
# Quick rollback to previous version
./scripts/rollback.sh production

# Rollback to specific revision
./scripts/rollback.sh production 3
```

## Troubleshooting

### Common Issues

1. **Pods not starting**: Check image pull secrets and container registry access
2. **Database connection errors**: Verify DATABASE_URL secret is correct
3. **Dapr sidecar not injecting**: Ensure Dapr is installed in cluster

### Useful Commands

```bash
# Check pod status
kubectl get pods -n todo-app

# View pod logs
kubectl logs -f deployment/backend-deployment -n todo-app

# Describe pod for events
kubectl describe pod <pod-name> -n todo-app

# Check Dapr sidecar logs
kubectl logs <pod-name> -c daprd -n todo-app
```

## CI/CD Pipeline

The GitHub Actions workflows automatically:

1. **CI (ci.yml)**: Runs on every push
   - Lints code
   - Runs tests
   - Builds Docker images
   - Scans for vulnerabilities

2. **CD Staging (cd-staging.yml)**: Runs on push to main
   - Builds and pushes images
   - Deploys to staging environment

3. **CD Production (cd-production.yml)**: Manual trigger
   - Requires approval
   - Deploys to production
   - Runs smoke tests
