#!/bin/bash
set -e

echo "🧠 Setting up kagent..."

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Check prerequisites
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

# Download kagent binary
echo -e "${BLUE}Downloading kagent...${NC}"
curl -LO https://github.com/kagent-io/kagent/releases/latest/download/kagent-linux-amd64

# Make executable
chmod +x kagent-linux-amd64

# Move to PATH
sudo mv kagent-linux-amd64 /usr/local/bin/kagent

echo -e "${GREEN}✓ kagent installed${NC}"

# Verify installation
kagent version

# Create configuration directory
mkdir -p ~/.kagent

# Copy config file
if [ -f "kagent/config.yaml" ]; then
    cp kagent/config.yaml ~/.kagent/config.yaml
    echo -e "${GREEN}✓ Configuration file copied${NC}"
fi

# Start kagent in background
echo -e "\n${BLUE}Starting kagent...${NC}"
kagent start --config ~/.kagent/config.yaml --daemon

# Wait for agent to start
sleep 5

# Check status
kagent status

echo -e "\n${GREEN}✅ kagent setup complete!${NC}"

echo -e "\n${BLUE}Useful commands:${NC}"
echo "  kagent status              # Check agent status"
echo "  kagent analyze cluster     # Analyze cluster health"
echo "  kagent recommend           # Get recommendations"
echo "  kagent auto-heal history   # View remediation history"
echo "  kagent logs --follow       # View agent logs"

echo -e "\n${YELLOW}Note:${NC} kagent is now monitoring your cluster autonomously"
