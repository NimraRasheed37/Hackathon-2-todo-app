"""Consumer for handling task completed events and spawning recurring tasks."""
from typing import Any, Dict

from sqlmodel import Session

from src.core.logging_config import get_logger
from src.database import engine
from src.events.producer import publish_event
from src.events.schemas import EventType, RecurrenceEvent
from src.services.recurring_service import RecurringService

logger = get_logger(__name__)


async def handle_task_completed(event_data: Dict[str, Any]) -> bool:
    """
    Handle TaskCompleted events to spawn next recurring task instance.

    When a task with a recurrence pattern is completed, this handler:
    1. Checks if the task has an active recurrence
    2. Spawns the next task instance if applicable
    3. Publishes RecurrenceTriggered event

    Args:
        event_data: The TaskCompleted event payload

    Returns:
        True if handled successfully
    """
    event_type = event_data.get("event_type")
    if event_type != EventType.TASK_COMPLETED.value:
        logger.debug(f"Ignoring non-completed event: {event_type}")
        return True

    payload = event_data.get("payload", {})
    task_id = payload.get("task_id")
    user_id = event_data.get("user_id")
    has_recurrence = payload.get("has_recurrence", False)
    correlation_id = event_data.get("correlation_id")

    if not task_id:
        logger.error("TaskCompleted event missing task_id")
        return False

    # Quick exit if task doesn't have recurrence
    if not has_recurrence:
        logger.debug(f"Task {task_id} has no recurrence, skipping")
        return True

    logger.info(f"Processing TaskCompleted for recurring task {task_id}")

    try:
        with Session(engine) as session:
            service = RecurringService(session)

            # Try to spawn the next task instance
            new_task = service.process_completed_task(int(task_id))

            if new_task:
                # Get the recurrence for event publishing
                recurrence = service.get_task_recurrence(int(task_id))
                if recurrence:
                    # Publish RecurrenceTriggered event
                    event = RecurrenceEvent.recurrence_triggered(
                        recurrence_id=str(recurrence.id),
                        original_task_id=task_id,
                        new_task_id=str(new_task.id),
                        user_id=user_id,
                        occurrence_number=recurrence.total_occurrences,
                        correlation_id=correlation_id,
                    )
                    await publish_event(event)

                logger.info(
                    f"Spawned new task {new_task.id} from recurring task {task_id}"
                )
            else:
                logger.info(
                    f"No new task spawned for task {task_id} "
                    "(recurrence may be complete or inactive)"
                )

        return True

    except Exception as e:
        logger.error(f"Error processing TaskCompleted for task {task_id}: {e}")
        raise


async def process_event(event_data: Dict[str, Any]) -> bool:
    """
    Main event processor - route events to appropriate handlers.

    This is the entry point for the Dapr subscription endpoint.

    Args:
        event_data: Raw event data from Dapr

    Returns:
        True if processed successfully
    """
    event_type = event_data.get("event_type")

    handlers = {
        EventType.TASK_COMPLETED.value: handle_task_completed,
    }

    handler = handlers.get(event_type)
    if handler:
        return await handler(event_data)
    else:
        logger.debug(f"No handler for event type: {event_type}")
        return True
