#!/bin/bash
set -e

echo "🚀 Setting up Minikube for Todo App..."

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if Minikube is installed
if ! command -v minikube &> /dev/null; then
    echo -e "${RED}❌ Minikube is not installed${NC}"
    echo "Please install Minikube: https://minikube.sigs.k8s.io/docs/start/"
    exit 1
fi

echo -e "${GREEN}✓ Minikube is installed${NC}"

# Check if kubectl is installed
if ! command -v kubectl &> /dev/null; then
    echo -e "${RED}❌ kubectl is not installed${NC}"
    echo "Please install kubectl: https://kubernetes.io/docs/tasks/tools/"
    exit 1
fi

echo -e "${GREEN}✓ kubectl is installed${NC}"

# Check if Minikube is already running
if minikube status &> /dev/null; then
    echo -e "${YELLOW}⚠ Minikube is already running${NC}"
    read -p "Do you want to delete and recreate the cluster? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${BLUE}Deleting existing Minikube cluster...${NC}"
        minikube delete
    else
        echo -e "${BLUE}Using existing Minikube cluster${NC}"
        exit 0
    fi
fi

# Start Minikube with appropriate resources
echo -e "${BLUE}Starting Minikube cluster...${NC}"
minikube start \
    --cpus=4 \
    --memory=8192 \
    --disk-size=20g \
    --driver=docker \
    --kubernetes-version=v1.28.0

echo -e "${GREEN}✓ Minikube cluster started${NC}"

# Enable required addons
echo -e "${BLUE}Enabling Minikube addons...${NC}"

# Enable ingress
minikube addons enable ingress
echo -e "${GREEN}✓ Ingress addon enabled${NC}"

# Enable metrics-server
minikube addons enable metrics-server
echo -e "${GREEN}✓ Metrics-server addon enabled${NC}"

# Enable dashboard
minikube addons enable dashboard
echo -e "${GREEN}✓ Dashboard addon enabled${NC}"

# Configure kubectl context
echo -e "${BLUE}Configuring kubectl context...${NC}"
kubectl config use-context minikube
echo -e "${GREEN}✓ kubectl context set to minikube${NC}"

# Verify cluster is ready
echo -e "${BLUE}Verifying cluster status...${NC}"
kubectl cluster-info
kubectl get nodes

echo -e "\n${GREEN}✅ Minikube setup complete!${NC}"
echo -e "\n${BLUE}Cluster Information:${NC}"
echo "  Context: $(kubectl config current-context)"
echo "  Nodes: $(kubectl get nodes --no-headers | wc -l)"
echo "  Kubernetes Version: $(kubectl version --short | grep Server | awk '{print $3}')"

echo -e "\n${BLUE}Useful commands:${NC}"
echo "  minikube status          # Check cluster status"
echo "  minikube dashboard       # Open Kubernetes dashboard"
echo "  minikube stop            # Stop the cluster"
echo "  minikube delete          # Delete the cluster"
echo "  kubectl get nodes        # View cluster nodes"

echo -e "\n${YELLOW}Next steps:${NC}"
echo "  1. Run ./scripts/build-images.sh to build Docker images"
echo "  2. Run ./scripts/deploy-local.sh to deploy the application"
