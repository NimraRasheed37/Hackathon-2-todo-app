"""Reminders API routes."""

from typing import List

from fastapi import APIRouter, HTTPException, status

from src.api.dependencies import CurrentUserDep, SessionDep
from src.core.exceptions import TaskNotFoundError
from src.core.logging_config import get_logger
from src.core.security import validate_user_authorization
from src.models.task import Task
from src.schemas.reminder import ReminderCreate, ReminderResponse
from src.services.reminder_service import ReminderService

router = APIRouter()
logger = get_logger(__name__)


def get_reminder_service(session: SessionDep) -> ReminderService:
    """Get ReminderService instance with injected session."""
    return ReminderService(session)


@router.post(
    "/{user_id}/tasks/{task_id}/reminders",
    response_model=ReminderResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_reminder(
    user_id: str,
    task_id: int,
    reminder_data: ReminderCreate,
    current_user: CurrentUserDep,
    session: SessionDep,
):
    """Create a reminder for a task.

    For relative reminders, the task must have a due date.
    """
    validate_user_authorization(current_user.id, user_id)

    # Verify task exists and belongs to user
    task = session.get(Task, task_id)
    if not task:
        raise TaskNotFoundError(task_id, user_id)
    if task.user_id != user_id:
        raise TaskNotFoundError(task_id, user_id)

    # Get task due date for relative reminders
    task_due_date = getattr(task, 'due_date', None)

    service = get_reminder_service(session)

    try:
        reminder = service.schedule_reminder(
            task_id=task_id,
            user_id=user_id,
            reminder_config=reminder_data,
            task_due_date=task_due_date,
        )
        logger.info(f"Created reminder {reminder.id} for task {task_id}")
        return reminder
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get(
    "/{user_id}/tasks/{task_id}/reminders",
    response_model=List[ReminderResponse],
)
async def get_task_reminders(
    user_id: str,
    task_id: int,
    current_user: CurrentUserDep,
    session: SessionDep,
):
    """Get all reminders for a task."""
    validate_user_authorization(current_user.id, user_id)

    # Verify task exists and belongs to user
    task = session.get(Task, task_id)
    if not task:
        raise TaskNotFoundError(task_id, user_id)
    if task.user_id != user_id:
        raise TaskNotFoundError(task_id, user_id)

    service = get_reminder_service(session)
    reminders = service.get_task_reminders(task_id)
    return reminders


@router.delete(
    "/{user_id}/tasks/{task_id}/reminders/{reminder_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_reminder(
    user_id: str,
    task_id: int,
    reminder_id: int,
    current_user: CurrentUserDep,
    session: SessionDep,
):
    """Delete (cancel) a reminder."""
    validate_user_authorization(current_user.id, user_id)

    # Verify task exists and belongs to user
    task = session.get(Task, task_id)
    if not task:
        raise TaskNotFoundError(task_id, user_id)
    if task.user_id != user_id:
        raise TaskNotFoundError(task_id, user_id)

    service = get_reminder_service(session)
    reminder = service.get_reminder(reminder_id)

    if not reminder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reminder not found",
        )

    if reminder.task_id != task_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reminder not found for this task",
        )

    service.delete_reminder(reminder_id)
    logger.info(f"Deleted reminder {reminder_id} for task {task_id}")
