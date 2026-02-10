#!/bin/bash
# deploy-local.sh - Deploy Todo App to local Minikube cluster
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== Todo App Local Deployment ===${NC}"

# Check prerequisites
echo -e "\n${YELLOW}Checking prerequisites...${NC}"

if ! command -v minikube &> /dev/null; then
    echo -e "${RED}Error: minikube is not installed${NC}"
    exit 1
fi

if ! command -v kubectl &> /dev/null; then
    echo -e "${RED}Error: kubectl is not installed${NC}"
    exit 1
fi

if ! command -v helm &> /dev/null; then
    echo -e "${RED}Error: helm is not installed${NC}"
    exit 1
fi

if ! command -v docker &> /dev/null; then
    echo -e "${RED}Error: docker is not installed${NC}"
    exit 1
fi

echo -e "${GREEN}✓ All prerequisites installed${NC}"

# Check if Minikube is running
echo -e "\n${YELLOW}Checking Minikube status...${NC}"
if ! minikube status &> /dev/null; then
    echo -e "${YELLOW}Starting Minikube...${NC}"
    minikube start --memory=4096 --cpus=2 --driver=docker
fi
echo -e "${GREEN}✓ Minikube is running${NC}"

# Enable ingress addon
echo -e "\n${YELLOW}Enabling ingress addon...${NC}"
minikube addons enable ingress
echo -e "${GREEN}✓ Ingress addon enabled${NC}"

# Set Docker environment to use Minikube's Docker daemon
echo -e "\n${YELLOW}Configuring Docker to use Minikube...${NC}"
eval $(minikube docker-env)
echo -e "${GREEN}✓ Docker configured for Minikube${NC}"

# Build Docker images
echo -e "\n${YELLOW}Building Docker images...${NC}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "Building frontend image..."
docker build -t todo-frontend:local "$PROJECT_ROOT/phase-2/frontend"
echo -e "${GREEN}✓ Frontend image built${NC}"

echo "Building backend image..."
docker build -t todo-backend:local "$PROJECT_ROOT/phase-2/backend"
echo -e "${GREEN}✓ Backend image built${NC}"

# Check for values-local.yaml
VALUES_FILE="$PROJECT_ROOT/k8s/helm/todo-app/values-local.yaml"
if [ ! -f "$VALUES_FILE" ]; then
    echo -e "${RED}Error: values-local.yaml not found${NC}"
    echo "Please create $VALUES_FILE with your secrets:"
    echo "  cp $PROJECT_ROOT/k8s/helm/todo-app/values.yaml $VALUES_FILE"
    echo "  # Then edit values-local.yaml with your secrets"
    exit 1
fi

# Deploy with Helm
echo -e "\n${YELLOW}Deploying with Helm...${NC}"
helm upgrade --install todo-app "$PROJECT_ROOT/k8s/helm/todo-app" \
    -f "$VALUES_FILE" \
    --wait \
    --timeout 5m

echo -e "${GREEN}✓ Helm deployment complete${NC}"

# Wait for pods to be ready
echo -e "\n${YELLOW}Waiting for pods to be ready...${NC}"
kubectl wait --for=condition=ready pod -l app.kubernetes.io/instance=todo-app --timeout=300s
echo -e "${GREEN}✓ All pods are ready${NC}"

# Get Minikube IP and add hosts entry reminder
MINIKUBE_IP=$(minikube ip)
echo -e "\n${GREEN}=== Deployment Complete ===${NC}"
echo -e "\n${YELLOW}Add this line to your /etc/hosts file:${NC}"
echo -e "${GREEN}$MINIKUBE_IP todo.local${NC}"
echo ""
echo -e "Access the application at: ${GREEN}http://todo.local${NC}"
echo ""
echo -e "Useful commands:"
echo -e "  kubectl get pods        # Check pod status"
echo -e "  kubectl logs -f <pod>   # View logs"
echo -e "  helm status todo-app    # Check Helm release status"
echo -e "  ./scripts/cleanup.sh    # Clean up deployment"
