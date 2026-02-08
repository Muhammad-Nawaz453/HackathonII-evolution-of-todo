# Specification: Dapr Setup and Integration

**Feature ID**: 03
**Feature Name**: Dapr Setup and Integration
**Phase**: 5 - Production Cloud Deployment
**Status**: Draft
**Created**: 2026-02-07
**Last Updated**: 2026-02-07

## Purpose

Deploy Dapr (Distributed Application Runtime) on DOKS to provide microservices building blocks including pub/sub, state management, service invocation, and distributed tracing. Integrate Dapr with the backend and event services to simplify distributed systems development.

## User Stories

**As a developer**, I want Dapr to handle pub/sub complexity so that I can publish and consume events without managing Kafka clients directly.

**As a platform engineer**, I want Dapr sidecars to provide observability so that I can trace requests across services automatically.

**As an operations engineer**, I want Dapr to handle retries and circuit breaking so that the system is resilient to transient failures.

**As a security engineer**, I want Dapr to manage secrets so that applications don't access Kubernetes secrets directly.

## Acceptance Criteria

### Dapr Installation

- [ ] Dapr control plane installed in `dapr-system` namespace
- [ ] Dapr operator, sidecar injector, and placement service running
- [ ] Dapr dashboard accessible for debugging
- [ ] Dapr CLI installed for local development and testing

### Dapr Components

- [ ] Pub/Sub component configured to use Kafka
- [ ] State store component configured to use Redis
- [ ] Secret store component configured to use Kubernetes secrets
- [ ] Components deployed to appropriate namespaces

### Backend Integration

- [ ] Backend deployment has Dapr sidecar injected
- [ ] Backend publishes events via Dapr pub/sub API
- [ ] Backend accesses secrets via Dapr secrets API
- [ ] Backend exposes metrics for Dapr sidecar

### Event Service Integration

- [ ] Event service deployment has Dapr sidecar injected
- [ ] Event service subscribes to topics via Dapr
- [ ] Event service processes events idempotently
- [ ] Event service handles subscription errors gracefully

### Distributed Tracing

- [ ] Dapr tracing configured to use Jaeger
- [ ] Traces visible in Jaeger UI
- [ ] Traces include all service hops (backend → Kafka → event service)
- [ ] Correlation IDs propagated across services

## Architecture

### Dapr Sidecar Pattern

```
┌─────────────────────────────────────────────────┐
│                  Pod                            │
│                                                 │
│  ┌──────────────────┐    ┌──────────────────┐  │
│  │   Application    │◄──►│  Dapr Sidecar    │  │
│  │   Container      │    │                  │  │
│  │                  │    │  - Pub/Sub       │  │
│  │  (Backend API)   │    │  - State Store   │  │
│  │                  │    │  - Secrets       │  │
│  │                  │    │  - Tracing       │  │
│  └──────────────────┘    └──────────────────┘  │
│         │                         │             │
│         │                         │             │
└─────────┼─────────────────────────┼─────────────┘
          │                         │
          │                         ▼
          │                  Dapr Control Plane
          │                  (dapr-system)
          │
          ▼
    External Services
    (Database, etc.)
```

### Dapr Components Architecture

```
Backend API Pod                Event Service Pod
┌─────────────┐               ┌─────────────┐
│  Backend    │               │   Event     │
│  Container  │               │  Container  │
└──────┬──────┘               └──────┬──────┘
       │                             │
       │ HTTP/gRPC                   │ HTTP/gRPC
       │                             │
┌──────▼──────┐               ┌──────▼──────┐
│    Dapr     │               │    Dapr     │
│   Sidecar   │               │   Sidecar   │
└──────┬──────┘               └──────┬──────┘
       │                             │
       │                             │
       └──────────┬──────────────────┘
                  │
                  ▼
         ┌────────────────┐
         │ Dapr Pub/Sub   │
         │  Component     │
         │   (Kafka)      │
         └────────┬───────┘
                  │
                  ▼
         ┌────────────────┐
         │ Kafka Cluster  │
         └────────────────┘
```

## Implementation Details

### 1. Install Dapr

**File**: `scripts/install-dapr.sh`

```bash
#!/bin/bash
set -e

echo "Installing Dapr on DOKS..."

# Install Dapr CLI (if not already installed)
if ! command -v dapr &> /dev/null; then
    echo "Installing Dapr CLI..."
    wget -q https://raw.githubusercontent.com/dapr/cli/master/install/install.sh -O - | /bin/bash
fi

# Initialize Dapr on Kubernetes
echo "Initializing Dapr on Kubernetes..."
dapr init --kubernetes --wait --timeout 600

# Verify Dapr installation
echo "Verifying Dapr installation..."
dapr status -k

# Install Dapr dashboard
echo "Installing Dapr dashboard..."
kubectl apply -f https://raw.githubusercontent.com/dapr/dapr/master/charts/dapr/charts/dapr_dashboard/templates/dashboard.yaml

echo "Dapr installed successfully!"
echo ""
echo "To access Dapr dashboard:"
echo "  kubectl port-forward svc/dapr-dashboard -n dapr-system 8080:8080"
echo "  Open http://localhost:8080"
```

Alternative using Helm:

```bash
#!/bin/bash
set -e

echo "Installing Dapr using Helm..."

# Add Dapr Helm repository
helm repo add dapr https://dapr.github.io/helm-charts/
helm repo update

# Install Dapr
helm upgrade --install dapr dapr/dapr \
  --namespace dapr-system \
  --create-namespace \
  --version 1.12.0 \
  --set global.ha.enabled=true \
  --set global.ha.replicaCount=3 \
  --set global.logAsJson=true \
  --set global.prometheus.enabled=true \
  --wait

echo "Dapr installed successfully!"
```

### 2. Dapr Pub/Sub Component (Kafka)

**File**: `dapr/components/pubsub.yaml`

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: kafka-pubsub
  namespace: todo-app-prod
spec:
  type: pubsub.kafka
  version: v1
  metadata:
  - name: brokers
    value: "todo-kafka-kafka-bootstrap.kafka.svc.cluster.local:9092"
  - name: consumerGroup
    value: "todo-app"
  - name: clientId
    value: "todo-backend"
  - name: authType
    value: "none"
  - name: maxMessageBytes
    value: "1024000"
  - name: consumeRetryInterval
    value: "200ms"
  - name: version
    value: "3.6.0"
scopes:
- todo-backend
- event-service
```

### 3. Dapr State Store Component (Redis)

**File**: `dapr/components/statestore.yaml`

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: statestore
  namespace: todo-app-prod
spec:
  type: state.redis
  version: v1
  metadata:
  - name: redisHost
    value: redis-master.todo-app-prod.svc.cluster.local:6379
  - name: redisPassword
    secretKeyRef:
      name: redis-secret
      key: password
  - name: enableTLS
    value: "false"
  - name: maxRetries
    value: "3"
  - name: maxRetryBackoff
    value: "2s"
scopes:
- todo-backend
- event-service
---
apiVersion: v1
kind: Secret
metadata:
  name: redis-secret
  namespace: todo-app-prod
type: Opaque
stringData:
  password: "changeme"  # Change in production!
```

### 4. Dapr Secret Store Component

**File**: `dapr/components/secretstore.yaml`

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: kubernetes-secrets
  namespace: todo-app-prod
spec:
  type: secretstores.kubernetes
  version: v1
  metadata: []
scopes:
- todo-backend
- event-service
```

### 5. Dapr Configuration (Tracing)

**File**: `dapr/configuration/tracing.yaml`

```yaml
apiVersion: dapr.io/v1alpha1
kind: Configuration
metadata:
  name: tracing-config
  namespace: todo-app-prod
spec:
  tracing:
    samplingRate: "1"  # 100% sampling for demo (reduce in production)
    zipkin:
      endpointAddress: "http://jaeger-collector.monitoring.svc.cluster.local:9411/api/v2/spans"
  metric:
    enabled: true
  mtls:
    enabled: false  # Enable in production
    workloadCertTTL: "24h"
    allowedClockSkew: "15m"
```

### 6. Dapr Subscription (Event Service)

**File**: `dapr/subscriptions/task-events.yaml`

```yaml
apiVersion: dapr.io/v2alpha1
kind: Subscription
metadata:
  name: task-events-subscription
  namespace: todo-app-prod
spec:
  pubsubname: kafka-pubsub
  topic: todo.tasks.created
  routes:
    default: /events/task-created
  scopes:
  - event-service
---
apiVersion: dapr.io/v2alpha1
kind: Subscription
metadata:
  name: task-updated-subscription
  namespace: todo-app-prod
spec:
  pubsubname: kafka-pubsub
  topic: todo.tasks.updated
  routes:
    default: /events/task-updated
  scopes:
  - event-service
---
apiVersion: dapr.io/v2alpha1
kind: Subscription
metadata:
  name: task-deleted-subscription
  namespace: todo-app-prod
spec:
  pubsubname: kafka-pubsub
  topic: todo.tasks.deleted
  routes:
    default: /events/task-deleted
  scopes:
  - event-service
---
apiVersion: dapr.io/v2alpha1
kind: Subscription
metadata:
  name: task-completed-subscription
  namespace: todo-app-prod
spec:
  pubsubname: kafka-pubsub
  topic: todo.tasks.completed
  routes:
    default: /events/task-completed
  scopes:
  - event-service
```

### 7. Backend Deployment with Dapr Sidecar

**File**: `helm/todo-app-prod/templates/backend-dapr.yaml`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: todo-backend
  namespace: {{ .Values.namespace }}
  labels:
    app: todo-backend
spec:
  replicas: {{ .Values.backend.replicas }}
  selector:
    matchLabels:
      app: todo-backend
  template:
    metadata:
      labels:
        app: todo-backend
      annotations:
        dapr.io/enabled: "true"
        dapr.io/app-id: "todo-backend"
        dapr.io/app-port: "8000"
        dapr.io/enable-api-logging: "true"
        dapr.io/log-level: "info"
        dapr.io/config: "tracing-config"
        dapr.io/sidecar-cpu-request: "100m"
        dapr.io/sidecar-memory-request: "128Mi"
        dapr.io/sidecar-cpu-limit: "200m"
        dapr.io/sidecar-memory-limit: "256Mi"
    spec:
      containers:
      - name: backend
        image: {{ .Values.backend.image }}
        ports:
        - containerPort: 8000
          name: http
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: database-secret
              key: url
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: openai-secret
              key: api-key
        - name: DAPR_HTTP_PORT
          value: "3500"
        - name: DAPR_GRPC_PORT
          value: "50001"
        resources:
          requests:
            cpu: {{ .Values.backend.resources.requests.cpu }}
            memory: {{ .Values.backend.resources.requests.memory }}
          limits:
            cpu: {{ .Values.backend.resources.limits.cpu }}
            memory: {{ .Values.backend.resources.limits.memory }}
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 5
```

### 8. Backend Code - Dapr Client

**File**: `backend/src/dapr_client.py` (new)

```python
"""Dapr client for pub/sub and state management."""

from dapr.clients import DaprClient
from dapr.clients.grpc._response import TopicEventResponse
from typing import Dict, Any, Optional
import logging
import json
import uuid
from datetime import datetime

logger = logging.getLogger(__name__)


class DaprEventPublisher:
    """Publishes events to Kafka via Dapr pub/sub."""

    def __init__(self, pubsub_name: str = "kafka-pubsub"):
        self.pubsub_name = pubsub_name
        self.source = "todo-backend"

    async def publish_event(
        self,
        topic: str,
        event_type: str,
        payload: Dict[str, Any],
        correlation_id: Optional[str] = None,
    ) -> bool:
        """
        Publish event to Kafka via Dapr.

        Args:
            topic: Kafka topic name (e.g., "todo.tasks.created")
            event_type: Event type (e.g., "task.created")
            payload: Event payload
            correlation_id: Optional correlation ID for tracing

        Returns:
            True if published successfully, False otherwise
        """
        try:
            event = {
                "event_id": str(uuid.uuid4()),
                "event_type": event_type,
                "event_version": "v1",
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "correlation_id": correlation_id or str(uuid.uuid4()),
                "source": self.source,
                "payload": payload,
            }

            with DaprClient() as client:
                client.publish_event(
                    pubsub_name=self.pubsub_name,
                    topic_name=topic,
                    data=json.dumps(event),
                    data_content_type="application/json",
                )

            logger.info(
                f"Published event {event_type} to {topic}",
                extra={
                    "event_id": event["event_id"],
                    "correlation_id": event["correlation_id"],
                },
            )
            return True

        except Exception as e:
            logger.error(
                f"Failed to publish event {event_type} to {topic}: {e}",
                exc_info=True,
            )
            return False


class DaprStateManager:
    """Manages state using Dapr state store (Redis)."""

    def __init__(self, store_name: str = "statestore"):
        self.store_name = store_name

    async def save_state(self, key: str, value: Any) -> bool:
        """Save state to Redis via Dapr."""
        try:
            with DaprClient() as client:
                client.save_state(
                    store_name=self.store_name,
                    key=key,
                    value=json.dumps(value),
                )
            logger.info(f"Saved state for key: {key}")
            return True
        except Exception as e:
            logger.error(f"Failed to save state for key {key}: {e}")
            return False

    async def get_state(self, key: str) -> Optional[Any]:
        """Get state from Redis via Dapr."""
        try:
            with DaprClient() as client:
                response = client.get_state(
                    store_name=self.store_name,
                    key=key,
                )
            if response.data:
                return json.loads(response.data)
            return None
        except Exception as e:
            logger.error(f"Failed to get state for key {key}: {e}")
            return None

    async def delete_state(self, key: str) -> bool:
        """Delete state from Redis via Dapr."""
        try:
            with DaprClient() as client:
                client.delete_state(
                    store_name=self.store_name,
                    key=key,
                )
            logger.info(f"Deleted state for key: {key}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete state for key {key}: {e}")
            return False
```

### 9. Event Service with Dapr

**File**: `backend-event-service/src/main.py`

```python
"""Event service that consumes events from Kafka via Dapr."""

from fastapi import FastAPI, Request
from cloudevents.http import from_http
import logging
import json

app = FastAPI(title="Event Service", version="1.0.0")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.post("/events/task-created")
async def handle_task_created(request: Request):
    """Handle task.created events."""
    try:
        # Parse CloudEvent
        event = from_http(request.headers, await request.body())

        data = json.loads(event.data)
        logger.info(f"Received task.created event: {data}")

        # Process event (analytics, audit, notifications, etc.)
        task_id = data["payload"]["task_id"]
        title = data["payload"]["title"]

        logger.info(f"Processing task creation: ID={task_id}, Title={title}")

        # TODO: Store in analytics database, send notifications, etc.

        return {"success": True}

    except Exception as e:
        logger.error(f"Error handling task.created event: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


@app.post("/events/task-updated")
async def handle_task_updated(request: Request):
    """Handle task.updated events."""
    try:
        event = from_http(request.headers, await request.body())
        data = json.loads(event.data)
        logger.info(f"Received task.updated event: {data}")

        # Process event
        task_id = data["payload"]["task_id"]
        changes = data["payload"].get("changes", {})

        logger.info(f"Processing task update: ID={task_id}, Changes={changes}")

        return {"success": True}

    except Exception as e:
        logger.error(f"Error handling task.updated event: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


@app.post("/events/task-deleted")
async def handle_task_deleted(request: Request):
    """Handle task.deleted events."""
    try:
        event = from_http(request.headers, await request.body())
        data = json.loads(event.data)
        logger.info(f"Received task.deleted event: {data}")

        task_id = data["payload"]["task_id"]
        logger.info(f"Processing task deletion: ID={task_id}")

        return {"success": True}

    except Exception as e:
        logger.error(f"Error handling task.deleted event: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


@app.post("/events/task-completed")
async def handle_task_completed(request: Request):
    """Handle task.completed events."""
    try:
        event = from_http(request.headers, await request.body())
        data = json.loads(event.data)
        logger.info(f"Received task.completed event: {data}")

        task_id = data["payload"]["task_id"]
        logger.info(f"Processing task completion: ID={task_id}")

        return {"success": True}

    except Exception as e:
        logger.error(f"Error handling task.completed event: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy", "service": "event-service"}


@app.get("/dapr/subscribe")
async def subscribe():
    """Dapr subscription endpoint."""
    subscriptions = [
        {
            "pubsubname": "kafka-pubsub",
            "topic": "todo.tasks.created",
            "route": "/events/task-created",
        },
        {
            "pubsubname": "kafka-pubsub",
            "topic": "todo.tasks.updated",
            "route": "/events/task-updated",
        },
        {
            "pubsubname": "kafka-pubsub",
            "topic": "todo.tasks.deleted",
            "route": "/events/task-deleted",
        },
        {
            "pubsubname": "kafka-pubsub",
            "topic": "todo.tasks.completed",
            "route": "/events/task-completed",
        },
    ]
    return subscriptions


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
```

## Edge Cases and Error Handling

### Dapr Sidecar Not Ready

- **Scenario**: Application starts before Dapr sidecar is ready
- **Handling**: Use init containers or readiness probes with delay
- **Recovery**: Kubernetes restarts pod if health checks fail

### Pub/Sub Component Unavailable

- **Scenario**: Kafka cluster is down
- **Handling**: Dapr retries with exponential backoff
- **Fallback**: Log error, continue serving API requests
- **Monitoring**: Alert on high pub/sub error rate

### State Store Unavailable

- **Scenario**: Redis is down
- **Handling**: Degrade gracefully, serve from database
- **Recovery**: Automatic when Redis comes back
- **Monitoring**: Alert on state store errors

### Event Delivery Failures

- **Scenario**: Event service is down or slow
- **Handling**: Dapr retries delivery, Kafka retains messages
- **Recovery**: Event service catches up when healthy
- **Monitoring**: Monitor consumer lag

## Testing Strategy

### Unit Tests

- Test Dapr client wrapper functions
- Test event serialization and deserialization
- Mock Dapr API responses

### Integration Tests

- Test pub/sub flow end-to-end
- Test state store operations
- Test secret retrieval
- Test distributed tracing

### Resilience Tests

- Kill Dapr sidecar, verify pod restarts
- Simulate Kafka unavailability
- Simulate Redis unavailability
- Test retry and circuit breaker behavior

## Monitoring and Metrics

### Dapr Metrics

- `dapr_http_server_request_count`: HTTP requests to Dapr sidecar
- `dapr_grpc_io_server_completed_rpcs`: gRPC calls completed
- `dapr_component_pubsub_ingress_count`: Pub/sub messages received
- `dapr_component_pubsub_egress_count`: Pub/sub messages sent
- `dapr_component_state_count`: State operations count

### Alerts

```yaml
- alert: DaprSidecarDown
  expr: up{job="dapr-sidecar"} == 0
  for: 2m
  annotations:
    summary: "Dapr sidecar is down"

- alert: DaprPubSubErrors
  expr: rate(dapr_component_pubsub_egress_count{success="false"}[5m]) > 0.05
  for: 5m
  annotations:
    summary: "High Dapr pub/sub error rate"
```

## Performance Requirements

- Dapr sidecar adds < 5ms latency to pub/sub operations
- State store operations complete in < 10ms (p95)
- Dapr sidecar uses < 200m CPU, < 256Mi memory
- System handles 1000 pub/sub operations/second

## Security Considerations

- mTLS between Dapr sidecars (enable in production)
- Secrets never exposed to application code
- Component scoping restricts access
- API token authentication for Dapr API (optional)

## Rollout Plan

1. Install Dapr control plane
2. Deploy Redis for state store
3. Deploy Dapr components (pub/sub, state, secrets)
4. Deploy Dapr configuration (tracing)
5. Update backend deployment with Dapr annotations
6. Deploy event service with Dapr annotations
7. Verify Dapr sidecars are injected
8. Test pub/sub flow
9. Verify traces in Jaeger

## Success Metrics

- Dapr control plane healthy (3 replicas)
- Dapr sidecars injected into all pods
- Events published via Dapr successfully
- Events consumed via Dapr successfully
- Distributed traces visible in Jaeger
- Dapr metrics scraped by Prometheus
- No significant performance degradation

## Dependencies

- Kubernetes cluster (DOKS)
- Kafka cluster (for pub/sub)
- Redis (for state store)
- Jaeger (for tracing)
- Prometheus (for metrics)

## Future Enhancements

- Enable mTLS for production
- Add Dapr bindings for external integrations
- Use Dapr actors for stateful workflows
- Add Dapr workflows for saga patterns
- Implement Dapr resiliency policies

---

**Specification Version**: 1.0
**Approved By**: [Pending]
**Implementation Status**: Not Started
