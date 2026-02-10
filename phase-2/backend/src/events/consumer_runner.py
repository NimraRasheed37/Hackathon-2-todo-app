"""Consumer runner for starting all Kafka consumers via Dapr subscriptions."""
import asyncio
import os
from typing import Any, Dict

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.core.logging_config import get_logger, setup_logging
from src.events.consumers import recurring_consumer, reminder_consumer, audit_consumer
from src.events.schemas import TOPICS

# Initialize logging
setup_logging()
logger = get_logger(__name__)

# Create FastAPI app for Dapr subscription endpoints
app = FastAPI(
    title="Todo Consumer Service",
    description="Kafka consumer service for processing events via Dapr",
    version="1.0.0",
)


@app.get("/dapr/subscribe")
async def subscribe():
    """Return Dapr subscription configuration.

    This endpoint tells Dapr which topics to subscribe to and where
    to deliver events.
    """
    return [
        {
            "pubsubname": "pubsub",
            "topic": TOPICS["task_events"],
            "route": "/events/tasks",
        },
        {
            "pubsubname": "pubsub",
            "topic": TOPICS["reminders"],
            "route": "/events/reminders",
        },
        {
            "pubsubname": "pubsub",
            "topic": TOPICS["audit"],
            "route": "/events/audit",
        },
    ]


@app.post("/events/tasks")
async def handle_task_events(request: Request):
    """Handle task events (created, updated, completed, deleted).

    Routes to:
    - Recurring consumer for TaskCompleted events
    - Reminder consumer for TaskCompleted (cancel reminders)
    - Audit consumer for all events
    """
    try:
        event_data = await request.json()
        cloud_event = event_data.get("data", event_data)

        logger.info(f"Received task event: {cloud_event.get('event_type')}")

        # Process in parallel
        results = await asyncio.gather(
            recurring_consumer.process_event(cloud_event),
            reminder_consumer.process_event(cloud_event),
            audit_consumer.process_event(cloud_event),
            return_exceptions=True,
        )

        # Check for errors
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Consumer {i} failed: {result}")

        return JSONResponse({"status": "SUCCESS"})

    except Exception as e:
        logger.error(f"Error processing task event: {e}")
        # Return SUCCESS to avoid Dapr retries for unrecoverable errors
        # In production, you might want to return RETRY for transient errors
        return JSONResponse({"status": "SUCCESS"})


@app.post("/events/reminders")
async def handle_reminder_events(request: Request):
    """Handle reminder events (due, sent)."""
    try:
        event_data = await request.json()
        cloud_event = event_data.get("data", event_data)

        logger.info(f"Received reminder event: {cloud_event.get('event_type')}")

        # Process with reminder and audit consumers
        results = await asyncio.gather(
            reminder_consumer.process_event(cloud_event),
            audit_consumer.process_event(cloud_event),
            return_exceptions=True,
        )

        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Consumer {i} failed: {result}")

        return JSONResponse({"status": "SUCCESS"})

    except Exception as e:
        logger.error(f"Error processing reminder event: {e}")
        return JSONResponse({"status": "SUCCESS"})


@app.post("/events/audit")
async def handle_audit_events(request: Request):
    """Handle audit-specific events (for direct audit logging)."""
    try:
        event_data = await request.json()
        cloud_event = event_data.get("data", event_data)

        logger.info(f"Received audit event: {cloud_event.get('event_type')}")

        await audit_consumer.process_event(cloud_event)

        return JSONResponse({"status": "SUCCESS"})

    except Exception as e:
        logger.error(f"Error processing audit event: {e}")
        return JSONResponse({"status": "SUCCESS"})


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "consumer"}


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", "8001"))
    logger.info(f"Starting consumer service on port {port}")

    uvicorn.run(
        "src.events.consumer_runner:app",
        host="0.0.0.0",
        port=port,
        reload=os.getenv("ENVIRONMENT", "development") == "development",
    )
