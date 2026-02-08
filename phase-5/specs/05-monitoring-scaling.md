# Specification: Monitoring and Scaling

**Feature ID**: 05
**Feature Name**: Monitoring, Observability, and Autoscaling
**Phase**: 5 - Production Cloud Deployment
**Status**: Draft
**Created**: 2026-02-07
**Last Updated**: 2026-02-07

## Purpose

Implement comprehensive monitoring, observability, and autoscaling for the production deployment. Deploy Prometheus for metrics collection, Grafana for visualization, Jaeger for distributed tracing, and configure Horizontal Pod Autoscalers (HPA) for automatic scaling based on resource utilization.

## User Stories

**As an operations engineer**, I want comprehensive monitoring so that I can detect and respond to issues before they impact users.

**As a developer**, I want distributed tracing so that I can debug performance issues across microservices.

**As a platform engineer**, I want autoscaling so that the system automatically handles traffic spikes without manual intervention.

**As a product manager**, I want dashboards showing key metrics so that I can understand system health and usage patterns.

## Acceptance Criteria

### Prometheus Deployment

- [ ] Prometheus deployed in `monitoring` namespace
- [ ] Prometheus scraping metrics from all services
- [ ] Prometheus scraping Kafka metrics
- [ ] Prometheus scraping Dapr metrics
- [ ] Prometheus scraping Kubernetes metrics
- [ ] Prometheus retention configured (7 days)
- [ ] Prometheus accessible via port-forward or ingress

### Grafana Deployment

- [ ] Grafana deployed in `monitoring` namespace
- [ ] Grafana connected to Prometheus data source
- [ ] Pre-configured dashboards for Kubernetes cluster
- [ ] Pre-configured dashboards for Kafka
- [ ] Pre-configured dashboards for Dapr
- [ ] Custom dashboard for application metrics
- [ ] Grafana accessible via port-forward or ingress

### Jaeger Deployment

- [ ] Jaeger deployed in `monitoring` namespace
- [ ] Jaeger collector receiving traces from Dapr
- [ ] Jaeger UI accessible via port-forward or ingress
- [ ] Traces visible for end-to-end requests
- [ ] Traces show all service hops (backend → Kafka → event service)

### Application Metrics

- [ ] Backend exposes `/metrics` endpoint
- [ ] Event service exposes `/metrics` endpoint
- [ ] Custom metrics for task operations (create, update, delete)
- [ ] Custom metrics for event publishing and consumption
- [ ] HTTP request metrics (rate, latency, errors)

### Horizontal Pod Autoscaling

- [ ] HPA configured for backend (target: 70% CPU)
- [ ] HPA configured for frontend (target: 70% CPU)
- [ ] HPA configured for event service (target: 70% CPU)
- [ ] HPA scales up under load
- [ ] HPA scales down when load decreases
- [ ] Min/max replica counts configured

### Alerting

- [ ] Alert rules configured in Prometheus
- [ ] Alerts for high error rate
- [ ] Alerts for high latency
- [ ] Alerts for pod crashes
- [ ] Alerts for Kafka consumer lag
- [ ] Alerts for node resource exhaustion

## Architecture

### Monitoring Stack Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  Monitoring Namespace                       │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                  Prometheus                          │  │
│  │  - Scrapes metrics from all services                 │  │
│  │  - Stores time-series data                           │  │
│  │  - Evaluates alert rules                             │  │
│  └────────────────┬─────────────────────────────────────┘  │
│                   │                                         │
│                   │ Metrics                                 │
│                   │                                         │
│  ┌────────────────▼─────────────────────────────────────┐  │
│  │                  Grafana                             │  │
│  │  - Visualizes metrics                                │  │
│  │  - Pre-built dashboards                              │  │
│  │  - Custom dashboards                                 │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                  Jaeger                              │  │
│  │  - Collector: Receives traces                        │  │
│  │  - Query: Serves UI                                  │  │
│  │  - Storage: In-memory or Cassandra                   │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                           ▲
                           │ Metrics & Traces
                           │
┌──────────────────────────┴──────────────────────────────────┐
│              Application Pods (All Namespaces)              │
│                                                             │
│  Backend Pods → Expose /metrics, Send traces to Jaeger     │
│  Event Service → Expose /metrics, Send traces to Jaeger    │
│  Kafka → Expose JMX metrics                                 │
│  Dapr Sidecars → Expose metrics, Send traces to Jaeger     │
└─────────────────────────────────────────────────────────────┘
```

### Autoscaling Architecture

```
┌─────────────────────────────────────────────────────────────┐
│              Horizontal Pod Autoscaler (HPA)                │
│                                                             │
│  Monitors: CPU/Memory usage from Metrics Server            │
│  Decides: Scale up/down based on target utilization        │
│  Acts: Adjusts replica count in Deployment                 │
└────────────────────┬────────────────────────────────────────┘
                     │
                     │ Scale commands
                     │
┌────────────────────▼────────────────────────────────────────┐
│                  Deployments                                │
│                                                             │
│  Backend: min=2, max=10, target=70% CPU                    │
│  Frontend: min=2, max=8, target=70% CPU                    │
│  Event Service: min=1, max=5, target=70% CPU               │
└─────────────────────────────────────────────────────────────┘
```

## Implementation Details

### 1. Install Prometheus

**File**: `scripts/setup-monitoring.sh`

```bash
#!/bin/bash
set -e

echo "Setting up monitoring stack..."

# Create monitoring namespace
kubectl create namespace monitoring --dry-run=client -o yaml | kubectl apply -f -

# Add Helm repositories
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add grafana https://grafana.github.io/helm-charts
helm repo add jaegertracing https://jaegertracing.github.io/helm-charts
helm repo update

# Install Prometheus
echo "Installing Prometheus..."
helm upgrade --install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --version 55.0.0 \
  --set prometheus.prometheusSpec.retention=7d \
  --set prometheus.prometheusSpec.storageSpec.volumeClaimTemplate.spec.resources.requests.storage=10Gi \
  --set prometheus.prometheusSpec.serviceMonitorSelectorNilUsesHelmValues=false \
  --set grafana.enabled=true \
  --set grafana.adminPassword=admin \
  --wait

# Install Jaeger
echo "Installing Jaeger..."
helm upgrade --install jaeger jaegertracing/jaeger \
  --namespace monitoring \
  --version 0.71.0 \
  --set provisionDataStore.cassandra=false \
  --set allInOne.enabled=true \
  --set storage.type=memory \
  --set agent.enabled=false \
  --set collector.enabled=false \
  --set query.enabled=false \
  --wait

echo "✅ Monitoring stack installed!"
echo ""
echo "Access Grafana:"
echo "  kubectl port-forward -n monitoring svc/prometheus-grafana 3000:80"
echo "  Open http://localhost:3000 (admin/admin)"
echo ""
echo "Access Prometheus:"
echo "  kubectl port-forward -n monitoring svc/prometheus-kube-prometheus-prometheus 9090:9090"
echo "  Open http://localhost:9090"
echo ""
echo "Access Jaeger:"
echo "  kubectl port-forward -n monitoring svc/jaeger-query 16686:16686"
echo "  Open http://localhost:16686"
```

### 2. Prometheus ServiceMonitor for Backend

**File**: `kubernetes/monitoring/backend-servicemonitor.yaml`

```yaml
apiVersion: v1
kind: ServiceMonitor
metadata:
  name: todo-backend
  namespace: todo-app-prod
  labels:
    app: todo-backend
spec:
  selector:
    matchLabels:
      app: todo-backend
  endpoints:
  - port: metrics
    interval: 30s
    path: /metrics
```

### 3. Custom Grafana Dashboard

**File**: `kubernetes/monitoring/grafana-dashboard.yaml`

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: todo-app-dashboard
  namespace: monitoring
  labels:
    grafana_dashboard: "1"
data:
  todo-app-dashboard.json: |
    {
      "dashboard": {
        "title": "Todo App - Production",
        "panels": [
          {
            "title": "API Request Rate",
            "targets": [
              {
                "expr": "rate(http_requests_total{job=\"todo-backend\"}[5m])"
              }
            ]
          },
          {
            "title": "API Latency (p95)",
            "targets": [
              {
                "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket{job=\"todo-backend\"}[5m]))"
              }
            ]
          },
          {
            "title": "Error Rate",
            "targets": [
              {
                "expr": "rate(http_requests_total{job=\"todo-backend\",status=~\"5..\"}[5m])"
              }
            ]
          },
          {
            "title": "Tasks Created",
            "targets": [
              {
                "expr": "rate(tasks_created_total[5m])"
              }
            ]
          },
          {
            "title": "Events Published",
            "targets": [
              {
                "expr": "rate(events_published_total[5m])"
              }
            ]
          },
          {
            "title": "Kafka Consumer Lag",
            "targets": [
              {
                "expr": "kafka_consumergroup_lag{group=\"event-service\"}"
              }
            ]
          },
          {
            "title": "Pod CPU Usage",
            "targets": [
              {
                "expr": "rate(container_cpu_usage_seconds_total{namespace=\"todo-app-prod\"}[5m])"
              }
            ]
          },
          {
            "title": "Pod Memory Usage",
            "targets": [
              {
                "expr": "container_memory_usage_bytes{namespace=\"todo-app-prod\"}"
              }
            ]
          }
        ]
      }
    }
```

### 4. Prometheus Alert Rules

**File**: `kubernetes/monitoring/prometheus-rules.yaml`

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: todo-app-alerts
  namespace: monitoring
  labels:
    prometheus: kube-prometheus
spec:
  groups:
  - name: todo-app
    interval: 30s
    rules:
    - alert: HighErrorRate
      expr: |
        rate(http_requests_total{job="todo-backend",status=~"5.."}[5m]) > 0.05
      for: 5m
      labels:
        severity: critical
      annotations:
        summary: "High error rate in backend API"
        description: "Backend API error rate is {{ $value }} (>5%)"

    - alert: HighAPILatency
      expr: |
        histogram_quantile(0.95, rate(http_request_duration_seconds_bucket{job="todo-backend"}[5m])) > 1
      for: 5m
      labels:
        severity: warning
      annotations:
        summary: "High API latency"
        description: "API p95 latency is {{ $value }}s (>1s)"

    - alert: PodCrashLooping
      expr: |
        rate(kube_pod_container_status_restarts_total{namespace="todo-app-prod"}[15m]) > 0
      for: 5m
      labels:
        severity: critical
      annotations:
        summary: "Pod is crash looping"
        description: "Pod {{ $labels.pod }} is restarting frequently"

    - alert: HighKafkaConsumerLag
      expr: |
        kafka_consumergroup_lag{group="event-service"} > 1000
      for: 5m
      labels:
        severity: warning
      annotations:
        summary: "High Kafka consumer lag"
        description: "Consumer lag is {{ $value }} messages (>1000)"

    - alert: NodeMemoryPressure
      expr: |
        kube_node_status_condition{condition="MemoryPressure",status="true"} == 1
      for: 5m
      labels:
        severity: warning
      annotations:
        summary: "Node under memory pressure"
        description: "Node {{ $labels.node }} is under memory pressure"

    - alert: PodMemoryUsageHigh
      expr: |
        container_memory_usage_bytes{namespace="todo-app-prod"} / container_spec_memory_limit_bytes{namespace="todo-app-prod"} > 0.9
      for: 5m
      labels:
        severity: warning
      annotations:
        summary: "Pod memory usage is high"
        description: "Pod {{ $labels.pod }} memory usage is {{ $value }}% (>90%)"
```

### 5. Horizontal Pod Autoscaler

**File**: `helm/todo-app-prod/templates/hpa.yaml`

```yaml
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: todo-backend-hpa
  namespace: {{ .Values.namespace }}
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: todo-backend
  minReplicas: {{ .Values.backend.autoscaling.minReplicas }}
  maxReplicas: {{ .Values.backend.autoscaling.maxReplicas }}
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: {{ .Values.backend.autoscaling.targetCPU }}
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: {{ .Values.backend.autoscaling.targetMemory }}
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Percent
        value: 100
        periodSeconds: 30
      - type: Pods
        value: 2
        periodSeconds: 30
      selectPolicy: Max
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: todo-frontend-hpa
  namespace: {{ .Values.namespace }}
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: todo-frontend
  minReplicas: {{ .Values.frontend.autoscaling.minReplicas }}
  maxReplicas: {{ .Values.frontend.autoscaling.maxReplicas }}
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: {{ .Values.frontend.autoscaling.targetCPU }}
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
    scaleUp:
      stabilizationWindowSeconds: 0
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: event-service-hpa
  namespace: {{ .Values.namespace }}
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: event-service
  minReplicas: {{ .Values.eventService.autoscaling.minReplicas }}
  maxReplicas: {{ .Values.eventService.autoscaling.maxReplicas }}
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: {{ .Values.eventService.autoscaling.targetCPU }}
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
    scaleUp:
      stabilizationWindowSeconds: 0
```

### 6. Backend Metrics Endpoint

**File**: `backend/src/metrics.py` (new)

```python
"""Prometheus metrics for the backend API."""

from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from fastapi import Response
import time

# HTTP metrics
http_requests_total = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

http_request_duration_seconds = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint']
)

# Task metrics
tasks_created_total = Counter(
    'tasks_created_total',
    'Total tasks created'
)

tasks_updated_total = Counter(
    'tasks_updated_total',
    'Total tasks updated'
)

tasks_deleted_total = Counter(
    'tasks_deleted_total',
    'Total tasks deleted'
)

tasks_completed_total = Counter(
    'tasks_completed_total',
    'Total tasks marked as completed'
)

# Event metrics
events_published_total = Counter(
    'events_published_total',
    'Total events published',
    ['event_type', 'success']
)

events_publish_duration_seconds = Histogram(
    'events_publish_duration_seconds',
    'Event publishing duration in seconds',
    ['event_type']
)

# Database metrics
db_connections_active = Gauge(
    'db_connections_active',
    'Active database connections'
)

db_query_duration_seconds = Histogram(
    'db_query_duration_seconds',
    'Database query duration in seconds',
    ['query_type']
)


def metrics_endpoint():
    """Expose metrics for Prometheus scraping."""
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)


class MetricsMiddleware:
    """Middleware to track HTTP request metrics."""

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        method = scope["method"]
        path = scope["path"]

        # Skip metrics endpoint itself
        if path == "/metrics":
            return await self.app(scope, receive, send)

        start_time = time.time()

        async def send_wrapper(message):
            if message["type"] == "http.response.start":
                status = message["status"]
                duration = time.time() - start_time

                http_requests_total.labels(
                    method=method,
                    endpoint=path,
                    status=status
                ).inc()

                http_request_duration_seconds.labels(
                    method=method,
                    endpoint=path
                ).observe(duration)

            await send(message)

        await self.app(scope, receive, send_wrapper)
```

**Add to `backend/src/main.py`**:

```python
from src.metrics import metrics_endpoint, MetricsMiddleware
from src.metrics import (
    tasks_created_total,
    tasks_updated_total,
    tasks_deleted_total,
    tasks_completed_total
)

# Add middleware
app.add_middleware(MetricsMiddleware)

# Add metrics endpoint
@app.get("/metrics")
async def metrics():
    return metrics_endpoint()

# Increment metrics in route handlers
@app.post("/tasks")
async def create_task(...):
    # ... existing code ...
    tasks_created_total.inc()
    # ... rest of code ...
```

### 7. Load Testing Script (Optional)

**File**: `scripts/load-test.sh`

```bash
#!/bin/bash
set -e

# Simple load test using Apache Bench
# Install: apt-get install apache2-utils

BACKEND_URL="${BACKEND_URL:-http://localhost:8000}"
REQUESTS="${REQUESTS:-1000}"
CONCURRENCY="${CONCURRENCY:-10}"

echo "Load testing backend API..."
echo "URL: $BACKEND_URL"
echo "Requests: $REQUESTS"
echo "Concurrency: $CONCURRENCY"
echo ""

# Test GET /tasks
echo "Testing GET /tasks..."
ab -n "$REQUESTS" -c "$CONCURRENCY" "$BACKEND_URL/api/tasks"

# Test POST /tasks (requires JSON payload)
echo ""
echo "Testing POST /tasks..."
ab -n "$REQUESTS" -c "$CONCURRENCY" \
   -p <(echo '{"title":"Load test task","description":"Testing"}') \
   -T "application/json" \
   "$BACKEND_URL/api/tasks"

echo ""
echo "Load test complete!"
echo "Check Grafana dashboards for metrics."
```

## Edge Cases and Error Handling

### Metrics Server Unavailable

- **Scenario**: Metrics server is down, HPA cannot scale
- **Handling**: HPA maintains current replica count
- **Recovery**: Automatic when metrics server restarts
- **Prevention**: Deploy metrics server with high availability

### Prometheus Storage Full

- **Scenario**: Prometheus runs out of disk space
- **Handling**: Prometheus stops accepting new metrics
- **Recovery**: Increase PVC size or reduce retention
- **Prevention**: Monitor disk usage, set appropriate retention

### Grafana Dashboard Not Loading

- **Scenario**: Grafana cannot connect to Prometheus
- **Handling**: Check Prometheus service endpoint
- **Recovery**: Reconfigure data source in Grafana
- **Verification**: Test connection in Grafana settings

### Jaeger Traces Not Appearing

- **Scenario**: Traces not visible in Jaeger UI
- **Handling**: Check Dapr tracing configuration
- **Recovery**: Verify Jaeger collector endpoint in Dapr config
- **Debugging**: Check Dapr sidecar logs for tracing errors

## Testing Strategy

### Monitoring Tests

- [ ] Verify Prometheus is scraping all targets
- [ ] Verify Grafana can query Prometheus
- [ ] Verify Jaeger is receiving traces
- [ ] Verify custom metrics are exposed
- [ ] Verify alert rules are loaded

### Autoscaling Tests

- [ ] Generate load to trigger scale-up
- [ ] Verify HPA increases replica count
- [ ] Remove load and verify scale-down
- [ ] Verify min/max replica limits are respected
- [ ] Test scale-up/down behavior and timing

### Alert Tests

- [ ] Trigger high error rate alert
- [ ] Trigger high latency alert
- [ ] Trigger pod crash alert
- [ ] Verify alerts appear in Prometheus
- [ ] Verify alert notifications (if configured)

## Monitoring and Metrics

### Key Metrics to Monitor

**Application Metrics:**
- `http_requests_total`: Total HTTP requests by method, endpoint, status
- `http_request_duration_seconds`: Request latency histogram
- `tasks_created_total`: Total tasks created
- `events_published_total`: Total events published
- `events_publish_duration_seconds`: Event publishing latency

**Infrastructure Metrics:**
- `kube_pod_status_phase`: Pod status (Running, Pending, Failed)
- `kube_pod_container_status_restarts_total`: Container restart count
- `container_cpu_usage_seconds_total`: CPU usage
- `container_memory_usage_bytes`: Memory usage
- `kube_node_status_condition`: Node health status

**Kafka Metrics:**
- `kafka_server_brokertopicmetrics_messagesinpersec`: Message rate
- `kafka_consumergroup_lag`: Consumer lag
- `kafka_server_replicamanager_underreplicatedpartitions`: Under-replicated partitions

**Dapr Metrics:**
- `dapr_component_pubsub_egress_count`: Pub/sub messages sent
- `dapr_component_pubsub_ingress_count`: Pub/sub messages received
- `dapr_http_server_request_count`: Dapr HTTP requests

### Grafana Dashboards

1. **Kubernetes Cluster Dashboard** (pre-built)
   - Node CPU/memory usage
   - Pod count and status
   - Network traffic
   - Persistent volume usage

2. **Kafka Dashboard** (pre-built)
   - Broker health
   - Topic throughput
   - Consumer lag
   - Partition distribution

3. **Dapr Dashboard** (pre-built)
   - Service invocation metrics
   - Pub/sub metrics
   - State store operations
   - Sidecar resource usage

4. **Todo App Dashboard** (custom)
   - API request rate and latency
   - Task operation metrics
   - Event publishing metrics
   - Error rate
   - Pod resource usage

## Performance Requirements

- Prometheus scrapes metrics every 30 seconds
- Grafana dashboards load within 2 seconds
- Jaeger traces appear within 10 seconds
- HPA scales up within 2 minutes of load increase
- HPA scales down within 5 minutes of load decrease
- Metrics retention: 7 days

## Security Considerations

- Grafana admin password changed from default
- Prometheus accessible only within cluster (or via ingress with auth)
- Jaeger UI accessible only within cluster (or via ingress with auth)
- Metrics endpoints do not expose sensitive data
- RBAC configured for monitoring namespace

## Cost Optimization

- Use in-memory storage for Jaeger (demo only)
- Set Prometheus retention to 7 days
- Use sampling for Jaeger traces (not 100%)
- Right-size monitoring pod resources
- Consider managed monitoring services for production

## Rollout Plan

1. Install Prometheus with kube-prometheus-stack
2. Install Jaeger
3. Configure Dapr tracing to use Jaeger
4. Add metrics endpoints to backend and event service
5. Create ServiceMonitors for applications
6. Import Grafana dashboards
7. Configure Prometheus alert rules
8. Deploy Horizontal Pod Autoscalers
9. Test autoscaling with load
10. Verify traces in Jaeger

## Success Metrics

- Prometheus scraping all targets successfully
- Grafana dashboards showing real-time metrics
- Jaeger showing distributed traces
- Custom application metrics visible
- HPA scaling pods based on load
- Alerts firing correctly when thresholds exceeded
- No performance degradation from monitoring overhead

## Troubleshooting Guide

### Prometheus Not Scraping Targets

```bash
# Check Prometheus targets
kubectl port-forward -n monitoring svc/prometheus-kube-prometheus-prometheus 9090:9090
# Open http://localhost:9090/targets

# Check ServiceMonitor
kubectl get servicemonitor -n todo-app-prod

# Check if metrics endpoint is accessible
kubectl exec -n todo-app-prod <pod-name> -- curl localhost:8000/metrics
```

### HPA Not Scaling

```bash
# Check HPA status
kubectl get hpa -n todo-app-prod

# Check metrics server
kubectl top nodes
kubectl top pods -n todo-app-prod

# Describe HPA for details
kubectl describe hpa todo-backend-hpa -n todo-app-prod
```

### Jaeger Not Showing Traces

```bash
# Check Dapr tracing configuration
kubectl get configuration -n todo-app-prod

# Check Dapr sidecar logs
kubectl logs -n todo-app-prod <pod-name> -c daprd

# Verify Jaeger collector is running
kubectl get pods -n monitoring -l app=jaeger
```

## Dependencies

- Prometheus Operator (kube-prometheus-stack)
- Grafana
- Jaeger
- Metrics Server (for HPA)
- Dapr (for distributed tracing)

## Future Enhancements

- Alertmanager for alert routing and notifications
- Slack/Discord integration for alerts
- Long-term metrics storage (Thanos, Cortex)
- Custom metrics for autoscaling (e.g., queue depth)
- SLO/SLI tracking and error budgets
- Distributed tracing with sampling strategies
- Log aggregation with Loki or ELK

---

**Specification Version**: 1.0
**Approved By**: [Pending]
**Implementation Status**: Not Started
