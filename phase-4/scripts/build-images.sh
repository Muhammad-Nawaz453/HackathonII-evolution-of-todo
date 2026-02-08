#!/bin/bash
set -e

echo "🐳 Building Docker images for Todo App..."

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Check if Docker is running
if ! docker info &> /dev/null; then
    echo -e "${RED}❌ Docker is not running${NC}"
    echo "Please start Docker and try again"
    exit 1
fi

echo -e "${GREEN}✓ Docker is running${NC}"

# Check if Minikube is running
if ! minikube status &> /dev/null; then
    echo -e "${RED}❌ Minikube is not running${NC}"
    echo "Please run ./scripts/setup-minikube.sh first"
    exit 1
fi

echo -e "${GREEN}✓ Minikube is running${NC}"

# Set Docker environment to use Minikube's Docker daemon
echo -e "${BLUE}Configuring Docker to use Minikube's daemon...${NC}"
eval $(minikube docker-env)
echo -e "${GREEN}✓ Docker environment configured${NC}"

# Build backend image
echo -e "\n${BLUE}Building backend image...${NC}"
docker build \
    -t todo-backend:latest \
    -f docker/backend/Dockerfile \
    ../phase-3/backend

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Backend image built successfully${NC}"
else
    echo -e "${RED}❌ Backend image build failed${NC}"
    exit 1
fi

# Build frontend image
echo -e "\n${BLUE}Building frontend image...${NC}"
docker build \
    -t todo-frontend:latest \
    -f docker/frontend/Dockerfile \
    ../phase-3/frontend

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Frontend image built successfully${NC}"
else
    echo -e "${RED}❌ Frontend image build failed${NC}"
    exit 1
fi

# Show image sizes
echo -e "\n${BLUE}Image sizes:${NC}"
docker images | grep -E "REPOSITORY|todo-"

# Verify images are in Minikube
echo -e "\n${BLUE}Verifying images in Minikube...${NC}"
minikube image ls | grep todo-

echo -e "\n${GREEN}✅ All images built successfully!${NC}"

echo -e "\n${BLUE}Images built:${NC}"
echo "  - todo-backend:latest"
echo "  - todo-frontend:latest"

echo -e "\n${YELLOW}Next steps:${NC}"
echo "  Run ./scripts/deploy-local.sh to deploy the application"

# Reset Docker environment
eval $(minikube docker-env -u)
