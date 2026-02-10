"""Task repository for database operations."""

from datetime import datetime, timezone
from typing import List, Literal, Optional

from sqlmodel import Session, select

from src.core.exceptions import TaskNotFoundError
from src.models.task import Task
from src.schemas.task import TaskCreate, TaskUpdate


class TaskRepository:
    """Repository for task database operations."""

    def __init__(self, session: Session):
        self.session = session

    def get_all_by_user(
        self,
        user_id: str,
        status: Literal["all", "pending", "completed"] = "all",
        sort: Literal["created", "title", "updated", "priority", "due_date"] = "created",
    ) -> List[Task]:
        """Get all tasks for a user with optional filtering and sorting."""
        statement = select(Task).where(Task.user_id == user_id)

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
        elif sort == "priority":
            # Sort by priority: critical > high > medium > low > none
            # Using a custom order: critical=0, high=1, medium=2, low=3, none=4
            from sqlalchemy import case
            priority_order = case(
                (Task.priority == "critical", 0),
                (Task.priority == "high", 1),
                (Task.priority == "medium", 2),
                (Task.priority == "low", 3),
                else_=4
            )
            statement = statement.order_by(priority_order, Task.created_at.desc())
        elif sort == "due_date":
            # Sort by due date, null values last
            from sqlalchemy import nulls_last
            statement = statement.order_by(nulls_last(Task.due_date.asc()))
        else:
            statement = statement.order_by(Task.created_at.desc())

        return list(self.session.exec(statement).all())

    def get_by_id_and_user(self, task_id: int, user_id: str) -> Optional[Task]:
        """Get a task by ID with ownership validation."""
        statement = select(Task).where(
            Task.id == task_id,
            Task.user_id == user_id,
        )
        return self.session.exec(statement).first()

    def create(self, user_id: str, task_data: TaskCreate) -> Task:
        """Create a new task for a user."""
        task = Task(
            user_id=user_id,
            title=task_data.title,
            description=task_data.description,
            priority=task_data.priority,
            due_date=task_data.due_date,
        )
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def update(self, task_id: int, user_id: str, task_update: TaskUpdate) -> Task:
        """Update an existing task with ownership validation."""
        task = self.get_by_id_and_user(task_id, user_id)
        if not task:
            raise TaskNotFoundError(task_id, user_id)

        # Update only provided fields
        update_data = task_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(task, key, value)

        task.updated_at = datetime.now(timezone.utc)
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def toggle_complete(self, task_id: int, user_id: str) -> Task:
        """Toggle task completion status with ownership validation."""
        task = self.get_by_id_and_user(task_id, user_id)
        if not task:
            raise TaskNotFoundError(task_id, user_id)

        task.completed = not task.completed
        task.updated_at = datetime.now(timezone.utc)
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def delete(self, task_id: int, user_id: str) -> bool:
        """Delete a task with ownership validation."""
        task = self.get_by_id_and_user(task_id, user_id)
        if not task:
            raise TaskNotFoundError(task_id, user_id)

        self.session.delete(task)
        self.session.commit()
        return True
