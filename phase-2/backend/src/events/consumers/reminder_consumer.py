"""Consumer for handling reminder due events and sending notifications."""
from typing import Any, Dict

from sqlmodel import Session

from src.core.logging_config import get_logger
from src.database import engine
from src.events.producer import publish_event
from src.events.schemas import EventType, ReminderEvent
from src.models.task import Task
from src.schemas.reminder import NotificationCreate, NotificationType
from src.services.notification_service import NotificationService
from src.services.reminder_service import ReminderService

logger = get_logger(__name__)


async def handle_reminder_due(event_data: Dict[str, Any]) -> bool:
    """
    Handle ReminderDue events to create and deliver notifications.

    Args:
        event_data: The ReminderDue event payload

    Returns:
        True if handled successfully
    """
    event_type = event_data.get("event_type")
    if event_type != EventType.REMINDER_DUE.value:
        logger.debug(f"Ignoring non-reminder event: {event_type}")
        return True

    payload = event_data.get("payload", {})
    reminder_id = payload.get("reminder_id")
    task_id = payload.get("task_id")
    user_id = event_data.get("user_id")
    task_title = payload.get("task_title")
    channels = payload.get("channels", ["in_app"])
    correlation_id = event_data.get("correlation_id")

    if not reminder_id or not task_id:
        logger.error("ReminderDue event missing required fields")
        return False

    logger.info(f"Processing ReminderDue for reminder {reminder_id}, task {task_id}")

    try:
        with Session(engine) as session:
            reminder_service = ReminderService(session)
            notification_service = NotificationService(session)

            # Mark reminder as sent
            reminder_service.mark_reminder_sent(int(reminder_id))

            # Create in-app notification if channel is enabled
            if "in_app" in channels:
                notification = NotificationCreate(
                    user_id=user_id,
                    type=NotificationType.REMINDER,
                    title="Task Reminder",
                    message=f"Reminder: {task_title}",
                    data={
                        "task_id": task_id,
                        "reminder_id": reminder_id,
                    },
                )
                notification_service.create_notification(notification)

            # Publish ReminderSent event for each channel
            for channel in channels:
                event = ReminderEvent.reminder_sent(
                    reminder_id=reminder_id,
                    user_id=user_id,
                    channel=channel,
                    correlation_id=correlation_id,
                )
                await publish_event(event)

            logger.info(f"Processed reminder {reminder_id} for task {task_id}")

        return True

    except Exception as e:
        logger.error(f"Error processing ReminderDue for reminder {reminder_id}: {e}")
        raise


async def handle_task_completed(event_data: Dict[str, Any]) -> bool:
    """
    Handle TaskCompleted events to cancel pending reminders.

    When a task is completed, all its pending reminders should be cancelled.

    Args:
        event_data: The TaskCompleted event payload

    Returns:
        True if handled successfully
    """
    event_type = event_data.get("event_type")
    if event_type != EventType.TASK_COMPLETED.value:
        return True

    payload = event_data.get("payload", {})
    task_id = payload.get("task_id")

    if not task_id:
        logger.error("TaskCompleted event missing task_id")
        return False

    logger.info(f"Cancelling reminders for completed task {task_id}")

    try:
        with Session(engine) as session:
            reminder_service = ReminderService(session)
            count = reminder_service.cancel_task_reminders(int(task_id))
            if count > 0:
                logger.info(f"Cancelled {count} reminders for task {task_id}")

        return True

    except Exception as e:
        logger.error(f"Error cancelling reminders for task {task_id}: {e}")
        raise


async def process_event(event_data: Dict[str, Any]) -> bool:
    """
    Main event processor - route events to appropriate handlers.

    Args:
        event_data: Raw event data from Dapr

    Returns:
        True if processed successfully
    """
    event_type = event_data.get("event_type")

    handlers = {
        EventType.REMINDER_DUE.value: handle_reminder_due,
        EventType.TASK_COMPLETED.value: handle_task_completed,
    }

    handler = handlers.get(event_type)
    if handler:
        return await handler(event_data)
    else:
        logger.debug(f"No handler for event type: {event_type}")
        return True
