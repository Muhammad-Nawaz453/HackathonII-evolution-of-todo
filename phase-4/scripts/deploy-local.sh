#!/bin/bash
set -e

echo "🚀 Deploying Todo App to Minikube..."

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Check prerequisites
if ! command -v helm &> /dev/null; then
    echo -e "${RED}❌ Helm is not installed${NC}"
    echo "Please install Helm: https://helm.sh/docs/intro/install/"
    exit 1
fi

if ! minikube status &> /dev/null; then
    echo -e "${RED}❌ Minikube is not running${NC}"
    echo "Please run ./scripts/setup-minikube.sh first"
    exit 1
fi

echo -e "${GREEN}✓ Prerequisites met${NC}"

# Check if images exist
echo -e "${BLUE}Checking if Docker images exist...${NC}"
eval $(minikube docker-env)

if ! docker images | grep -q "todo-backend"; then
    echo -e "${RED}❌ Backend image not found${NC}"
    echo "Please run ./scripts/build-images.sh first"
    exit 1
fi

if ! docker images | grep -q "todo-frontend"; then
    echo -e "${RED}❌ Frontend image not found${NC}"
    echo "Please run ./scripts/build-images.sh first"
    exit 1
fi

echo -e "${GREEN}✓ Docker images found${NC}"

# Check if OpenAI API key is set
if [ -z "$OPENAI_API_KEY" ]; then
    echo -e "${YELLOW}⚠ OPENAI_API_KEY not set${NC}"
    read -p "Enter your OpenAI API key: " api_key
    export OPENAI_API_KEY="$api_key"
fi

# Create namespace
echo -e "\n${BLUE}Creating namespace...${NC}"
kubectl create namespace todo-app-dev --dry-run=client -o yaml | kubectl apply -f -
echo -e "${GREEN}✓ Namespace created${NC}"

# Deploy with Helm
echo -e "\n${BLUE}Deploying with Helm...${NC}"

# Check if release already exists
if helm list -n todo-app-dev | grep -q "todo-app"; then
    echo -e "${YELLOW}⚠ Release already exists, upgrading...${NC}"
    helm upgrade todo-app ./helm/todo-app \
        -f helm/todo-app/values-dev.yaml \
        -n todo-app-dev \
        --set backend.secrets.openaiApiKey="$OPENAI_API_KEY" \
        --wait \
        --timeout 5m
else
    echo -e "${BLUE}Installing new release...${NC}"
    helm install todo-app ./helm/todo-app \
        -f helm/todo-app/values-dev.yaml \
        -n todo-app-dev \
        --set backend.secrets.openaiApiKey="$OPENAI_API_KEY" \
        --wait \
        --timeout 5m
fi

echo -e "${GREEN}✓ Helm deployment complete${NC}"

# Wait for pods to be ready
echo -e "\n${BLUE}Waiting for pods to be ready...${NC}"
kubectl wait --for=condition=ready pod \
    -l app.kubernetes.io/name=todo-app \
    -n todo-app-dev \
    --timeout=300s

echo -e "${GREEN}✓ All pods are ready${NC}"

# Show deployment status
echo -e "\n${BLUE}Deployment Status:${NC}"
kubectl get pods -n todo-app-dev
kubectl get services -n todo-app-dev

# Get frontend URL
echo -e "\n${BLUE}Getting application URL...${NC}"
FRONTEND_URL=$(minikube service todo-app-frontend -n todo-app-dev --url)

echo -e "\n${GREEN}✅ Deployment complete!${NC}"

echo -e "\n${BLUE}Access the application:${NC}"
echo "  Frontend: $FRONTEND_URL"
echo "  Backend: http://$(minikube ip):$(kubectl get svc todo-app-backend -n todo-app-dev -o jsonpath='{.spec.ports[0].nodePort}')"

echo -e "\n${BLUE}Useful commands:${NC}"
echo "  kubectl get pods -n todo-app-dev              # View pods"
echo "  kubectl logs -f <pod-name> -n todo-app-dev    # View logs"
echo "  kubectl describe pod <pod-name> -n todo-app-dev  # Pod details"
echo "  helm list -n todo-app-dev                     # List releases"
echo "  helm status todo-app -n todo-app-dev          # Release status"

echo -e "\n${BLUE}Port forwarding (alternative access):${NC}"
echo "  kubectl port-forward svc/todo-app-frontend 3000:3000 -n todo-app-dev"
echo "  kubectl port-forward svc/todo-app-backend 8000:8000 -n todo-app-dev"

echo -e "\n${YELLOW}To open the application in browser:${NC}"
echo "  minikube service todo-app-frontend -n todo-app-dev"

# Reset Docker environment
eval $(minikube docker-env -u)
