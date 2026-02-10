"""Dapr pub/sub subscription endpoints."""
import asyncio
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from src.core.logging_config import get_logger
from src.events.consumers import recurring_consumer, reminder_consumer
from src.events.schemas import TOPICS

router = APIRouter()
logger = get_logger(__name__)


@router.get("/dapr/subscribe")
async def dapr_subscribe():
    """Return Dapr subscription configuration.

    This endpoint tells Dapr which topics this service subscribes to.
    Events are delivered to the corresponding route endpoints.
    """
    return [
        {
            "pubsubname": "pubsub",
            "topic": TOPICS["task_events"],
            "route": "/api/events/tasks",
        },
        {
            "pubsubname": "pubsub",
            "topic": TOPICS["reminders"],
            "route": "/api/events/reminders",
        },
    ]


@router.post("/events/tasks")
async def handle_task_events(request: Request):
    """Handle incoming task events from Dapr pub/sub.

    Processes TaskCreated, TaskUpdated, TaskCompleted, TaskDeleted events.
    """
    try:
        body = await request.json()
        # Dapr wraps the event in a CloudEvents envelope
        event_data = body.get("data", body)

        logger.info(f"Received task event: {event_data.get('event_type')}")

        # Process with appropriate consumers
        results = await asyncio.gather(
            recurring_consumer.process_event(event_data),
            reminder_consumer.process_event(event_data),
            return_exceptions=True,
        )

        # Log any errors but don't fail the request
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Consumer error: {result}")

        # Return SUCCESS to acknowledge the event
        return JSONResponse({"status": "SUCCESS"})

    except Exception as e:
        logger.error(f"Error processing task event: {e}")
        # Return SUCCESS to prevent infinite retries
        # In production, implement proper DLQ handling
        return JSONResponse({"status": "SUCCESS"})


@router.post("/events/reminders")
async def handle_reminder_events(request: Request):
    """Handle incoming reminder events from Dapr pub/sub.

    Processes ReminderDue events to send notifications.
    """
    try:
        body = await request.json()
        event_data = body.get("data", body)

        logger.info(f"Received reminder event: {event_data.get('event_type')}")

        await reminder_consumer.process_event(event_data)

        return JSONResponse({"status": "SUCCESS"})

    except Exception as e:
        logger.error(f"Error processing reminder event: {e}")
        return JSONResponse({"status": "SUCCESS"})
