"""Notifications API routes."""


from fastapi import APIRouter, HTTPException, Query, status

from src.api.dependencies import CurrentUserDep, SessionDep
from src.core.logging_config import get_logger
from src.core.security import validate_user_authorization
from src.schemas.reminder import (
    NotificationList,
    MarkNotificationsRead,
)
from src.services.notification_service import NotificationService

router = APIRouter()
logger = get_logger(__name__)


def get_notification_service(session: SessionDep) -> NotificationService:
    """Get NotificationService instance with injected session."""
    return NotificationService(session)


@router.get(
    "/{user_id}/notifications",
    response_model=NotificationList,
)
async def get_notifications(
    user_id: str,
    current_user: CurrentUserDep,
    session: SessionDep,
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    unread_only: bool = Query(default=False),
):
    """Get notifications for the current user."""
    validate_user_authorization(current_user.id, user_id)

    service = get_notification_service(session)
    notifications, total, unread_count = service.get_user_notifications(
        user_id=user_id,
        limit=limit,
        offset=offset,
        unread_only=unread_only,
    )

    return NotificationList(
        notifications=notifications,
        total=total,
        unread_count=unread_count,
    )


@router.post(
    "/{user_id}/notifications/mark-read",
    status_code=status.HTTP_200_OK,
)
async def mark_notifications_read(
    user_id: str,
    data: MarkNotificationsRead,
    current_user: CurrentUserDep,
    session: SessionDep,
):
    """Mark specific notifications as read."""
    validate_user_authorization(current_user.id, user_id)

    service = get_notification_service(session)
    count = service.mark_multiple_as_read(
        notification_ids=data.notification_ids,
        user_id=user_id,
    )

    return {"marked_read": count}


@router.post(
    "/{user_id}/notifications/mark-all-read",
    status_code=status.HTTP_200_OK,
)
async def mark_all_notifications_read(
    user_id: str,
    current_user: CurrentUserDep,
    session: SessionDep,
):
    """Mark all notifications as read."""
    validate_user_authorization(current_user.id, user_id)

    service = get_notification_service(session)
    count = service.mark_all_as_read(user_id=user_id)

    return {"marked_read": count}


@router.delete(
    "/{user_id}/notifications/{notification_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_notification(
    user_id: str,
    notification_id: int,
    current_user: CurrentUserDep,
    session: SessionDep,
):
    """Delete a notification."""
    validate_user_authorization(current_user.id, user_id)

    service = get_notification_service(session)
    deleted = service.delete_notification(
        notification_id=notification_id,
        user_id=user_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found",
        )
