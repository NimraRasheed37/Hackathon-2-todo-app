#!/bin/bash
# cleanup.sh - Clean up Todo App deployment
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== Todo App Cleanup ===${NC}"

# Uninstall Helm release
echo -e "\n${YELLOW}Uninstalling Helm release...${NC}"
if helm status todo-app &> /dev/null; then
    helm uninstall todo-app
    echo -e "${GREEN}✓ Helm release uninstalled${NC}"
else
    echo -e "${YELLOW}No Helm release found${NC}"
fi

# Remove Docker images (optional)
echo -e "\n${YELLOW}Do you want to remove Docker images? (y/N)${NC}"
read -r REMOVE_IMAGES

if [[ "$REMOVE_IMAGES" =~ ^[Yy]$ ]]; then
    echo "Removing Docker images..."
    docker rmi todo-frontend:local 2>/dev/null || true
    docker rmi todo-backend:local 2>/dev/null || true
    echo -e "${GREEN}✓ Docker images removed${NC}"
fi

# Stop Minikube (optional)
echo -e "\n${YELLOW}Do you want to stop Minikube? (y/N)${NC}"
read -r STOP_MINIKUBE

if [[ "$STOP_MINIKUBE" =~ ^[Yy]$ ]]; then
    echo "Stopping Minikube..."
    minikube stop
    echo -e "${GREEN}✓ Minikube stopped${NC}"
fi

# Delete Minikube cluster (optional)
echo -e "\n${YELLOW}Do you want to delete the Minikube cluster? (y/N)${NC}"
read -r DELETE_MINIKUBE

if [[ "$DELETE_MINIKUBE" =~ ^[Yy]$ ]]; then
    echo -e "${RED}WARNING: This will delete all data in the cluster!${NC}"
    echo "Are you sure? (y/N)"
    read -r CONFIRM_DELETE

    if [[ "$CONFIRM_DELETE" =~ ^[Yy]$ ]]; then
        minikube delete
        echo -e "${GREEN}✓ Minikube cluster deleted${NC}"
    fi
fi

echo -e "\n${GREEN}=== Cleanup Complete ===${NC}"
echo ""
echo "Remember to remove the hosts file entry if no longer needed:"
echo "  sudo sed -i '/todo.local/d' /etc/hosts"
