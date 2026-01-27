"""API dependency injection functions."""

from typing import Annotated, Generator

from fastapi import Depends
from sqlmodel import Session

from src.api.middleware.auth import get_current_user
from src.database import get_session
from src.repositories.task_repository import TaskRepository
from src.schemas.auth import UserInfo


def get_task_repository(
    session: Annotated[Session, Depends(get_session)]
) -> Generator[TaskRepository, None, None]:
    """Get TaskRepository instance with injected session."""
    yield TaskRepository(session)


# Type aliases for dependency injection
SessionDep = Annotated[Session, Depends(get_session)]
TaskRepositoryDep = Annotated[TaskRepository, Depends(get_task_repository)]
CurrentUserDep = Annotated[UserInfo, Depends(get_current_user)]
