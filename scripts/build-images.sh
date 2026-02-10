#!/bin/bash
# ===================================================
# Build Docker images for Todo App
# ===================================================
set -e

# Default version tag
VERSION=${1:-latest}

# Get script directory and project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "=================================================="
echo "Building Todo App Docker Images (v$VERSION)"
echo "=================================================="

# Build frontend image
echo ""
echo "Building frontend image..."
docker build -t todo-frontend:$VERSION "$PROJECT_ROOT/phase-2/frontend"

# Build backend image
echo ""
echo "Building backend image..."
docker build -t todo-backend:$VERSION "$PROJECT_ROOT/phase-2/backend"

echo ""
echo "=================================================="
echo "Build Complete!"
echo "=================================================="
echo ""
echo "Images built:"
docker images | grep todo | head -4

echo ""
echo "Image sizes:"
echo "  Frontend: $(docker images todo-frontend:$VERSION --format '{{.Size}}')"
echo "  Backend:  $(docker images todo-backend:$VERSION --format '{{.Size}}')"

echo ""
echo "Next steps:"
echo "  1. Load images into Minikube: minikube image load todo-frontend:$VERSION todo-backend:$VERSION"
echo "  2. Deploy with Helm: helm upgrade --install todo ./k8s/helm/todo-app"
