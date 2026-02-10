"""Notification service for managing user notifications."""

from datetime import datetime, timezone
from typing import Optional, List, Tuple

from sqlmodel import Session, select, func

from src.models.notification import Notification
from src.schemas.reminder import NotificationCreate
from src.core.logging_config import get_logger

logger = get_logger(__name__)


class NotificationService:
    """Service for managing user notifications."""

    def __init__(self, session: Session):
        self.session = session

    def create_notification(
        self,
        notification: NotificationCreate
    ) -> Notification:
        """Create a new notification.

        Args:
            notification: Notification data

        Returns:
            The created Notification
        """
        db_notification = Notification(
            user_id=notification.user_id,
            type=notification.type.value,
            title=notification.title,
            message=notification.message,
            data=notification.data,
            read=False,
        )

        self.session.add(db_notification)
        self.session.commit()
        self.session.refresh(db_notification)

        logger.info(
            f"Created notification {db_notification.id} for user {notification.user_id}"
        )
        return db_notification

    def get_notification(self, notification_id: int) -> Optional[Notification]:
        """Get a notification by ID."""
        return self.session.get(Notification, notification_id)

    def get_user_notifications(
        self,
        user_id: str,
        limit: int = 50,
        offset: int = 0,
        unread_only: bool = False,
    ) -> Tuple[List[Notification], int, int]:
        """Get notifications for a user with pagination.

        Args:
            user_id: The user ID
            limit: Max notifications to return
            offset: Pagination offset
            unread_only: Only return unread notifications

        Returns:
            Tuple of (notifications, total_count, unread_count)
        """
        # Base query
        base_query = select(Notification).where(Notification.user_id == user_id)

        if unread_only:
            base_query = base_query.where(Notification.read == False)

        # Get total count
        count_query = select(func.count()).select_from(Notification).where(
            Notification.user_id == user_id
        )
        if unread_only:
            count_query = count_query.where(Notification.read == False)
        total = self.session.exec(count_query).one()

        # Get unread count
        unread_query = select(func.count()).select_from(Notification).where(
            Notification.user_id == user_id,
            Notification.read == False
        )
        unread_count = self.session.exec(unread_query).one()

        # Get paginated results
        query = base_query.order_by(Notification.created_at.desc()).offset(offset).limit(limit)
        notifications = list(self.session.exec(query).all())

        return notifications, total, unread_count

    def mark_as_read(self, notification_id: int, user_id: str) -> Optional[Notification]:
        """Mark a notification as read.

        Args:
            notification_id: The notification ID
            user_id: The user ID (for authorization)

        Returns:
            The updated notification or None if not found/unauthorized
        """
        notification = self.session.get(Notification, notification_id)
        if not notification or notification.user_id != user_id:
            return None

        if not notification.read:
            notification.read = True
            notification.read_at = datetime.now(timezone.utc)
            self.session.add(notification)
            self.session.commit()
            self.session.refresh(notification)

        return notification

    def mark_multiple_as_read(
        self,
        notification_ids: List[int],
        user_id: str
    ) -> int:
        """Mark multiple notifications as read.

        Args:
            notification_ids: List of notification IDs
            user_id: The user ID (for authorization)

        Returns:
            Number of notifications updated
        """
        statement = select(Notification).where(
            Notification.id.in_(notification_ids),
            Notification.user_id == user_id,
            Notification.read == False
        )
        notifications = list(self.session.exec(statement).all())

        now = datetime.now(timezone.utc)
        count = 0
        for notification in notifications:
            notification.read = True
            notification.read_at = now
            self.session.add(notification)
            count += 1

        if count > 0:
            self.session.commit()
            logger.info(f"Marked {count} notifications as read for user {user_id}")

        return count

    def mark_all_as_read(self, user_id: str) -> int:
        """Mark all user notifications as read.

        Args:
            user_id: The user ID

        Returns:
            Number of notifications updated
        """
        statement = select(Notification).where(
            Notification.user_id == user_id,
            Notification.read == False
        )
        notifications = list(self.session.exec(statement).all())

        now = datetime.now(timezone.utc)
        count = 0
        for notification in notifications:
            notification.read = True
            notification.read_at = now
            self.session.add(notification)
            count += 1

        if count > 0:
            self.session.commit()
            logger.info(f"Marked all ({count}) notifications as read for user {user_id}")

        return count

    def delete_notification(self, notification_id: int, user_id: str) -> bool:
        """Delete a notification.

        Args:
            notification_id: The notification ID
            user_id: The user ID (for authorization)

        Returns:
            True if deleted, False if not found/unauthorized
        """
        notification = self.session.get(Notification, notification_id)
        if not notification or notification.user_id != user_id:
            return False

        self.session.delete(notification)
        self.session.commit()

        logger.info(f"Deleted notification {notification_id}")
        return True

    def delete_old_notifications(
        self,
        user_id: str,
        days: int = 30
    ) -> int:
        """Delete notifications older than specified days.

        Args:
            user_id: The user ID
            days: Delete notifications older than this many days

        Returns:
            Number of notifications deleted
        """
        cutoff = datetime.now(timezone.utc) - timezone.timedelta(days=days)
        statement = select(Notification).where(
            Notification.user_id == user_id,
            Notification.created_at < cutoff
        )
        notifications = list(self.session.exec(statement).all())

        count = len(notifications)
        for notification in notifications:
            self.session.delete(notification)

        if count > 0:
            self.session.commit()
            logger.info(f"Deleted {count} old notifications for user {user_id}")

        return count
