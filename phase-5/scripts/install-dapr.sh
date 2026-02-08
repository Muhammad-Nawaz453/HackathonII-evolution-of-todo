#!/bin/bash
set -e

echo "=========================================="
echo "  Installing Dapr on DOKS"
echo "=========================================="
echo ""

# Check if Dapr CLI is installed
if ! command -v dapr &> /dev/null; then
    echo "📦 Installing Dapr CLI..."
    wget -q https://raw.githubusercontent.com/dapr/cli/master/install/install.sh -O - | /bin/bash
    echo "✅ Dapr CLI installed"
else
    echo "✅ Dapr CLI already installed"
fi
echo ""

# Add Dapr Helm repository
echo "📦 Adding Dapr Helm repository..."
helm repo add dapr https://dapr.github.io/helm-charts/
helm repo update

# Install Dapr
echo "📦 Installing Dapr control plane..."
helm upgrade --install dapr dapr/dapr \
  --namespace dapr-system \
  --create-namespace \
  --version 1.12.0 \
  --set global.ha.enabled=true \
  --set global.ha.replicaCount=3 \
  --set global.logAsJson=true \
  --set global.prometheus.enabled=true \
  --set dapr_placement.logLevel=info \
  --set dapr_sidecar_injector.logLevel=info \
  --set dapr_operator.logLevel=info \
  --wait \
  --timeout 10m

echo "✅ Dapr control plane installed"
echo ""

# Verify Dapr installation
echo "🔍 Verifying Dapr installation..."
dapr status -k

echo ""
echo "=========================================="
echo "  ✅ Dapr Installation Complete!"
echo "=========================================="
echo ""
echo "Dapr Control Plane:"
echo "  Namespace: dapr-system"
echo "  Version: 1.12.0"
echo "  High Availability: Enabled (3 replicas)"
echo ""
echo "Components:"
echo "  - dapr-operator"
echo "  - dapr-sidecar-injector"
echo "  - dapr-sentry"
echo "  - dapr-placement-server"
echo ""
echo "Next Steps:"
echo "  1. Deploy Dapr components: kubectl apply -f ../dapr/components/"
echo "  2. Deploy Dapr configuration: kubectl apply -f ../dapr/configuration/"
echo ""
echo "Useful Commands:"
echo "  dapr status -k"
echo "  kubectl get pods -n dapr-system"
echo "  dapr dashboard -k"
echo ""
