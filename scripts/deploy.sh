#!/bin/bash
# Deploy script for Todo App
# Usage: ./deploy.sh [staging|production] [version]

set -euo pipefail

ENVIRONMENT="${1:-staging}"
VERSION="${2:-latest}"

# Configuration
REGISTRY="ghcr.io/your-org"
BACKEND_IMAGE="todo-backend"
FRONTEND_IMAGE="todo-frontend"

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Validate environment
if [[ "$ENVIRONMENT" != "staging" && "$ENVIRONMENT" != "production" ]]; then
    log_error "Invalid environment. Use 'staging' or 'production'"
    exit 1
fi

log_info "Deploying to $ENVIRONMENT with version $VERSION"

# Check kubectl is available
if ! command -v kubectl &> /dev/null; then
    log_error "kubectl not found. Please install kubectl."
    exit 1
fi

# Check kustomize is available
if ! command -v kustomize &> /dev/null; then
    log_error "kustomize not found. Please install kustomize."
    exit 1
fi

# Verify cluster connection
log_info "Verifying cluster connection..."
if ! kubectl cluster-info &> /dev/null; then
    log_error "Cannot connect to Kubernetes cluster. Check your kubeconfig."
    exit 1
fi

# Set namespace based on environment
if [[ "$ENVIRONMENT" == "production" ]]; then
    NAMESPACE="todo-app-production"
    OVERLAY_PATH="k8s/cloud/overlays/production"
else
    NAMESPACE="todo-app-staging"
    OVERLAY_PATH="k8s/cloud/overlays/staging"
fi

# Update image tags
log_info "Updating image tags..."
cd "$OVERLAY_PATH"
kustomize edit set image \
    "ghcr.io/your-org/todo-backend=${REGISTRY}/${BACKEND_IMAGE}:${VERSION}" \
    "ghcr.io/your-org/todo-frontend=${REGISTRY}/${FRONTEND_IMAGE}:${VERSION}"
cd - > /dev/null

# Create backup of current deployment
log_info "Creating backup of current deployment..."
kubectl get deployment -n "$NAMESPACE" -o yaml > "/tmp/backup-${NAMESPACE}-$(date +%Y%m%d%H%M%S).yaml" 2>/dev/null || true

# Apply deployment
log_info "Applying deployment..."
kubectl apply -k "$OVERLAY_PATH"

# Wait for rollout
log_info "Waiting for backend rollout..."
if [[ "$ENVIRONMENT" == "production" ]]; then
    kubectl rollout status deployment/prod-backend-deployment -n "$NAMESPACE" --timeout=600s
    kubectl rollout status deployment/prod-frontend-deployment -n "$NAMESPACE" --timeout=600s
else
    kubectl rollout status deployment/staging-backend-deployment -n "$NAMESPACE" --timeout=300s
    kubectl rollout status deployment/staging-frontend-deployment -n "$NAMESPACE" --timeout=300s
fi

# Verify deployment
log_info "Verifying deployment..."
kubectl get pods -n "$NAMESPACE"
kubectl get services -n "$NAMESPACE"

# Health check
log_info "Running health checks..."
sleep 10

# Get service URL (for ingress-based deployments)
if [[ "$ENVIRONMENT" == "production" ]]; then
    HEALTH_URL="https://api.your-domain.com/health"
else
    HEALTH_URL="https://staging-api.your-domain.com/health"
fi

for i in {1..5}; do
    if curl -sf "$HEALTH_URL" > /dev/null 2>&1; then
        log_info "Health check passed!"
        break
    fi
    log_warn "Health check attempt $i failed, retrying in 10s..."
    sleep 10
done

log_info "Deployment to $ENVIRONMENT completed successfully!"
echo ""
echo "Deployed version: $VERSION"
echo "Namespace: $NAMESPACE"
echo ""
