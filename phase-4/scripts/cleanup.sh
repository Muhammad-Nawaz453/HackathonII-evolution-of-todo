#!/bin/bash
set -e

echo "🧹 Cleaning up Todo App deployment..."

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Confirm cleanup
read -p "This will delete all Todo App resources from Minikube. Continue? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cleanup cancelled"
    exit 0
fi

# Uninstall Helm release
echo -e "${BLUE}Uninstalling Helm release...${NC}"
if helm list -n todo-app-dev | grep -q "todo-app"; then
    helm uninstall todo-app -n todo-app-dev
    echo -e "${GREEN}✓ Helm release uninstalled${NC}"
else
    echo -e "${YELLOW}⚠ No Helm release found${NC}"
fi

# Delete namespace
echo -e "${BLUE}Deleting namespace...${NC}"
if kubectl get namespace todo-app-dev &> /dev/null; then
    kubectl delete namespace todo-app-dev --timeout=60s
    echo -e "${GREEN}✓ Namespace deleted${NC}"
else
    echo -e "${YELLOW}⚠ Namespace not found${NC}"
fi

# Clean up Docker images (optional)
read -p "Do you want to delete Docker images? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${BLUE}Deleting Docker images...${NC}"
    eval $(minikube docker-env)

    if docker images | grep -q "todo-backend"; then
        docker rmi todo-backend:latest
        echo -e "${GREEN}✓ Backend image deleted${NC}"
    fi

    if docker images | grep -q "todo-frontend"; then
        docker rmi todo-frontend:latest
        echo -e "${GREEN}✓ Frontend image deleted${NC}"
    fi

    eval $(minikube docker-env -u)
fi

# Clean up PVCs (if any remain)
echo -e "${BLUE}Checking for remaining PVCs...${NC}"
if kubectl get pvc -n todo-app-dev &> /dev/null; then
    kubectl delete pvc --all -n todo-app-dev
    echo -e "${GREEN}✓ PVCs deleted${NC}"
fi

echo -e "\n${GREEN}✅ Cleanup complete!${NC}"

echo -e "\n${BLUE}Remaining resources:${NC}"
kubectl get all -n todo-app-dev 2>/dev/null || echo "  No resources found"

echo -e "\n${YELLOW}To completely reset Minikube:${NC}"
echo "  minikube delete"
