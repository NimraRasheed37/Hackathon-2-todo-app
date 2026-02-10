"""Tags API routes."""

from typing import List, Literal

from fastapi import APIRouter, HTTPException, Query, status

from src.api.dependencies import CurrentUserDep, SessionDep
from src.core.exceptions import TaskNotFoundError
from src.core.logging_config import get_logger
from src.core.security import validate_user_authorization
from src.models.task import Task
from src.schemas.tag import (
    TagCreate,
    TagResponse,
    TagUpdate,
    TaskTagsUpdate,
    TaskTagsResponse,
)
from src.services.tag_service import TagService

router = APIRouter()
logger = get_logger(__name__)


def get_tag_service(session: SessionDep) -> TagService:
    """Get TagService instance with injected session."""
    return TagService(session)


@router.get(
    "/{user_id}/tags",
    response_model=List[TagResponse],
)
async def get_tags(
    user_id: str,
    current_user: CurrentUserDep,
    session: SessionDep,
    sort_by: Literal["name", "usage", "created"] = Query(default="name"),
):
    """Get all tags for a user."""
    validate_user_authorization(current_user.id, user_id)

    service = get_tag_service(session)
    tags = service.get_user_tags(user_id, sort_by=sort_by)
    return tags


@router.post(
    "/{user_id}/tags",
    response_model=TagResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_tag(
    user_id: str,
    tag_data: TagCreate,
    current_user: CurrentUserDep,
    session: SessionDep,
):
    """Create a new tag."""
    validate_user_authorization(current_user.id, user_id)

    service = get_tag_service(session)
    try:
        tag = service.create_tag(user_id, tag_data)
        logger.info(f"Created tag {tag.id} for user {user_id}")
        return tag
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get(
    "/{user_id}/tags/{tag_id}",
    response_model=TagResponse,
)
async def get_tag(
    user_id: str,
    tag_id: int,
    current_user: CurrentUserDep,
    session: SessionDep,
):
    """Get a tag by ID."""
    validate_user_authorization(current_user.id, user_id)

    service = get_tag_service(session)
    tag = service.get_tag(tag_id)

    if not tag or tag.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag not found",
        )

    return tag


@router.put(
    "/{user_id}/tags/{tag_id}",
    response_model=TagResponse,
)
async def update_tag(
    user_id: str,
    tag_id: int,
    tag_data: TagUpdate,
    current_user: CurrentUserDep,
    session: SessionDep,
):
    """Update a tag."""
    validate_user_authorization(current_user.id, user_id)

    service = get_tag_service(session)
    try:
        tag = service.update_tag(tag_id, user_id, tag_data)
        if not tag:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tag not found",
            )
        logger.info(f"Updated tag {tag_id}")
        return tag
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.delete(
    "/{user_id}/tags/{tag_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_tag(
    user_id: str,
    tag_id: int,
    current_user: CurrentUserDep,
    session: SessionDep,
):
    """Delete a tag and remove it from all tasks."""
    validate_user_authorization(current_user.id, user_id)

    service = get_tag_service(session)
    deleted = service.delete_tag(tag_id, user_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag not found",
        )

    logger.info(f"Deleted tag {tag_id}")


# Task-Tag association endpoints


@router.get(
    "/{user_id}/tasks/{task_id}/tags",
    response_model=TaskTagsResponse,
)
async def get_task_tags(
    user_id: str,
    task_id: int,
    current_user: CurrentUserDep,
    session: SessionDep,
):
    """Get all tags for a task."""
    validate_user_authorization(current_user.id, user_id)

    # Verify task exists and belongs to user
    task = session.get(Task, task_id)
    if not task:
        raise TaskNotFoundError(task_id, user_id)
    if task.user_id != user_id:
        raise TaskNotFoundError(task_id, user_id)

    service = get_tag_service(session)
    tags = service.get_task_tags(task_id)

    return TaskTagsResponse(task_id=task_id, tags=tags)


@router.post(
    "/{user_id}/tasks/{task_id}/tags",
    response_model=TaskTagsResponse,
)
async def set_task_tags(
    user_id: str,
    task_id: int,
    tag_data: TaskTagsUpdate,
    current_user: CurrentUserDep,
    session: SessionDep,
):
    """Set tags for a task (replaces existing tags)."""
    validate_user_authorization(current_user.id, user_id)

    # Verify task exists and belongs to user
    task = session.get(Task, task_id)
    if not task:
        raise TaskNotFoundError(task_id, user_id)
    if task.user_id != user_id:
        raise TaskNotFoundError(task_id, user_id)

    service = get_tag_service(session)
    tags = service.set_task_tags(task_id, tag_data.tag_ids, user_id)

    logger.info(f"Set {len(tags)} tags for task {task_id}")
    return TaskTagsResponse(task_id=task_id, tags=tags)


@router.delete(
    "/{user_id}/tasks/{task_id}/tags/{tag_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def remove_tag_from_task(
    user_id: str,
    task_id: int,
    tag_id: int,
    current_user: CurrentUserDep,
    session: SessionDep,
):
    """Remove a tag from a task."""
    validate_user_authorization(current_user.id, user_id)

    # Verify task exists and belongs to user
    task = session.get(Task, task_id)
    if not task:
        raise TaskNotFoundError(task_id, user_id)
    if task.user_id != user_id:
        raise TaskNotFoundError(task_id, user_id)

    service = get_tag_service(session)
    removed = service.remove_tag_from_task(task_id, tag_id, user_id)

    if not removed:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag not found or not assigned to this task",
        )

    logger.info(f"Removed tag {tag_id} from task {task_id}")
