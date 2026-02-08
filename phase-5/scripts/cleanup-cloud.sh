#!/bin/bash
set -e

CLUSTER_NAME="${CLUSTER_NAME:-todo-app-prod}"
REGISTRY_NAME="${REGISTRY_NAME:-todo-app-registry}"

echo "=========================================="
echo "  ⚠️  CLEANUP WARNING"
echo "=========================================="
echo ""
echo "This will DELETE all cloud resources:"
echo "  - DOKS Cluster: $CLUSTER_NAME"
echo "  - Container Registry: $REGISTRY_NAME"
echo "  - Load Balancers (if any)"
echo "  - Persistent Volumes"
echo ""
echo "This action CANNOT be undone!"
echo ""
read -p "Type 'DELETE' to confirm: " CONFIRM

if [ "$CONFIRM" != "DELETE" ]; then
    echo "Aborted."
    exit 0
fi

echo ""
echo "🗑️  Starting cleanup..."
echo ""

# Delete DOKS cluster
echo "🗑️  Deleting DOKS cluster: $CLUSTER_NAME"
if doctl kubernetes cluster delete "$CLUSTER_NAME" --force 2>/dev/null; then
    echo "✅ Cluster deleted"
else
    echo "⚠️  Cluster not found or already deleted"
fi

# Delete container registry
echo "🗑️  Deleting container registry: $REGISTRY_NAME"
if doctl registry delete "$REGISTRY_NAME" --force 2>/dev/null; then
    echo "✅ Registry deleted"
else
    echo "⚠️  Registry not found or already deleted"
fi

# Clean up local kubeconfig
echo "🧹 Cleaning up local kubeconfig..."
kubectl config delete-context "do-$CLUSTER_NAME" 2>/dev/null || true
kubectl config delete-cluster "do-$CLUSTER_NAME" 2>/dev/null || true

echo ""
echo "=========================================="
echo "  ✅ Cleanup Complete!"
echo "=========================================="
echo ""
echo "All resources have been deleted."
echo ""
echo "⚠️  IMPORTANT: Verify in DigitalOcean console that:"
echo "  1. Load balancers are deleted (may take a few minutes)"
echo "  2. Volumes are deleted"
echo "  3. No unexpected charges remain"
echo ""
echo "DigitalOcean Console: https://cloud.digitalocean.com/"
echo ""
