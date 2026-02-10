"""Event producer for publishing events via Dapr pub/sub."""
import os
from typing import Optional

from .dapr_client import get_dapr_client
from .schemas import BaseEvent, TOPICS

# Check if Dapr is enabled (for local development without Dapr)
DAPR_ENABLED = os.getenv("DAPR_ENABLED", "true").lower() == "true"


async def publish_event(
    event: BaseEvent,
    topic: Optional[str] = None,
) -> bool:
    """
    Publish an event to Kafka via Dapr pub/sub.

    Args:
        event: Event to publish
        topic: Override topic name (defaults based on event type)

    Returns:
        True if published successfully
    """
    if not DAPR_ENABLED:
        # Log event for debugging when Dapr is disabled
        print(f"[EVENT] {event.event_type}: {event.model_dump_json()}")
        return True

    # Determine topic based on event type
    if topic is None:
        event_type = event.event_type
        if event_type.startswith("task."):
            topic = TOPICS["task_events"]
        elif event_type.startswith("reminder."):
            topic = TOPICS["reminders"]
        elif event_type.startswith("notification."):
            topic = TOPICS["notifications"]
        else:
            topic = TOPICS["task_events"]

    client = get_dapr_client()
    return await client.publish_event(
        topic=topic,
        data=event.model_dump(),
    )


async def publish_to_audit(event: BaseEvent) -> bool:
    """
    Publish an event to the audit log topic.

    Args:
        event: Event to log

    Returns:
        True if published successfully
    """
    if not DAPR_ENABLED:
        print(f"[AUDIT] {event.event_type}: {event.model_dump_json()}")
        return True

    client = get_dapr_client()
    return await client.publish_event(
        topic=TOPICS["audit"],
        data=event.model_dump(),
    )


async def publish_to_dlq(
    event: BaseEvent,
    error_message: str,
    retry_count: int = 0,
) -> bool:
    """
    Publish a failed event to the dead letter queue.

    Args:
        event: Original event that failed
        error_message: Error description
        retry_count: Number of retries attempted

    Returns:
        True if published successfully
    """
    dlq_payload = {
        "original_event": event.model_dump(),
        "error_message": error_message,
        "retry_count": retry_count,
    }

    if not DAPR_ENABLED:
        print(f"[DLQ] Error: {error_message}, Event: {event.event_type}")
        return True

    client = get_dapr_client()
    return await client.publish_event(
        topic=TOPICS["dlq"],
        data=dlq_payload,
    )
