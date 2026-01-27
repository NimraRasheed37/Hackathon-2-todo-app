"""Task repository for database operations."""

import uuid
from datetime import datetime, timezone
from typing import List, Literal, Optional, Union

from sqlmodel import Session, select

from src.core.exceptions import TaskNotFoundError
from src.models.task import Task
from src.schemas.task import TaskCreate, TaskUpdate


class TaskRepository:
    """Repository for task database operations."""

    def __init__(self, session: Session):
        self.session = session

    def _parse_user_id(self, user_id: Union[str, uuid.UUID]) -> uuid.UUID:
        """Parse user_id to UUID."""
        if isinstance(user_id, uuid.UUID):
            return user_id
        try:
            return uuid.UUID(user_id)
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid user_id format: {user_id}") from e

    def get_all_by_user(
        self,
        user_id: Union[str, uuid.UUID],
        status: Literal["all", "pending", "completed"] = "all",
        sort: Literal["created", "title", "updated"] = "created",
    ) -> List[Task]:
        """Get all tasks for a user with optional filtering and sorting."""
        parsed_user_id = self._parse_user_id(user_id)
        statement = select(Task).where(Task.user_id == parsed_user_id)

        # Apply status filter
        if status == "pending":
            statement = statement.where(Task.completed == False)  # noqa: E712
        elif status == "completed":
            statement = statement.where(Task.completed == True)  # noqa: E712

        # Apply sorting
        if sort == "title":
            statement = statement.order_by(Task.title)
        elif sort == "updated":
            statement = statement.order_by(Task.updated_at.desc())
        else:
            statement = statement.order_by(Task.created_at.desc())

        return list(self.session.exec(statement).all())

    def get_by_id_and_user(
        self, task_id: int, user_id: Union[str, uuid.UUID]
    ) -> Optional[Task]:
        """Get a task by ID with ownership validation."""
        parsed_user_id = self._parse_user_id(user_id)
        statement = select(Task).where(
            Task.id == task_id,
            Task.user_id == parsed_user_id,
        )
        return self.session.exec(statement).first()

    def create(self, user_id: Union[str, uuid.UUID], task_data: TaskCreate) -> Task:
        """Create a new task for a user."""
        parsed_user_id = self._parse_user_id(user_id)
        task = Task(
            user_id=parsed_user_id,
            title=task_data.title,
            description=task_data.description,
        )
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def update(
        self, task_id: int, user_id: Union[str, uuid.UUID], task_update: TaskUpdate
    ) -> Task:
        """Update an existing task with ownership validation."""
        task = self.get_by_id_and_user(task_id, user_id)
        if not task:
            raise TaskNotFoundError(task_id, str(user_id))

        # Update only provided fields
        update_data = task_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(task, key, value)

        task.updated_at = datetime.now(timezone.utc)
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def toggle_complete(self, task_id: int, user_id: Union[str, uuid.UUID]) -> Task:
        """Toggle task completion status with ownership validation."""
        task = self.get_by_id_and_user(task_id, user_id)
        if not task:
            raise TaskNotFoundError(task_id, str(user_id))

        task.completed = not task.completed
        task.updated_at = datetime.now(timezone.utc)
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def delete(self, task_id: int, user_id: Union[str, uuid.UUID]) -> bool:
        """Delete a task with ownership validation."""
        task = self.get_by_id_and_user(task_id, user_id)
        if not task:
            raise TaskNotFoundError(task_id, str(user_id))

        self.session.delete(task)
        self.session.commit()
        return True
