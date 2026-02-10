"""Recurring task service for managing task recurrence patterns and spawning new instances."""

from datetime import datetime, timezone, timedelta
from typing import Optional, List
from dateutil.relativedelta import relativedelta

from sqlmodel import Session, select

from src.models.recurrence import TaskRecurrence
from src.models.task import Task
from src.schemas.recurrence import RecurrencePattern, RecurrenceFrequency
from src.core.logging_config import get_logger

logger = get_logger(__name__)


class RecurringService:
    """Service for managing recurring tasks."""

    def __init__(self, session: Session):
        self.session = session

    def create_recurrence(
        self,
        task_id: int,
        pattern: RecurrencePattern,
        start_date: Optional[datetime] = None
    ) -> TaskRecurrence:
        """Create a new recurrence pattern for a task.

        Args:
            task_id: The task to make recurring
            pattern: The recurrence pattern configuration
            start_date: Optional start date for the recurrence

        Returns:
            The created TaskRecurrence record
        """
        # Get the task to validate it exists
        task = self.session.get(Task, task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")

        # Determine start date
        if start_date is None:
            start_date = task.due_date if hasattr(task, 'due_date') and task.due_date else datetime.now(timezone.utc)

        # Calculate first next occurrence
        next_occurrence = self.calculate_next_occurrence(pattern, start_date)

        # Create recurrence record
        recurrence = TaskRecurrence(
            task_id=task_id,
            pattern=pattern.model_dump(),
            next_occurrence=next_occurrence,
            total_occurrences=0,
            is_active=True,
        )

        self.session.add(recurrence)
        self.session.commit()
        self.session.refresh(recurrence)

        logger.info(f"Created recurrence {recurrence.id} for task {task_id}")
        return recurrence

    def get_recurrence(self, recurrence_id: int) -> Optional[TaskRecurrence]:
        """Get a recurrence by ID."""
        return self.session.get(TaskRecurrence, recurrence_id)

    def get_task_recurrence(self, task_id: int) -> Optional[TaskRecurrence]:
        """Get the active recurrence for a task."""
        statement = select(TaskRecurrence).where(
            TaskRecurrence.task_id == task_id,
            TaskRecurrence.is_active == True
        )
        return self.session.exec(statement).first()

    def get_due_recurrences(self, before: datetime) -> List[TaskRecurrence]:
        """Get all active recurrences due before a given time.

        Args:
            before: The cutoff datetime

        Returns:
            List of recurrences that need to spawn new tasks
        """
        statement = select(TaskRecurrence).where(
            TaskRecurrence.is_active == True,
            TaskRecurrence.next_occurrence <= before
        )
        return list(self.session.exec(statement).all())

    def update_recurrence(
        self,
        recurrence_id: int,
        pattern: Optional[RecurrencePattern] = None,
        is_active: Optional[bool] = None
    ) -> Optional[TaskRecurrence]:
        """Update a recurrence pattern.

        Args:
            recurrence_id: The recurrence to update
            pattern: Optional new pattern
            is_active: Optional active status

        Returns:
            The updated recurrence or None if not found
        """
        recurrence = self.session.get(TaskRecurrence, recurrence_id)
        if not recurrence:
            return None

        if pattern is not None:
            recurrence.pattern = pattern.model_dump()
            # Recalculate next occurrence based on new pattern
            base_date = recurrence.last_generated or datetime.now(timezone.utc)
            recurrence.next_occurrence = self.calculate_next_occurrence(pattern, base_date)

        if is_active is not None:
            recurrence.is_active = is_active

        self.session.add(recurrence)
        self.session.commit()
        self.session.refresh(recurrence)

        logger.info(f"Updated recurrence {recurrence_id}")
        return recurrence

    def delete_recurrence(self, recurrence_id: int) -> bool:
        """Delete a recurrence (soft delete by setting inactive)."""
        recurrence = self.session.get(TaskRecurrence, recurrence_id)
        if not recurrence:
            return False

        recurrence.is_active = False
        self.session.add(recurrence)
        self.session.commit()

        logger.info(f"Deactivated recurrence {recurrence_id}")
        return True

    def spawn_next_task(self, recurrence: TaskRecurrence) -> Optional[Task]:
        """Spawn the next instance of a recurring task.

        Args:
            recurrence: The recurrence to spawn from

        Returns:
            The newly created task instance or None if recurrence is complete
        """
        # Check if recurrence is still active
        if not recurrence.is_active:
            logger.info(f"Recurrence {recurrence.id} is inactive, skipping spawn")
            return None

        pattern = RecurrencePattern(**recurrence.pattern)

        # Check end conditions
        if pattern.end_date and recurrence.next_occurrence and recurrence.next_occurrence > pattern.end_date:
            logger.info(f"Recurrence {recurrence.id} reached end_date, deactivating")
            recurrence.is_active = False
            self.session.add(recurrence)
            self.session.commit()
            return None

        if pattern.max_occurrences and recurrence.total_occurrences >= pattern.max_occurrences:
            logger.info(f"Recurrence {recurrence.id} reached max_occurrences, deactivating")
            recurrence.is_active = False
            self.session.add(recurrence)
            self.session.commit()
            return None

        # Get the parent task
        parent_task = self.session.get(Task, recurrence.task_id)
        if not parent_task:
            logger.error(f"Parent task {recurrence.task_id} not found for recurrence {recurrence.id}")
            return None

        # Create new task instance
        new_task = Task(
            user_id=parent_task.user_id,
            title=parent_task.title,
            description=parent_task.description,
            completed=False,
            # Phase 5 fields (if they exist on the model)
        )

        # Copy Phase 5 fields if they exist
        if hasattr(parent_task, 'priority'):
            new_task.priority = parent_task.priority
        if hasattr(parent_task, 'due_date') and recurrence.next_occurrence:
            new_task.due_date = recurrence.next_occurrence
        if hasattr(parent_task, 'parent_task_id'):
            new_task.parent_task_id = parent_task.id
        if hasattr(parent_task, 'occurrence_number'):
            new_task.occurrence_number = recurrence.total_occurrences + 1

        self.session.add(new_task)

        # Update recurrence
        recurrence.total_occurrences += 1
        recurrence.last_generated = datetime.now(timezone.utc)
        recurrence.next_occurrence = self.calculate_next_occurrence(
            pattern,
            recurrence.next_occurrence or datetime.now(timezone.utc)
        )

        self.session.add(recurrence)
        self.session.commit()
        self.session.refresh(new_task)

        logger.info(f"Spawned task {new_task.id} from recurrence {recurrence.id}")
        return new_task

    def calculate_next_occurrence(
        self,
        pattern: RecurrencePattern,
        from_date: datetime
    ) -> datetime:
        """Calculate the next occurrence date based on the pattern.

        Args:
            pattern: The recurrence pattern
            from_date: The date to calculate from

        Returns:
            The next occurrence datetime
        """
        interval = pattern.interval

        if pattern.frequency == RecurrenceFrequency.DAILY:
            return from_date + timedelta(days=interval)

        elif pattern.frequency == RecurrenceFrequency.WEEKLY:
            if pattern.days_of_week:
                # Find next matching day of week
                current_weekday = from_date.weekday()
                days_ahead = None

                for day in sorted(pattern.days_of_week):
                    if day > current_weekday:
                        days_ahead = day - current_weekday
                        break

                if days_ahead is None:
                    # Wrap to next week
                    days_ahead = (7 - current_weekday) + min(pattern.days_of_week) + (7 * (interval - 1))

                return from_date + timedelta(days=days_ahead)
            else:
                return from_date + timedelta(weeks=interval)

        elif pattern.frequency == RecurrenceFrequency.MONTHLY:
            next_date = from_date + relativedelta(months=interval)
            if pattern.day_of_month:
                # Try to set the specific day, handling month-end cases
                try:
                    next_date = next_date.replace(day=pattern.day_of_month)
                except ValueError:
                    # If day doesn't exist in month, use last day
                    next_date = next_date + relativedelta(day=31)
            return next_date

        elif pattern.frequency == RecurrenceFrequency.YEARLY:
            return from_date + relativedelta(years=interval)

        elif pattern.frequency == RecurrenceFrequency.CUSTOM:
            # For custom, use daily with the specified interval
            return from_date + timedelta(days=interval)

        # Default fallback
        return from_date + timedelta(days=1)

    def process_completed_task(self, task_id: int) -> Optional[Task]:
        """Process a completed task and spawn next instance if recurring.

        This should be called when a task is marked as completed.

        Args:
            task_id: The completed task ID

        Returns:
            The newly spawned task if the task was recurring, None otherwise
        """
        recurrence = self.get_task_recurrence(task_id)
        if recurrence:
            return self.spawn_next_task(recurrence)
        return None
