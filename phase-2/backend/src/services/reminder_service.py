"""Reminder service for scheduling and managing task reminders."""

from datetime import datetime, timezone, timedelta
from typing import Optional, List

from sqlmodel import Session, select

from src.models.reminder import TaskReminder
from src.models.task import Task
from src.schemas.reminder import ReminderCreate, ReminderType
from src.core.logging_config import get_logger

logger = get_logger(__name__)


class ReminderService:
    """Service for managing task reminders."""

    def __init__(self, session: Session):
        self.session = session

    def schedule_reminder(
        self,
        task_id: int,
        user_id: str,
        reminder_config: ReminderCreate,
        task_due_date: Optional[datetime] = None,
    ) -> TaskReminder:
        """Schedule a new reminder for a task.

        Args:
            task_id: The task ID to remind about
            user_id: The user to notify
            reminder_config: Reminder configuration
            task_due_date: Task due date (required for relative reminders)

        Returns:
            The created TaskReminder
        """
        # Calculate scheduled_at based on reminder type
        if reminder_config.reminder_type == ReminderType.RELATIVE:
            if task_due_date is None:
                raise ValueError("Task due date is required for relative reminders")
            scheduled_at = task_due_date - timedelta(minutes=reminder_config.relative_minutes)
        else:
            scheduled_at = reminder_config.absolute_time

        # Don't schedule reminders in the past
        now = datetime.now(timezone.utc)
        if scheduled_at < now:
            logger.warning(
                f"Reminder scheduled_at {scheduled_at} is in the past, "
                f"adjusting to now"
            )
            scheduled_at = now + timedelta(minutes=1)

        reminder = TaskReminder(
            task_id=task_id,
            user_id=user_id,
            reminder_type=reminder_config.reminder_type.value,
            relative_minutes=reminder_config.relative_minutes,
            absolute_time=reminder_config.absolute_time,
            channels=[c.value for c in reminder_config.channels],
            status="pending",
            scheduled_at=scheduled_at,
        )

        self.session.add(reminder)
        self.session.commit()
        self.session.refresh(reminder)

        logger.info(f"Scheduled reminder {reminder.id} for task {task_id} at {scheduled_at}")
        return reminder

    def get_reminder(self, reminder_id: int) -> Optional[TaskReminder]:
        """Get a reminder by ID."""
        return self.session.get(TaskReminder, reminder_id)

    def get_task_reminders(self, task_id: int) -> List[TaskReminder]:
        """Get all reminders for a task."""
        statement = select(TaskReminder).where(
            TaskReminder.task_id == task_id,
            TaskReminder.status != "cancelled"
        ).order_by(TaskReminder.scheduled_at)
        return list(self.session.exec(statement).all())

    def get_user_reminders(
        self,
        user_id: str,
        status: Optional[str] = None
    ) -> List[TaskReminder]:
        """Get all reminders for a user."""
        statement = select(TaskReminder).where(TaskReminder.user_id == user_id)
        if status:
            statement = statement.where(TaskReminder.status == status)
        statement = statement.order_by(TaskReminder.scheduled_at)
        return list(self.session.exec(statement).all())

    def check_due_reminders(
        self,
        before: Optional[datetime] = None
    ) -> List[TaskReminder]:
        """Get all pending reminders due before a given time.

        Args:
            before: Cutoff time (defaults to now)

        Returns:
            List of due reminders
        """
        if before is None:
            before = datetime.now(timezone.utc)

        statement = select(TaskReminder).where(
            TaskReminder.status == "pending",
            TaskReminder.scheduled_at <= before
        ).order_by(TaskReminder.scheduled_at)

        return list(self.session.exec(statement).all())

    def mark_reminder_sent(self, reminder_id: int) -> Optional[TaskReminder]:
        """Mark a reminder as sent."""
        reminder = self.session.get(TaskReminder, reminder_id)
        if not reminder:
            return None

        reminder.status = "sent"
        reminder.sent_at = datetime.now(timezone.utc)
        self.session.add(reminder)
        self.session.commit()
        self.session.refresh(reminder)

        logger.info(f"Marked reminder {reminder_id} as sent")
        return reminder

    def cancel_reminder(self, reminder_id: int) -> bool:
        """Cancel a pending reminder."""
        reminder = self.session.get(TaskReminder, reminder_id)
        if not reminder:
            return False

        if reminder.status != "pending":
            logger.warning(f"Cannot cancel reminder {reminder_id} with status {reminder.status}")
            return False

        reminder.status = "cancelled"
        self.session.add(reminder)
        self.session.commit()

        logger.info(f"Cancelled reminder {reminder_id}")
        return True

    def cancel_task_reminders(self, task_id: int) -> int:
        """Cancel all pending reminders for a task.

        Args:
            task_id: The task ID

        Returns:
            Number of reminders cancelled
        """
        statement = select(TaskReminder).where(
            TaskReminder.task_id == task_id,
            TaskReminder.status == "pending"
        )
        reminders = list(self.session.exec(statement).all())

        count = 0
        for reminder in reminders:
            reminder.status = "cancelled"
            self.session.add(reminder)
            count += 1

        if count > 0:
            self.session.commit()
            logger.info(f"Cancelled {count} reminders for task {task_id}")

        return count

    def update_task_reminders(
        self,
        task_id: int,
        new_due_date: datetime
    ) -> int:
        """Update scheduled times for relative reminders when task due date changes.

        Args:
            task_id: The task ID
            new_due_date: The new task due date

        Returns:
            Number of reminders updated
        """
        statement = select(TaskReminder).where(
            TaskReminder.task_id == task_id,
            TaskReminder.status == "pending",
            TaskReminder.reminder_type == "relative"
        )
        reminders = list(self.session.exec(statement).all())

        count = 0
        for reminder in reminders:
            if reminder.relative_minutes:
                new_scheduled = new_due_date - timedelta(minutes=reminder.relative_minutes)
                reminder.scheduled_at = new_scheduled
                self.session.add(reminder)
                count += 1

        if count > 0:
            self.session.commit()
            logger.info(f"Updated {count} relative reminders for task {task_id}")

        return count

    def delete_reminder(self, reminder_id: int) -> bool:
        """Permanently delete a reminder."""
        reminder = self.session.get(TaskReminder, reminder_id)
        if not reminder:
            return False

        self.session.delete(reminder)
        self.session.commit()

        logger.info(f"Deleted reminder {reminder_id}")
        return True
