#!/bin/bash
set -e

# Configuration
CLUSTER_NAME="${CLUSTER_NAME:-todo-app-prod}"
REGION="${REGION:-nyc1}"
NODE_SIZE="${NODE_SIZE:-s-2vcpu-4gb}"
NODE_COUNT="${NODE_COUNT:-3}"
REGISTRY_NAME="${REGISTRY_NAME:-todo-app-registry}"

echo "=========================================="
echo "  DOKS Cluster Setup"
echo "=========================================="
echo "Cluster Name: $CLUSTER_NAME"
echo "Region: $REGION"
echo "Node Size: $NODE_SIZE"
echo "Node Count: $NODE_COUNT"
echo "Registry: $REGISTRY_NAME"
echo ""

# Check if doctl is installed
if ! command -v doctl &> /dev/null; then
    echo "❌ Error: doctl is not installed"
    echo "Install from: https://docs.digitalocean.com/reference/doctl/how-to/install/"
    exit 1
fi

# Check if authenticated
if ! doctl account get &> /dev/null; then
    echo "❌ Error: Not authenticated with DigitalOcean"
    echo "Run: doctl auth init"
    exit 1
fi

echo "✅ Prerequisites check passed"
echo ""

# Create DOKS cluster
echo "📦 Creating DOKS cluster (this takes 5-10 minutes)..."
doctl kubernetes cluster create "$CLUSTER_NAME" \
  --region "$REGION" \
  --version latest \
  --size "$NODE_SIZE" \
  --count "$NODE_COUNT" \
  --auto-upgrade=true \
  --surge-upgrade=true \
  --maintenance-window "saturday=02:00" \
  --tag "todo-app,production,phase-5" \
  --wait

echo "✅ Cluster created successfully"
echo ""

# Get cluster ID
CLUSTER_ID=$(doctl kubernetes cluster get "$CLUSTER_NAME" --format ID --no-header)
echo "Cluster ID: $CLUSTER_ID"

# Enable autoscaling
echo "⚙️  Enabling cluster autoscaling (min: 2, max: 5)..."
NODE_POOL_ID=$(doctl kubernetes cluster node-pool list "$CLUSTER_ID" --format ID --no-header)

doctl kubernetes cluster node-pool update "$CLUSTER_ID" "$NODE_POOL_ID" \
  --auto-scale \
  --min-nodes 2 \
  --max-nodes 5

echo "✅ Autoscaling enabled"
echo ""

# Configure kubectl
echo "🔧 Configuring kubectl..."
doctl kubernetes cluster kubeconfig save "$CLUSTER_NAME"

# Verify cluster access
echo "🔍 Verifying cluster access..."
kubectl cluster-info
echo ""
kubectl get nodes
echo ""

# Create container registry
echo "📦 Creating container registry..."
if doctl registry create "$REGISTRY_NAME" --subscription-tier basic --region "$REGION" 2>/dev/null; then
    echo "✅ Registry created: registry.digitalocean.com/$REGISTRY_NAME"
else
    echo "ℹ️  Registry already exists or creation skipped"
fi
echo ""

# Configure Docker to use registry
echo "🔐 Configuring Docker authentication..."
doctl registry login

echo ""
echo "=========================================="
echo "  ✅ DOKS Cluster Setup Complete!"
echo "=========================================="
echo ""
echo "Cluster Details:"
echo "  Name: $CLUSTER_NAME"
echo "  ID: $CLUSTER_ID"
echo "  Region: $REGION"
echo "  Nodes: $NODE_COUNT (autoscale: 2-5)"
echo "  Registry: registry.digitalocean.com/$REGISTRY_NAME"
echo ""
echo "Next Steps:"
echo "  1. Install Kafka:      ./scripts/install-kafka.sh"
echo "  2. Install Dapr:       ./scripts/install-dapr.sh"
echo "  3. Setup Monitoring:   ./scripts/setup-monitoring.sh"
echo "  4. Deploy Application: ./scripts/deploy-production.sh"
echo ""
echo "Useful Commands:"
echo "  kubectl get nodes"
echo "  kubectl get pods --all-namespaces"
echo "  doctl kubernetes cluster list"
echo ""
