#!/bin/bash
set -e

echo "🤖 Setting up kubectl-ai..."

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Check if kubectl is installed
if ! command -v kubectl &> /dev/null; then
    echo -e "${RED}❌ kubectl not found${NC}"
    echo "Please install kubectl first"
    exit 1
fi

echo -e "${GREEN}✓ kubectl is installed${NC}"

# Check if OpenAI API key is set
if [ -z "$OPENAI_API_KEY" ]; then
    echo -e "${YELLOW}⚠ OPENAI_API_KEY not set${NC}"
    read -p "Enter your OpenAI API key: " api_key
    export OPENAI_API_KEY="$api_key"
    echo "export OPENAI_API_KEY=\"$api_key\"" >> ~/.bashrc
fi

echo -e "${GREEN}✓ OpenAI API key configured${NC}"

# Install krew if not installed
if ! command -v kubectl-krew &> /dev/null; then
    echo -e "${BLUE}Installing krew...${NC}"
    (
      set -x; cd "$(mktemp -d)" &&
      OS="$(uname | tr '[:upper:]' '[:lower:]')" &&
      ARCH="$(uname -m | sed -e 's/x86_64/amd64/' -e 's/\(arm\)\(64\)\?.*/\1\2/' -e 's/aarch64$/arm64/')" &&
      KREW="krew-${OS}_${ARCH}" &&
      curl -fsSLO "https://github.com/kubernetes-sigs/krew/releases/latest/download/${KREW}.tar.gz" &&
      tar zxvf "${KREW}.tar.gz" &&
      ./"${KREW}" install krew
    )
    export PATH="${KREW_ROOT:-$HOME/.krew}/bin:$PATH"
    echo 'export PATH="${KREW_ROOT:-$HOME/.krew}/bin:$PATH"' >> ~/.bashrc
    echo -e "${GREEN}✓ krew installed${NC}"
else
    echo -e "${GREEN}✓ krew is already installed${NC}"
fi

# Install kubectl-ai
echo -e "${BLUE}Installing kubectl-ai...${NC}"
kubectl krew install ai

echo -e "${GREEN}✓ kubectl-ai installed${NC}"

# Create config directory
mkdir -p ~/.kubectl-ai

# Copy config file
if [ -f "kubectl-ai/config.yaml" ]; then
    cp kubectl-ai/config.yaml ~/.kubectl-ai/config.yaml
    echo -e "${GREEN}✓ Configuration file copied${NC}"
fi

# Test installation
echo -e "\n${BLUE}Testing kubectl-ai...${NC}"
kubectl ai version

echo -e "\n${GREEN}✅ kubectl-ai setup complete!${NC}"

echo -e "\n${BLUE}Try these commands:${NC}"
echo "  kubectl ai 'show me all pods'"
echo "  kubectl ai 'describe the todo-backend deployment'"
echo "  kubectl ai 'check cluster health'"

echo -e "\n${YELLOW}Note:${NC} kubectl-ai uses your OpenAI API key for AI-powered operations"
