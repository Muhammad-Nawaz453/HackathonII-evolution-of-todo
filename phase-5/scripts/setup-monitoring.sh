#!/bin/bash
set -e

echo "=========================================="
echo "  Setting Up Monitoring Stack"
echo "=========================================="
echo ""

# Create monitoring namespace
echo "📦 Creating monitoring namespace..."
kubectl create namespace monitoring --dry-run=client -o yaml | kubectl apply -f -

# Add Helm repositories
echo "📦 Adding Helm repositories..."
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add grafana https://grafana.github.io/helm-charts
helm repo add jaegertracing https://jaegertracing.github.io/helm-charts
helm repo update

# Install Prometheus with Grafana
echo "📦 Installing Prometheus and Grafana (this takes 3-5 minutes)..."
helm upgrade --install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --version 55.0.0 \
  --set prometheus.prometheusSpec.retention=7d \
  --set prometheus.prometheusSpec.storageSpec.volumeClaimTemplate.spec.resources.requests.storage=10Gi \
  --set prometheus.prometheusSpec.serviceMonitorSelectorNilUsesHelmValues=false \
  --set grafana.enabled=true \
  --set grafana.adminPassword=admin \
  --set grafana.persistence.enabled=true \
  --set grafana.persistence.size=5Gi \
  --wait \
  --timeout 10m

echo "✅ Prometheus and Grafana installed"
echo ""

# Install Jaeger
echo "📦 Installing Jaeger..."
helm upgrade --install jaeger jaegertracing/jaeger \
  --namespace monitoring \
  --version 0.71.0 \
  --set provisionDataStore.cassandra=false \
  --set allInOne.enabled=true \
  --set storage.type=memory \
  --set agent.enabled=false \
  --set collector.enabled=false \
  --set query.enabled=false \
  --set allInOne.resources.requests.cpu=200m \
  --set allInOne.resources.requests.memory=256Mi \
  --set allInOne.resources.limits.cpu=500m \
  --set allInOne.resources.limits.memory=512Mi \
  --wait \
  --timeout 5m

echo "✅ Jaeger installed"
echo ""

# Apply Prometheus alert rules
echo "📦 Applying Prometheus alert rules..."
kubectl apply -f ../kubernetes/monitoring/prometheus-rules.yaml

echo "✅ Alert rules applied"
echo ""

# Apply Grafana dashboards
echo "📦 Applying Grafana dashboards..."
kubectl apply -f ../kubernetes/monitoring/grafana-dashboard.yaml

echo "✅ Dashboards applied"
echo ""

# Verify installations
echo "🔍 Verifying monitoring stack..."
kubectl get pods -n monitoring

echo ""
echo "=========================================="
echo "  ✅ Monitoring Stack Setup Complete!"
echo "=========================================="
echo ""
echo "Components Installed:"
echo "  - Prometheus (metrics collection)"
echo "  - Grafana (visualization)"
echo "  - Jaeger (distributed tracing)"
echo "  - Alertmanager (alert routing)"
echo ""
echo "Access Instructions:"
echo ""
echo "Grafana:"
echo "  kubectl port-forward -n monitoring svc/prometheus-grafana 3000:80"
echo "  Open: http://localhost:3000"
echo "  Login: admin / admin"
echo ""
echo "Prometheus:"
echo "  kubectl port-forward -n monitoring svc/prometheus-kube-prometheus-prometheus 9090:9090"
echo "  Open: http://localhost:9090"
echo ""
echo "Jaeger:"
echo "  kubectl port-forward -n monitoring svc/jaeger-query 16686:16686"
echo "  Open: http://localhost:16686"
echo ""
echo "Useful Commands:"
echo "  kubectl get pods -n monitoring"
echo "  kubectl get servicemonitors -n monitoring"
echo "  kubectl get prometheusrules -n monitoring"
echo ""
