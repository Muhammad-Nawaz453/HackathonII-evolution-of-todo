"""Event service that consumes events from Kafka via Dapr."""

from fastapi import FastAPI, Request
from cloudevents.http import from_http
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response
import logging
import json
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Event Service",
    version="1.0.0",
    description="Processes events from Kafka via Dapr"
)

# Prometheus metrics
events_received_total = Counter(
    'events_received_total',
    'Total events received',
    ['event_type', 'success']
)

event_processing_duration_seconds = Histogram(
    'event_processing_duration_seconds',
    'Event processing duration in seconds',
    ['event_type']
)


@app.post("/events/task-created")
async def handle_task_created(request: Request):
    """Handle task.created events."""
    try:
        # Parse CloudEvent
        event = from_http(request.headers, await request.body())
        data = json.loads(event.data)

        logger.info(f"Received task.created event: {data.get('event_id')}")

        # Process event
        with event_processing_duration_seconds.labels(event_type='task.created').time():
            task_id = data["payload"]["task_id"]
            title = data["payload"]["title"]

            logger.info(f"Processing task creation: ID={task_id}, Title={title}")

            # TODO: Implement actual processing
            # - Store in analytics database
            # - Send notifications
            # - Update dashboards
            # - Trigger workflows

        events_received_total.labels(event_type='task.created', success='true').inc()
        return {"success": True}

    except Exception as e:
        logger.error(f"Error handling task.created event: {e}", exc_info=True)
        events_received_total.labels(event_type='task.created', success='false').inc()
        return {"success": False, "error": str(e)}


@app.post("/events/task-updated")
async def handle_task_updated(request: Request):
    """Handle task.updated events."""
    try:
        event = from_http(request.headers, await request.body())
        data = json.loads(event.data)

        logger.info(f"Received task.updated event: {data.get('event_id')}")

        with event_processing_duration_seconds.labels(event_type='task.updated').time():
            task_id = data["payload"]["task_id"]
            changes = data["payload"].get("changes", {})

            logger.info(f"Processing task update: ID={task_id}, Changes={changes}")

        events_received_total.labels(event_type='task.updated', success='true').inc()
        return {"success": True}

    except Exception as e:
        logger.error(f"Error handling task.updated event: {e}", exc_info=True)
        events_received_total.labels(event_type='task.updated', success='false').inc()
        return {"success": False, "error": str(e)}


@app.post("/events/task-deleted")
async def handle_task_deleted(request: Request):
    """Handle task.deleted events."""
    try:
        event = from_http(request.headers, await request.body())
        data = json.loads(event.data)

        logger.info(f"Received task.deleted event: {data.get('event_id')}")

        with event_processing_duration_seconds.labels(event_type='task.deleted').time():
            task_id = data["payload"]["task_id"]
            logger.info(f"Processing task deletion: ID={task_id}")

        events_received_total.labels(event_type='task.deleted', success='true').inc()
        return {"success": True}

    except Exception as e:
        logger.error(f"Error handling task.deleted event: {e}", exc_info=True)
        events_received_total.labels(event_type='task.deleted', success='false').inc()
        return {"success": False, "error": str(e)}


@app.post("/events/task-completed")
async def handle_task_completed(request: Request):
    """Handle task.completed events."""
    try:
        event = from_http(request.headers, await request.body())
        data = json.loads(event.data)

        logger.info(f"Received task.completed event: {data.get('event_id')}")

        with event_processing_duration_seconds.labels(event_type='task.completed').time():
            task_id = data["payload"]["task_id"]
            logger.info(f"Processing task completion: ID={task_id}")

        events_received_total.labels(event_type='task.completed', success='true').inc()
        return {"success": True}

    except Exception as e:
        logger.error(f"Error handling task.completed event: {e}", exc_info=True)
        events_received_total.labels(event_type='task.completed', success='false').inc()
        return {"success": False, "error": str(e)}


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "event-service",
        "version": "1.0.0"
    }


@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint."""
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.get("/dapr/subscribe")
async def subscribe():
    """
    Dapr subscription endpoint.
    Dapr calls this to discover which topics this service subscribes to.
    """
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
    logger.info(f"Dapr subscription endpoint called, returning {len(subscriptions)} subscriptions")
    return subscriptions


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="info")
