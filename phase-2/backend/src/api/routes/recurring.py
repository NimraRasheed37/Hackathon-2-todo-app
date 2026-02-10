"""Recurring tasks API routes."""

from fastapi import APIRouter, HTTPException, status

from src.api.dependencies import CurrentUserDep, SessionDep
from src.core.exceptions import TaskNotFoundError
from src.core.logging_config import get_logger
from src.core.security import validate_user_authorization
from src.models.task import Task
from src.schemas.recurrence import (
    RecurrenceCreate,
    RecurrenceResponse,
    RecurrenceUpdate,
)
from src.services.recurring_service import RecurringService

router = APIRouter()
logger = get_logger(__name__)


def get_recurring_service(session: SessionDep) -> RecurringService:
    """Get RecurringService instance with injected session."""
    return RecurringService(session)


@router.post(
    "/{user_id}/tasks/{task_id}/recurrence",
    response_model=RecurrenceResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_recurrence(
    user_id: str,
    task_id: int,
    recurrence_data: RecurrenceCreate,
    current_user: CurrentUserDep,
    session: SessionDep,
):
    """Create a recurrence pattern for a task.

    This makes the task recurring. When the task is completed,
    a new instance will be created based on the recurrence pattern.
    """
    validate_user_authorization(current_user.id, user_id)

    # Verify task exists and belongs to user
    task = session.get(Task, task_id)
    if not task:
        raise TaskNotFoundError(task_id, user_id)
    if task.user_id != user_id:
        raise TaskNotFoundError(task_id, user_id)

    service = get_recurring_service(session)

    # Check if task already has an active recurrence
    existing = service.get_task_recurrence(task_id)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task already has an active recurrence. Update or delete it first.",
        )

    try:
        recurrence = service.create_recurrence(
            task_id=task_id,
            pattern=recurrence_data.pattern,
            start_date=recurrence_data.start_date,
        )
        logger.info(f"Created recurrence {recurrence.id} for task {task_id}")
        return recurrence
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get(
    "/{user_id}/tasks/{task_id}/recurrence",
    response_model=RecurrenceResponse,
)
async def get_recurrence(
    user_id: str,
    task_id: int,
    current_user: CurrentUserDep,
    session: SessionDep,
):
    """Get the recurrence pattern for a task."""
    validate_user_authorization(current_user.id, user_id)

    # Verify task exists and belongs to user
    task = session.get(Task, task_id)
    if not task:
        raise TaskNotFoundError(task_id, user_id)
    if task.user_id != user_id:
        raise TaskNotFoundError(task_id, user_id)

    service = get_recurring_service(session)
    recurrence = service.get_task_recurrence(task_id)

    if not recurrence:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No recurrence pattern found for this task",
        )

    return recurrence


@router.put(
    "/{user_id}/tasks/{task_id}/recurrence",
    response_model=RecurrenceResponse,
)
async def update_recurrence(
    user_id: str,
    task_id: int,
    recurrence_update: RecurrenceUpdate,
    current_user: CurrentUserDep,
    session: SessionDep,
):
    """Update the recurrence pattern for a task."""
    validate_user_authorization(current_user.id, user_id)

    # Verify task exists and belongs to user
    task = session.get(Task, task_id)
    if not task:
        raise TaskNotFoundError(task_id, user_id)
    if task.user_id != user_id:
        raise TaskNotFoundError(task_id, user_id)

    service = get_recurring_service(session)
    recurrence = service.get_task_recurrence(task_id)

    if not recurrence:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No recurrence pattern found for this task",
        )

    updated = service.update_recurrence(
        recurrence_id=recurrence.id,
        pattern=recurrence_update.pattern,
        is_active=recurrence_update.is_active,
    )

    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recurrence not found",
        )

    logger.info(f"Updated recurrence {recurrence.id} for task {task_id}")
    return updated


@router.delete(
    "/{user_id}/tasks/{task_id}/recurrence",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_recurrence(
    user_id: str,
    task_id: int,
    current_user: CurrentUserDep,
    session: SessionDep,
):
    """Delete (deactivate) the recurrence pattern for a task.

    This stops the task from recurring. The task itself is not deleted.
    """
    validate_user_authorization(current_user.id, user_id)

    # Verify task exists and belongs to user
    task = session.get(Task, task_id)
    if not task:
        raise TaskNotFoundError(task_id, user_id)
    if task.user_id != user_id:
        raise TaskNotFoundError(task_id, user_id)

    service = get_recurring_service(session)
    recurrence = service.get_task_recurrence(task_id)

    if not recurrence:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No recurrence pattern found for this task",
        )

    service.delete_recurrence(recurrence.id)
    logger.info(f"Deleted recurrence {recurrence.id} for task {task_id}")
