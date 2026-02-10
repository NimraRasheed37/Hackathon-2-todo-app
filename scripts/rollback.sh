#!/bin/bash
# Rollback script for Todo App
# Usage: ./rollback.sh [staging|production] [revision]

set -euo pipefail

ENVIRONMENT="${1:-staging}"
REVISION="${2:-}"

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

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

# Set namespace and deployment names
if [[ "$ENVIRONMENT" == "production" ]]; then
    NAMESPACE="todo-app-production"
    BACKEND_DEPLOYMENT="prod-backend-deployment"
    FRONTEND_DEPLOYMENT="prod-frontend-deployment"
else
    NAMESPACE="todo-app-staging"
    BACKEND_DEPLOYMENT="staging-backend-deployment"
    FRONTEND_DEPLOYMENT="staging-frontend-deployment"
fi

log_info "Rolling back $ENVIRONMENT environment..."

# Show rollout history
log_info "Current rollout history:"
echo "Backend:"
kubectl rollout history deployment/"$BACKEND_DEPLOYMENT" -n "$NAMESPACE" || true
echo ""
echo "Frontend:"
kubectl rollout history deployment/"$FRONTEND_DEPLOYMENT" -n "$NAMESPACE" || true
echo ""

# Perform rollback
if [[ -n "$REVISION" ]]; then
    log_info "Rolling back to revision $REVISION..."
    kubectl rollout undo deployment/"$BACKEND_DEPLOYMENT" -n "$NAMESPACE" --to-revision="$REVISION"
    kubectl rollout undo deployment/"$FRONTEND_DEPLOYMENT" -n "$NAMESPACE" --to-revision="$REVISION"
else
    log_info "Rolling back to previous revision..."
    kubectl rollout undo deployment/"$BACKEND_DEPLOYMENT" -n "$NAMESPACE"
    kubectl rollout undo deployment/"$FRONTEND_DEPLOYMENT" -n "$NAMESPACE"
fi

# Wait for rollback to complete
log_info "Waiting for rollback to complete..."
kubectl rollout status deployment/"$BACKEND_DEPLOYMENT" -n "$NAMESPACE" --timeout=300s
kubectl rollout status deployment/"$FRONTEND_DEPLOYMENT" -n "$NAMESPACE" --timeout=300s

# Verify rollback
log_info "Rollback completed. Current state:"
kubectl get pods -n "$NAMESPACE"

# Health check
log_info "Running health checks..."
sleep 10

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

log_info "Rollback of $ENVIRONMENT completed successfully!"
