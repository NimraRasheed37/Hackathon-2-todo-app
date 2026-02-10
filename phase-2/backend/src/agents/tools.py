"""AI tool implementations for task management."""

from datetime import datetime
from typing import Any, Dict, List, Literal, Optional

from sqlmodel import Session

from src.core.logging_config import get_logger
from src.models.task import Task
from src.repositories.task_repository import TaskRepository
from src.schemas.task import Priority, TaskCreate, TaskUpdate

logger = get_logger(__name__)


def find_task_by_identifier(
    tasks: List[Task], identifier: str
) -> tuple[Optional[Task], Optional[List[Task]]]:
    """
    Find a task by ID or partial title match.

    Returns:
        Tuple of (matched_task, ambiguous_candidates)
        - If exact match: (task, None)
        - If ambiguous: (None, list of candidates)
        - If not found: (None, None)
    """
    # Try to parse as integer ID first
    try:
        task_id = int(identifier)
        for task in tasks:
            if task.id == task_id:
                return task, None
        return None, None
    except ValueError:
        pass

    # Try partial title match (case-insensitive)
    identifier_lower = identifier.lower()
    matches = [t for t in tasks if identifier_lower in t.title.lower()]

    if len(matches) == 1:
        return matches[0], None
    elif len(matches) > 1:
        return None, matches
    else:
        return None, None


def add_task(
    session: Session,
    user_id: str,
    title: str,
    description: Optional[str] = None,
    priority: Optional[str] = None,
    due_date: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Add a new task for the user.

    Args:
        session: Database session
        user_id: The authenticated user's ID
        title: Task title (max 500 chars)
        description: Optional task description
        priority: Optional priority level (none, low, medium, high, critical)
        due_date: Optional due date in ISO 8601 format

    Returns:
        Tool response dict with success status and data
    """
    try:
        # Validate title length
        if len(title) > 500:
            return {
                "success": False,
                "error": "Task title cannot exceed 500 characters",
                "message": "Failed to create task"
            }

        if not title.strip():
            return {
                "success": False,
                "error": "Task title cannot be empty",
                "message": "Failed to create task"
            }

        # Parse priority
        task_priority = Priority.NONE
        if priority:
            try:
                task_priority = Priority(priority.lower())
            except ValueError:
                return {
                    "success": False,
                    "error": "VALIDATION_ERROR",
                    "message": f"Invalid priority '{priority}'. Use: none, low, medium, high, critical"
                }

        # Parse due date
        task_due_date = None
        if due_date:
            try:
                task_due_date = datetime.fromisoformat(due_date.replace("Z", "+00:00"))
            except (ValueError, TypeError):
                return {
                    "success": False,
                    "error": "VALIDATION_ERROR",
                    "message": f"Invalid date format '{due_date}'. Use ISO 8601 format (e.g., 2025-12-31T23:59:00)"
                }

        repo = TaskRepository(session)
        task_data = TaskCreate(
            title=title.strip(),
            description=description,
            priority=task_priority,
            due_date=task_due_date,
        )
        task = repo.create(user_id, task_data)

        logger.info(f"Created task {task.id} for user {user_id}")

        result_data = {
            "task_id": task.id,
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "priority": task.priority.value if hasattr(task.priority, 'value') else str(task.priority),
        }
        if task.due_date:
            result_data["due_date"] = task.due_date.isoformat()

        return {
            "success": True,
            "data": result_data,
            "message": "Task created successfully"
        }
    except Exception as e:
        logger.error(f"Error creating task: {e}")
        return {
            "success": False,
            "error": "DATABASE_ERROR",
            "message": "Failed to create task due to a database error"
        }


def list_tasks(
    session: Session,
    user_id: str,
    status: Literal["all", "pending", "completed"] = "all",
) -> Dict[str, Any]:
    """
    List all tasks for the user, optionally filtered by status.

    Args:
        session: Database session
        user_id: The authenticated user's ID
        status: Filter by 'all', 'pending', or 'completed'

    Returns:
        Tool response dict with success status and task list
    """
    try:
        repo = TaskRepository(session)
        tasks = repo.get_all_by_user(user_id, status=status)

        task_list = []
        for t in tasks:
            task_info = {
                "id": t.id,
                "title": t.title,
                "description": t.description,
                "completed": t.completed,
                "priority": t.priority.value if hasattr(t.priority, 'value') else str(t.priority),
            }
            if t.due_date:
                task_info["due_date"] = t.due_date.isoformat()
            task_list.append(task_info)

        return {
            "success": True,
            "data": {
                "tasks": task_list,
                "count": len(task_list),
            },
            "message": f"Found {len(task_list)} tasks" if task_list else "No tasks found"
        }
    except Exception as e:
        logger.error(f"Error listing tasks: {e}")
        return {
            "success": False,
            "error": "DATABASE_ERROR",
            "message": "Failed to list tasks due to a database error"
        }


def complete_task(
    session: Session,
    user_id: str,
    task_identifier: str,
) -> Dict[str, Any]:
    """
    Mark a task as completed.

    Args:
        session: Database session
        user_id: The authenticated user's ID
        task_identifier: Task ID or partial title to match

    Returns:
        Tool response dict with success status and task data
    """
    try:
        repo = TaskRepository(session)
        tasks = repo.get_all_by_user(user_id)

        task, candidates = find_task_by_identifier(tasks, task_identifier)

        if candidates:
            return {
                "success": False,
                "error": "AMBIGUOUS",
                "data": {
                    "candidates": [{"id": t.id, "title": t.title} for t in candidates[:5]]
                },
                "message": f"Multiple tasks match '{task_identifier}'. Please be more specific."
            }

        if not task:
            return {
                "success": False,
                "error": "NOT_FOUND",
                "message": f"No task found matching '{task_identifier}'"
            }

        if task.completed:
            return {
                "success": True,
                "data": {
                    "task_id": task.id,
                    "title": task.title,
                    "completed": True,
                },
                "message": f"Task '{task.title}' was already completed"
            }

        # Mark as completed
        updated_task = repo.toggle_complete(task.id, user_id)

        logger.info(f"Completed task {task.id} for user {user_id}")

        return {
            "success": True,
            "data": {
                "task_id": updated_task.id,
                "title": updated_task.title,
                "completed": updated_task.completed,
            },
            "message": "Task marked as completed"
        }
    except Exception as e:
        logger.error(f"Error completing task: {e}")
        return {
            "success": False,
            "error": "DATABASE_ERROR",
            "message": "Failed to complete task due to a database error"
        }


def delete_task(
    session: Session,
    user_id: str,
    task_identifier: str,
) -> Dict[str, Any]:
    """
    Delete a task permanently.

    Args:
        session: Database session
        user_id: The authenticated user's ID
        task_identifier: Task ID or partial title to match

    Returns:
        Tool response dict with success status
    """
    try:
        repo = TaskRepository(session)
        tasks = repo.get_all_by_user(user_id)

        task, candidates = find_task_by_identifier(tasks, task_identifier)

        if candidates:
            return {
                "success": False,
                "error": "AMBIGUOUS",
                "data": {
                    "candidates": [{"id": t.id, "title": t.title} for t in candidates[:5]]
                },
                "message": f"Multiple tasks match '{task_identifier}'. Please be more specific."
            }

        if not task:
            return {
                "success": False,
                "error": "NOT_FOUND",
                "message": f"No task found matching '{task_identifier}'"
            }

        task_title = task.title
        task_id = task.id
        repo.delete(task.id, user_id)

        logger.info(f"Deleted task {task_id} for user {user_id}")

        return {
            "success": True,
            "data": {
                "task_id": task_id,
                "title": task_title,
            },
            "message": "Task deleted successfully"
        }
    except Exception as e:
        logger.error(f"Error deleting task: {e}")
        return {
            "success": False,
            "error": "DATABASE_ERROR",
            "message": "Failed to delete task due to a database error"
        }


def update_task(
    session: Session,
    user_id: str,
    task_identifier: str,
    new_title: Optional[str] = None,
    new_description: Optional[str] = None,
    new_priority: Optional[str] = None,
    new_due_date: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Update a task's title, description, priority, or due date.

    Args:
        session: Database session
        user_id: The authenticated user's ID
        task_identifier: Task ID or partial title to match
        new_title: New title for the task
        new_description: New description for the task
        new_priority: New priority level (none, low, medium, high, critical)
        new_due_date: New due date in ISO 8601 format, or 'clear' to remove

    Returns:
        Tool response dict with success status and updated task data
    """
    try:
        if not new_title and new_description is None and not new_priority and not new_due_date:
            return {
                "success": False,
                "error": "VALIDATION_ERROR",
                "message": "No updates provided. Please specify a new title, description, priority, or due date."
            }

        if new_title and len(new_title) > 500:
            return {
                "success": False,
                "error": "VALIDATION_ERROR",
                "message": "Task title cannot exceed 500 characters"
            }

        repo = TaskRepository(session)
        tasks = repo.get_all_by_user(user_id)

        task, candidates = find_task_by_identifier(tasks, task_identifier)

        if candidates:
            return {
                "success": False,
                "error": "AMBIGUOUS",
                "data": {
                    "candidates": [{"id": t.id, "title": t.title} for t in candidates[:5]]
                },
                "message": f"Multiple tasks match '{task_identifier}'. Please be more specific."
            }

        if not task:
            return {
                "success": False,
                "error": "NOT_FOUND",
                "message": f"No task found matching '{task_identifier}'"
            }

        old_title = task.title

        # Build update data
        update_data = {}
        if new_title:
            update_data["title"] = new_title.strip()
        if new_description is not None:
            update_data["description"] = new_description
        if new_priority:
            try:
                update_data["priority"] = Priority(new_priority.lower())
            except ValueError:
                return {
                    "success": False,
                    "error": "VALIDATION_ERROR",
                    "message": f"Invalid priority '{new_priority}'. Use: none, low, medium, high, critical"
                }
        if new_due_date:
            if new_due_date.lower() == "clear":
                update_data["due_date"] = None
            else:
                try:
                    update_data["due_date"] = datetime.fromisoformat(new_due_date.replace("Z", "+00:00"))
                except (ValueError, TypeError):
                    return {
                        "success": False,
                        "error": "VALIDATION_ERROR",
                        "message": f"Invalid date format '{new_due_date}'. Use ISO 8601 format (e.g., 2025-12-31T23:59:00)"
                    }

        task_update = TaskUpdate(**update_data)
        updated_task = repo.update(task.id, user_id, task_update)

        logger.info(f"Updated task {task.id} for user {user_id}")

        result_data = {
            "task_id": updated_task.id,
            "old_title": old_title,
            "new_title": updated_task.title,
            "description": updated_task.description,
            "priority": updated_task.priority.value if hasattr(updated_task.priority, 'value') else str(updated_task.priority),
        }
        if updated_task.due_date:
            result_data["due_date"] = updated_task.due_date.isoformat()

        return {
            "success": True,
            "data": result_data,
            "message": "Task updated successfully"
        }
    except Exception as e:
        logger.error(f"Error updating task: {e}")
        return {
            "success": False,
            "error": "DATABASE_ERROR",
            "message": "Failed to update task due to a database error"
        }


def create_tool_executor(session: Session, user_id: str):
    """
    Create a tool executor function for the AI agent.

    Args:
        session: Database session
        user_id: The authenticated user's ID

    Returns:
        Function that executes tools with (tool_name, arguments) -> result
    """
    def executor(tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool by name with given arguments."""
        if tool_name == "add_task":
            return add_task(
                session,
                user_id,
                title=arguments.get("title", ""),
                description=arguments.get("description"),
                priority=arguments.get("priority"),
                due_date=arguments.get("due_date"),
            )
        elif tool_name == "list_tasks":
            return list_tasks(
                session,
                user_id,
                status=arguments.get("status", "all"),
            )
        elif tool_name == "complete_task":
            return complete_task(
                session,
                user_id,
                task_identifier=arguments.get("task_identifier", ""),
            )
        elif tool_name == "delete_task":
            return delete_task(
                session,
                user_id,
                task_identifier=arguments.get("task_identifier", ""),
            )
        elif tool_name == "update_task":
            return update_task(
                session,
                user_id,
                task_identifier=arguments.get("task_identifier", ""),
                new_title=arguments.get("new_title"),
                new_description=arguments.get("new_description"),
                new_priority=arguments.get("new_priority"),
                new_due_date=arguments.get("new_due_date"),
            )
        else:
            return {
                "success": False,
                "error": "UNKNOWN_TOOL",
                "message": f"Unknown tool: {tool_name}"
            }

    return executor
