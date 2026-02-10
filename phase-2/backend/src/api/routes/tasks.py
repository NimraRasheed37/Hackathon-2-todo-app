"""Task API routes with authentication and authorization."""

from typing import List, Literal

from fastapi import APIRouter, HTTPException, Query, status, BackgroundTasks

from src.api.dependencies import CurrentUserDep, TaskRepositoryDep
from src.core.exceptions import AuthorizationError, TaskNotFoundError
from src.core.logging_config import get_logger
from src.core.security import log_security_event, validate_user_authorization
from src.events.producer import publish_event, publish_to_audit
from src.events.schemas import TaskEvent
from src.schemas.task import TaskCreate, TaskRead, TaskUpdate

router = APIRouter()
logger = get_logger(__name__)


@router.get("/{user_id}/tasks", response_model=List[TaskRead])
async def list_tasks(
    user_id: str,
    current_user: CurrentUserDep,
    repository: TaskRepositoryDep,
    status_filter: Literal["all", "pending", "completed"] = Query(
        default="all", alias="status"
    ),
    sort: Literal["created", "title", "updated", "priority", "due_date"] = Query(default="created"),
):
    """List all tasks for a user with optional filtering and sorting."""
    # Authorization check: user can only access their own tasks
    validate_user_authorization(current_user.id, user_id)

    # Validate query parameters
    valid_status = ["all", "pending", "completed"]
    valid_sort = ["created", "title", "updated", "priority", "due_date"]

    if status_filter not in valid_status:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status value. Must be one of: {', '.join(valid_status)}",
        )

    if sort not in valid_sort:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid sort value. Must be one of: {', '.join(valid_sort)}",
        )

    tasks = repository.get_all_by_user(user_id, status=status_filter, sort=sort)
    return tasks


@router.post(
    "/{user_id}/tasks",
    response_model=TaskRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_task(
    user_id: str,
    task_data: TaskCreate,
    current_user: CurrentUserDep,
    repository: TaskRepositoryDep,
    background_tasks: BackgroundTasks,
):
    """Create a new task for a user."""
    # Authorization check: user can only create tasks for themselves
    validate_user_authorization(current_user.id, user_id)

    task = repository.create(user_id, task_data)

    # Publish task created event in background
    event = TaskEvent.task_created(
        task_id=str(task.id),
        user_id=user_id,
        title=task.title,
        description=task.description,
        priority=task.priority.value if task.priority else "none",
        due_date=task.due_date.isoformat() if task.due_date else None,
    )
    background_tasks.add_task(publish_event, event)
    background_tasks.add_task(publish_to_audit, event)

    return task


@router.get("/{user_id}/tasks/{task_id}", response_model=TaskRead)
async def get_task(
    user_id: str,
    task_id: int,
    current_user: CurrentUserDep,
    repository: TaskRepositoryDep,
):
    """Get a single task by ID with ownership validation."""
    # Authorization check: user can only access their own tasks
    validate_user_authorization(current_user.id, user_id)

    task = repository.get_by_id_and_user(task_id, user_id)
    if not task:
        raise TaskNotFoundError(task_id, user_id)
    return task


@router.put("/{user_id}/tasks/{task_id}", response_model=TaskRead)
async def update_task(
    user_id: str,
    task_id: int,
    task_update: TaskUpdate,
    current_user: CurrentUserDep,
    repository: TaskRepositoryDep,
    background_tasks: BackgroundTasks,
):
    """Update a task's title and/or description."""
    # Authorization check: user can only update their own tasks
    validate_user_authorization(current_user.id, user_id)

    try:
        task = repository.update(task_id, user_id, task_update)

        # Publish task updated event in background
        changes = task_update.model_dump(exclude_unset=True)
        event = TaskEvent.task_updated(
            task_id=str(task_id),
            user_id=user_id,
            changes=changes,
        )
        background_tasks.add_task(publish_event, event)
        background_tasks.add_task(publish_to_audit, event)

        return task
    except TaskNotFoundError:
        raise


@router.patch("/{user_id}/tasks/{task_id}/complete", response_model=TaskRead)
async def toggle_task_completion(
    user_id: str,
    task_id: int,
    current_user: CurrentUserDep,
    repository: TaskRepositoryDep,
    background_tasks: BackgroundTasks,
):
    """Toggle task completion status."""
    # Authorization check: user can only toggle their own tasks
    validate_user_authorization(current_user.id, user_id)

    try:
        task = repository.toggle_complete(task_id, user_id)

        # Publish task completed event if task was marked as complete
        if task.completed:
            # Check if task has recurrence pattern
            has_recurrence = getattr(task, 'recurrence_pattern', None) is not None
            event = TaskEvent.task_completed(
                task_id=str(task_id),
                user_id=user_id,
                has_recurrence=has_recurrence,
            )
            background_tasks.add_task(publish_event, event)
            background_tasks.add_task(publish_to_audit, event)
        else:
            # Task was uncompleted - publish update event
            event = TaskEvent.task_updated(
                task_id=str(task_id),
                user_id=user_id,
                changes={"completed": False},
            )
            background_tasks.add_task(publish_event, event)

        return task
    except TaskNotFoundError:
        raise


@router.delete(
    "/{user_id}/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_task(
    user_id: str,
    task_id: int,
    current_user: CurrentUserDep,
    repository: TaskRepositoryDep,
    background_tasks: BackgroundTasks,
):
    """Delete a task permanently."""
    # Authorization check: user can only delete their own tasks
    validate_user_authorization(current_user.id, user_id)

    try:
        repository.delete(task_id, user_id)

        # Publish task deleted event in background
        event = TaskEvent.task_deleted(
            task_id=str(task_id),
            user_id=user_id,
        )
        background_tasks.add_task(publish_event, event)
        background_tasks.add_task(publish_to_audit, event)
    except TaskNotFoundError:
        raise
