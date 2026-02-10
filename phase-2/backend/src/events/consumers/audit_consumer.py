"""Consumer for logging all events to the audit log."""
from typing import Any, Dict

from sqlmodel import Session

from src.core.logging_config import get_logger
from src.database import engine
from src.services.audit_service import AuditService

logger = get_logger(__name__)


async def handle_any_event(event_data: Dict[str, Any]) -> bool:
    """
    Handle any event by logging it to the audit log.

    This consumer receives all events and creates an audit record for each.

    Args:
        event_data: The event payload

    Returns:
        True if handled successfully
    """
    event_type = event_data.get("event_type")
    event_id = event_data.get("event_id")
    aggregate_type = event_data.get("aggregate_type")
    aggregate_id = event_data.get("aggregate_id")
    user_id = event_data.get("user_id")
    payload = event_data.get("payload", {})
    timestamp = event_data.get("timestamp")
    correlation_id = event_data.get("correlation_id")

    logger.debug(f"Audit: Processing {event_type} event {event_id}")

    try:
        with Session(engine) as session:
            service = AuditService(session)

            service.log_event(
                event_id=event_id,
                event_type=event_type,
                aggregate_type=aggregate_type,
                aggregate_id=aggregate_id,
                user_id=user_id,
                payload=payload,
                timestamp=timestamp,
                correlation_id=correlation_id,
            )

        logger.info(f"Audit: Logged event {event_id} ({event_type})")
        return True

    except Exception as e:
        logger.error(f"Audit: Failed to log event {event_id}: {e}")
        raise


async def process_event(event_data: Dict[str, Any]) -> bool:
    """
    Main event processor - logs all events.

    Args:
        event_data: Raw event data from Dapr

    Returns:
        True if processed successfully
    """
    return await handle_any_event(event_data)
