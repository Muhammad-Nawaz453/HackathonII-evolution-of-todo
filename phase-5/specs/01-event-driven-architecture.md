# Specification: Event-Driven Architecture

**Feature ID**: 01
**Feature Name**: Event-Driven Architecture
**Phase**: 5 - Production Cloud Deployment
**Status**: Draft
**Created**: 2026-02-07
**Last Updated**: 2026-02-07

## Purpose

Transform the todo application from a synchronous, request-response architecture to an event-driven architecture where state changes are published as events to Apache Kafka. This enables loose coupling, scalability, and real-time event processing across distributed services.

## User Stories

**As a system architect**, I want all task state changes to be published as events so that multiple services can react to changes independently without tight coupling.

**As a developer**, I want a clear event schema and publishing mechanism so that I can reliably publish and consume events.

**As an operations engineer**, I want event-driven architecture so that the system can scale horizontally and handle high throughput.

**As a product manager**, I want event streams so that we can build analytics, notifications, and audit trails without modifying the core application.

## Acceptance Criteria

### Event Publishing

- [ ] When a task is created via POST /tasks, a `task.created` event is published to Kafka
- [ ] When a task is updated via PUT /tasks/{id}, a `task.updated` event is published to Kafka
- [ ] When a task is deleted via DELETE /tasks/{id}, a `task.deleted` event is published to Kafka
- [ ] When a task is marked complete via POST /tasks/{id}/complete, a `task.completed` event is published to Kafka
- [ ] Event publishing is asynchronous and does not block the API response
- [ ] Failed event publishing is logged but does not fail the API request
- [ ] Events include correlation IDs for distributed tracing

### Event Schema

- [ ] All events follow a consistent schema with: event_id, event_type, timestamp, correlation_id, payload
- [ ] Event schemas are defined in Avro format
- [ ] Event schemas are versioned (v1, v2, etc.)
- [ ] Events are backward-compatible (new fields are optional)

### Event Consumption

- [ ] Event service consumes all task events from Kafka
- [ ] Event processing is idempotent (processing same event multiple times is safe)
- [ ] Failed event processing is retried with exponential backoff
- [ ] Unprocessable events are sent to dead letter queue
- [ ] Event consumer tracks offset and commits after successful processing

### Integration with Existing System

- [ ] Backend API continues to work synchronously (database writes happen immediately)
- [ ] Event publishing happens after successful database write
- [ ] API response time is not significantly impacted by event publishing (<50ms overhead)
- [ ] Existing Phase 3 functionality remains unchanged

## Event Types

### 1. TaskCreated Event

**Topic**: `todo.tasks.created`
**Partition Key**: `task_id`

**Schema**:
```json
{
  "event_id": "uuid",
  "event_type": "task.created",
  "event_version": "v1",
  "timestamp": "ISO 8601 timestamp",
  "correlation_id": "uuid",
  "source": "todo-backend",
  "payload": {
    "task_id": "integer",
    "title": "string",
    "description": "string or null",
    "status": "incomplete",
    "created_at": "ISO 8601 timestamp",
    "user_id": "string or null"
  }
}
```

### 2. TaskUpdated Event

**Topic**: `todo.tasks.updated`
**Partition Key**: `task_id`

**Schema**:
```json
{
  "event_id": "uuid",
  "event_type": "task.updated",
  "event_version": "v1",
  "timestamp": "ISO 8601 timestamp",
  "correlation_id": "uuid",
  "source": "todo-backend",
  "payload": {
    "task_id": "integer",
    "title": "string",
    "description": "string or null",
    "status": "complete or incomplete",
    "updated_at": "ISO 8601 timestamp",
    "changes": {
      "title": "boolean",
      "description": "boolean",
      "status": "boolean"
    }
  }
}
```

### 3. TaskDeleted Event

**Topic**: `todo.tasks.deleted`
**Partition Key**: `task_id`

**Schema**:
```json
{
  "event_id": "uuid",
  "event_type": "task.deleted",
  "event_version": "v1",
  "timestamp": "ISO 8601 timestamp",
  "correlation_id": "uuid",
  "source": "todo-backend",
  "payload": {
    "task_id": "integer",
    "deleted_at": "ISO 8601 timestamp"
  }
}
```

### 4. TaskCompleted Event

**Topic**: `todo.tasks.completed`
**Partition Key**: `task_id`

**Schema**:
```json
{
  "event_id": "uuid",
  "event_type": "task.completed",
  "event_version": "v1",
  "timestamp": "ISO 8601 timestamp",
  "correlation_id": "uuid",
  "source": "todo-backend",
  "payload": {
    "task_id": "integer",
    "completed_at": "ISO 8601 timestamp"
  }
}
```

## Architecture

### Event Flow

```
User Request → Backend API → Database Write → Event Publisher → Dapr Pub/Sub → Kafka Topic
                    ↓                                                                ↓
              API Response                                                    Event Service
                                                                                     ↓
                                                                          Process Event
                                                                          (Analytics, Audit, etc.)
```

### Components

1. **Backend API** (existing, modified)
   - Handles HTTP requests
   - Writes to database
   - Publishes events via Dapr pub/sub
   - Returns response to client

2. **Event Publisher** (new module in backend)
   - Publishes events to Dapr pub/sub API
   - Handles serialization to JSON/Avro
   - Adds correlation IDs and metadata
   - Logs publishing failures

3. **Dapr Pub/Sub Component** (new)
   - Configured to use Kafka as backend
   - Handles connection to Kafka cluster
   - Provides HTTP/gRPC API for publishing

4. **Kafka Cluster** (new)
   - 3 brokers for high availability
   - Topics with 3 partitions each
   - Replication factor of 3
   - Retention: 7 days

5. **Event Service** (new microservice)
   - Subscribes to all task events
   - Processes events for analytics
   - Logs events for audit trail
   - Idempotent processing

## Implementation Details

### Backend Changes

**File**: `backend/src/event_publisher.py` (new)

```python
from dapr.clients import DaprClient
from typing import Dict, Any
import uuid
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class EventPublisher:
    def __init__(self, pubsub_name: str = "kafka-pubsub"):
        self.pubsub_name = pubsub_name
        self.source = "todo-backend"

    async def publish_event(
        self,
        topic: str,
        event_type: str,
        payload: Dict[str, Any],
        correlation_id: str = None
    ) -> bool:
        """Publish event to Kafka via Dapr pub/sub."""
        try:
            event = {
                "event_id": str(uuid.uuid4()),
                "event_type": event_type,
                "event_version": "v1",
                "timestamp": datetime.utcnow().isoformat(),
                "correlation_id": correlation_id or str(uuid.uuid4()),
                "source": self.source,
                "payload": payload
            }

            with DaprClient() as client:
                client.publish_event(
                    pubsub_name=self.pubsub_name,
                    topic_name=topic,
                    data=event,
                    data_content_type="application/json"
                )

            logger.info(f"Published event {event_type} to {topic}")
            return True

        except Exception as e:
            logger.error(f"Failed to publish event {event_type}: {e}")
            return False
```

**File**: `backend/src/routers/tasks.py` (modified)

Add event publishing after database operations:

```python
from src.event_publisher import EventPublisher

event_publisher = EventPublisher()

@router.post("/tasks", response_model=Task)
async def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    # Existing code to create task in database
    db_task = Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    # NEW: Publish event
    await event_publisher.publish_event(
        topic="todo.tasks.created",
        event_type="task.created",
        payload={
            "task_id": db_task.id,
            "title": db_task.title,
            "description": db_task.description,
            "status": "incomplete",
            "created_at": db_task.created_at.isoformat()
        }
    )

    return db_task
```

### Event Service

**File**: `backend-event-service/src/main.py` (new)

```python
from fastapi import FastAPI
from dapr.ext.fastapi import DaprApp
import logging

app = FastAPI(title="Event Service")
dapr_app = DaprApp(app)

logger = logging.getLogger(__name__)

@dapr_app.subscribe(pubsub="kafka-pubsub", topic="todo.tasks.created")
async def handle_task_created(event: dict):
    """Handle task created events."""
    logger.info(f"Received task.created event: {event}")

    # Process event (analytics, audit, etc.)
    task_id = event["payload"]["task_id"]
    title = event["payload"]["title"]

    # TODO: Store in analytics database, send notifications, etc.
    logger.info(f"Task {task_id} created: {title}")

    return {"success": True}

@dapr_app.subscribe(pubsub="kafka-pubsub", topic="todo.tasks.updated")
async def handle_task_updated(event: dict):
    """Handle task updated events."""
    logger.info(f"Received task.updated event: {event}")
    return {"success": True}

@dapr_app.subscribe(pubsub="kafka-pubsub", topic="todo.tasks.deleted")
async def handle_task_deleted(event: dict):
    """Handle task deleted events."""
    logger.info(f"Received task.deleted event: {event}")
    return {"success": True}

@dapr_app.subscribe(pubsub="kafka-pubsub", topic="todo.tasks.completed")
async def handle_task_completed(event: dict):
    """Handle task completed events."""
    logger.info(f"Received task.completed event: {event}")
    return {"success": True}

@app.get("/health")
async def health():
    return {"status": "healthy"}
```

## Edge Cases and Error Handling

### Event Publishing Failures

- **Scenario**: Kafka is unavailable
- **Handling**: Log error, continue with API response (event publishing is best-effort)
- **Recovery**: Events can be republished from database audit log if needed

### Duplicate Events

- **Scenario**: Event published multiple times due to retries
- **Handling**: Event service processes idempotently using event_id deduplication
- **Implementation**: Store processed event_ids in Redis with TTL

### Event Ordering

- **Scenario**: Events arrive out of order
- **Handling**: Use partition key (task_id) to ensure ordering within partition
- **Implementation**: Kafka guarantees ordering within partition

### Schema Evolution

- **Scenario**: Event schema needs to change
- **Handling**: Add new optional fields, never remove or change existing fields
- **Versioning**: Increment event_version field (v1 → v2)

### Consumer Lag

- **Scenario**: Event service falls behind in processing
- **Handling**: Monitor consumer lag, scale event service horizontally
- **Alerting**: Alert if lag exceeds 1000 messages

## Data Requirements

### Kafka Topics

- `todo.tasks.created`: 3 partitions, replication factor 3, retention 7 days
- `todo.tasks.updated`: 3 partitions, replication factor 3, retention 7 days
- `todo.tasks.deleted`: 3 partitions, replication factor 3, retention 7 days
- `todo.tasks.completed`: 3 partitions, replication factor 3, retention 7 days

### Event Metadata

- `event_id`: UUID v4, unique per event
- `correlation_id`: UUID v4, tracks request across services
- `timestamp`: ISO 8601 UTC timestamp
- `source`: Service name that published event

## Dependencies

- Apache Kafka cluster (deployed via Strimzi operator)
- Dapr pub/sub component configured with Kafka
- Backend API (Phase 3)
- Event service (new microservice)

## Testing Strategy

### Unit Tests

- Test event serialization and schema validation
- Test event publisher with mocked Dapr client
- Test event handlers with sample events

### Integration Tests

- Test end-to-end event flow (API → Kafka → Event Service)
- Test event publishing with real Kafka cluster
- Test event consumption and processing

### Load Tests

- Test event throughput (target: 1000 events/second)
- Test consumer lag under high load
- Test system behavior when Kafka is unavailable

## Monitoring and Metrics

### Metrics to Track

- `events_published_total`: Counter of events published by type
- `events_published_failures_total`: Counter of failed publishes
- `event_publish_duration_seconds`: Histogram of publish latency
- `events_consumed_total`: Counter of events consumed by type
- `event_processing_duration_seconds`: Histogram of processing time
- `consumer_lag`: Gauge of consumer lag per topic

### Alerts

- Alert if event publishing failure rate > 5%
- Alert if consumer lag > 1000 messages for 5 minutes
- Alert if event processing time p95 > 1 second

## Performance Requirements

- Event publishing adds < 50ms to API response time
- Event service processes events within 100ms (p95)
- System handles 1000 events/second sustained load
- Consumer lag stays below 100 messages under normal load

## Security Considerations

- Events do not contain sensitive data (passwords, tokens)
- Kafka uses SASL/SCRAM authentication (optional for demo)
- Dapr sidecars communicate via mTLS
- Event service validates event schema before processing

## Rollout Plan

1. Deploy Kafka cluster to DOKS
2. Configure Dapr pub/sub component
3. Deploy event service
4. Update backend to publish events (feature flag enabled)
5. Monitor event flow and consumer lag
6. Enable for all users once stable

## Success Metrics

- All task operations publish events successfully (>99% success rate)
- Event service processes all events within SLA (100ms p95)
- Consumer lag stays below 100 messages
- No impact on API response times (<50ms overhead)
- Zero data loss (all events delivered at least once)

## Future Enhancements

- Schema registry for centralized schema management
- Event replay capability for debugging
- Multiple event consumers (analytics, notifications, webhooks)
- Event-driven workflows (saga pattern)
- Event sourcing for full audit trail

---

**Specification Version**: 1.0
**Approved By**: [Pending]
**Implementation Status**: Not Started
