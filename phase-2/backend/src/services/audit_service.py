"""Audit service for logging events to the audit log table."""

from datetime import datetime, timezone
from typing import Optional, List

from sqlmodel import Session, select, func
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB

from src.core.logging_config import get_logger

logger = get_logger(__name__)


# Note: This model is defined here to avoid circular imports
# The actual table is created by migration 007
from sqlmodel import Field, SQLModel  # noqa: E402


class AuditLog(SQLModel, table=True):
    """SQLModel entity for audit log entries."""

    __tablename__ = "audit_log"

    id: Optional[int] = Field(default=None, primary_key=True)
    event_id: str = Field(max_length=100, unique=True, index=True)
    event_type: str = Field(max_length=50, index=True)
    aggregate_type: str = Field(max_length=50, index=True)
    aggregate_id: str = Field(max_length=100, index=True)
    user_id: str = Field(index=True)
    payload: dict = Field(default={}, sa_column=Column(JSONB))
    correlation_id: Optional[str] = Field(default=None, max_length=100, index=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), index=True)


class AuditService:
    """Service for managing audit log entries."""

    def __init__(self, session: Session):
        self.session = session

    def log_event(
        self,
        event_id: str,
        event_type: str,
        aggregate_type: str,
        aggregate_id: str,
        user_id: str,
        payload: dict,
        timestamp: Optional[str] = None,
        correlation_id: Optional[str] = None,
    ) -> AuditLog:
        """Log an event to the audit log.

        Args:
            event_id: Unique event identifier
            event_type: Type of event (e.g., task.created)
            aggregate_type: Type of aggregate (e.g., Task)
            aggregate_id: ID of the aggregate
            user_id: User who triggered the event
            payload: Event payload data
            timestamp: Event timestamp (ISO format)
            correlation_id: Correlation ID for tracing

        Returns:
            The created AuditLog entry
        """
        # Check for duplicate (idempotency)
        existing = self.get_by_event_id(event_id)
        if existing:
            logger.debug(f"Duplicate event {event_id} - skipping")
            return existing

        # Parse timestamp or use now
        if timestamp:
            try:
                created_at = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            except ValueError:
                created_at = datetime.now(timezone.utc)
        else:
            created_at = datetime.now(timezone.utc)

        audit_entry = AuditLog(
            event_id=event_id,
            event_type=event_type,
            aggregate_type=aggregate_type,
            aggregate_id=aggregate_id,
            user_id=user_id,
            payload=payload,
            correlation_id=correlation_id,
            created_at=created_at,
        )

        self.session.add(audit_entry)
        self.session.commit()
        self.session.refresh(audit_entry)

        logger.debug(f"Logged audit entry {audit_entry.id} for event {event_id}")
        return audit_entry

    def get_by_event_id(self, event_id: str) -> Optional[AuditLog]:
        """Get an audit entry by event ID."""
        statement = select(AuditLog).where(AuditLog.event_id == event_id)
        return self.session.exec(statement).first()

    def get_by_aggregate(
        self,
        aggregate_type: str,
        aggregate_id: str,
        limit: int = 50
    ) -> List[AuditLog]:
        """Get audit entries for a specific aggregate.

        Args:
            aggregate_type: Type of aggregate
            aggregate_id: ID of the aggregate
            limit: Max entries to return

        Returns:
            List of audit entries ordered by created_at desc
        """
        statement = (
            select(AuditLog)
            .where(
                AuditLog.aggregate_type == aggregate_type,
                AuditLog.aggregate_id == aggregate_id
            )
            .order_by(AuditLog.created_at.desc())
            .limit(limit)
        )
        return list(self.session.exec(statement).all())

    def get_by_user(
        self,
        user_id: str,
        event_type: Optional[str] = None,
        limit: int = 50
    ) -> List[AuditLog]:
        """Get audit entries for a user.

        Args:
            user_id: User ID
            event_type: Optional event type filter
            limit: Max entries to return

        Returns:
            List of audit entries ordered by created_at desc
        """
        statement = select(AuditLog).where(AuditLog.user_id == user_id)

        if event_type:
            statement = statement.where(AuditLog.event_type == event_type)

        statement = statement.order_by(AuditLog.created_at.desc()).limit(limit)
        return list(self.session.exec(statement).all())

    def get_by_correlation_id(self, correlation_id: str) -> List[AuditLog]:
        """Get all audit entries with a correlation ID.

        Useful for tracing related events across the system.

        Args:
            correlation_id: Correlation ID to search for

        Returns:
            List of audit entries ordered by created_at asc
        """
        statement = (
            select(AuditLog)
            .where(AuditLog.correlation_id == correlation_id)
            .order_by(AuditLog.created_at.asc())
        )
        return list(self.session.exec(statement).all())

    def get_recent_events(
        self,
        event_type: Optional[str] = None,
        limit: int = 100
    ) -> List[AuditLog]:
        """Get recent audit entries.

        Args:
            event_type: Optional event type filter
            limit: Max entries to return

        Returns:
            List of recent audit entries
        """
        statement = select(AuditLog)

        if event_type:
            statement = statement.where(AuditLog.event_type == event_type)

        statement = statement.order_by(AuditLog.created_at.desc()).limit(limit)
        return list(self.session.exec(statement).all())

    def count_events(
        self,
        event_type: Optional[str] = None,
        since: Optional[datetime] = None
    ) -> int:
        """Count audit entries with optional filters.

        Args:
            event_type: Optional event type filter
            since: Only count events after this time

        Returns:
            Count of matching entries
        """
        statement = select(func.count()).select_from(AuditLog)

        if event_type:
            statement = statement.where(AuditLog.event_type == event_type)

        if since:
            statement = statement.where(AuditLog.created_at >= since)

        return self.session.exec(statement).one()
