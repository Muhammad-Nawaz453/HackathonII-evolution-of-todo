#!/bin/bash
set -e

NAMESPACE="todo-app-prod"
REGISTRY="${REGISTRY:-registry.digitalocean.com/todo-app-registry}"
VERSION="${VERSION:-latest}"

echo "=========================================="
echo "  Deploying Todo App to DOKS"
echo "=========================================="
echo "Namespace: $NAMESPACE"
echo "Registry: $REGISTRY"
echo "Version: $VERSION"
echo ""

# Verify cluster access
if ! kubectl cluster-info &> /dev/null; then
    echo "❌ Error: Cannot access Kubernetes cluster"
    echo "Run: doctl kubernetes cluster kubeconfig save <cluster-name>"
    exit 1
fi

echo "✅ Cluster access verified"
echo ""

# Create namespace
echo "📦 Creating namespace..."
kubectl create namespace "$NAMESPACE" --dry-run=client -o yaml | kubectl apply -f -

# Check if secrets exist
if [ ! -f ../kubernetes/doks/secrets.yaml ]; then
    echo "❌ Error: ../kubernetes/doks/secrets.yaml not found"
    echo ""
    echo "Please create secrets.yaml from secrets.yaml.example:"
    echo "  cp ../kubernetes/doks/secrets.yaml.example ../kubernetes/doks/secrets.yaml"
    echo "  # Edit secrets.yaml with real values"
    echo "  # Add secrets.yaml to .gitignore"
    exit 1
fi

# Apply secrets
echo "🔐 Applying secrets..."
kubectl apply -f ../kubernetes/doks/secrets.yaml

# Deploy Dapr components
echo "📦 Deploying Dapr components..."
kubectl apply -f ../dapr/components/

# Deploy Dapr configuration
echo "📦 Deploying Dapr configuration..."
kubectl apply -f ../dapr/configuration/

# Deploy Redis (for Dapr state store)
echo "📦 Deploying Redis..."
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
helm upgrade --install redis bitnami/redis \
  --namespace "$NAMESPACE" \
  --set auth.password=changeme \
  --set master.persistence.size=2Gi \
  --set replica.replicaCount=1 \
  --set replica.persistence.size=2Gi \
  --wait \
  --timeout 5m

echo "✅ Redis deployed"
echo ""

# Deploy application using Helm
echo "📦 Deploying application with Helm..."
helm upgrade --install todo-app ../helm/todo-app-prod \
  --namespace "$NAMESPACE" \
  --values ../helm/todo-app-prod/values-production.yaml \
  --set backend.image="$REGISTRY/todo-backend:$VERSION" \
  --set frontend.image="$REGISTRY/todo-frontend:$VERSION" \
  --set eventService.image="$REGISTRY/event-service:$VERSION" \
  --wait \
  --timeout 10m

echo "✅ Application deployed"
echo ""

# Wait for rollout
echo "⏳ Waiting for deployments to be ready..."
kubectl rollout status deployment/todo-backend -n "$NAMESPACE" --timeout=5m
kubectl rollout status deployment/todo-frontend -n "$NAMESPACE" --timeout=5m
kubectl rollout status deployment/event-service -n "$NAMESPACE" --timeout=5m

echo "✅ All deployments ready"
echo ""

# Install ingress-nginx if not already installed
if ! kubectl get namespace ingress-nginx &> /dev/null; then
    echo "📦 Installing ingress-nginx controller..."
    helm upgrade --install ingress-nginx ingress-nginx \
      --repo https://kubernetes.github.io/ingress-nginx \
      --namespace ingress-nginx \
      --create-namespace \
      --set controller.service.type=LoadBalancer \
      --set controller.metrics.enabled=true \
      --set controller.podAnnotations."prometheus\.io/scrape"=true \
      --set controller.podAnnotations."prometheus\.io/port"=10254 \
      --wait \
      --timeout 5m

    echo "✅ Ingress controller installed"
    echo ""
fi

# Apply ingress
echo "📦 Applying ingress..."
kubectl apply -f ../kubernetes/doks/ingress.yaml

echo "✅ Ingress applied"
echo ""

# Get ingress URL
echo "⏳ Waiting for load balancer IP (this can take 2-5 minutes)..."
for i in {1..30}; do
    INGRESS_IP=$(kubectl get svc ingress-nginx-controller -n ingress-nginx -o jsonpath='{.status.loadBalancer.ingress[0].ip}' 2>/dev/null || echo "")
    if [ -n "$INGRESS_IP" ]; then
        break
    fi
    echo "  Attempt $i/30: Waiting for IP..."
    sleep 10
done

echo ""
echo "=========================================="
echo "  ✅ Deployment Complete!"
echo "=========================================="
echo ""

if [ -n "$INGRESS_IP" ]; then
    echo "🌐 Application URLs:"
    echo "  Frontend:    http://$INGRESS_IP"
    echo "  Backend API: http://$INGRESS_IP/api"
    echo "  Health:      http://$INGRESS_IP/api/health"
    echo ""
else
    echo "⚠️  Load balancer IP not yet assigned."
    echo "Check status with:"
    echo "  kubectl get svc ingress-nginx-controller -n ingress-nginx -w"
    echo ""
fi

echo "📊 Deployment Status:"
kubectl get pods -n "$NAMESPACE"
echo ""

echo "🔍 Useful Commands:"
echo "  # View pods"
echo "  kubectl get pods -n $NAMESPACE"
echo ""
echo "  # View logs"
echo "  kubectl logs -n $NAMESPACE -l app=todo-backend -f"
echo "  kubectl logs -n $NAMESPACE -l app=event-service -f"
echo ""
echo "  # View Dapr sidecars"
echo "  kubectl logs -n $NAMESPACE <pod-name> -c daprd"
echo ""
echo "  # Check HPA status"
echo "  kubectl get hpa -n $NAMESPACE"
echo ""
echo "  # Access Grafana"
echo "  kubectl port-forward -n monitoring svc/prometheus-grafana 3000:80"
echo ""
