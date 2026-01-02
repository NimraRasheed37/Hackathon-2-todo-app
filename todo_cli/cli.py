from todo_cli.models import Task
from todo_cli.storage import Storage
from todo_cli.utils import get_non_empty_input, get_optional_input, confirm_action
from typing import Optional


def add_task_cli(storage: Storage):
    """
    CLI function to add a new task.
    Prompts the user for a title and optional description, then adds the task to storage.
    """
    title = get_non_empty_input("Enter task title: ", "Task title cannot be empty.")
    if not title:
        return

    description = get_optional_input("Enter task description (optional): ")

    new_task = Task(title=title, description=description)
    storage.add_task(new_task)
    print(f"✅ Task '{new_task.title}' added successfully.")


def view_tasks_cli(storage: Storage):
    """
    CLI function to display all tasks in a formatted table.
    Tasks are sorted by creation date.
    """
    tasks = storage.get_all_tasks()
    if not tasks:
        print("📭 No tasks found. Your to-do list is empty.")
        return

    sorted_tasks = sorted(tasks, key=lambda t: t.created_date)

    print("\n┌───────┬──────────┬──────────────────────┬──────────────────────────────────────────┐")
    print("│ Status│    ID    │        Title         │               Description                │")
    print("├───────┼──────────┼──────────────────────┼──────────────────────────────────────────┤")

    for task in sorted_tasks:
        status = "✅" if task.completed else "❌"
        task_id = task.id[:8] + "..." if len(task.id) > 8 else task.id
        title = task.title[:20] + "..." if len(task.title) > 20 else task.title
        description = task.description or ""
        description = description[:40] + "..." if len(description) > 40 else description

        print(f"│ {status:^5} │ {task_id:<8} │ {title:<20} │ {description:<40} │")

    print("└───────┴──────────┴──────────────────────┴──────────────────────────────────────────┘")


def delete_task_cli(storage: Storage):
    """
    CLI function to delete a task by its ID.
    Prompts the user for a task ID and asks for confirmation before deletion.
    """
    task_id = get_non_empty_input("Enter the ID of the task to delete: ", "Task ID cannot be empty.")
    if not task_id:
        return

    tasks = storage.get_all_tasks()
    task_to_delete = next((t for t in tasks if t.id.startswith(task_id)), None)

    if not task_to_delete:
        print(f"❌ No task found with ID starting with '{task_id}'.")
        return

    if confirm_action(
        f"Are you sure you want to delete task '{task_to_delete.title}' "
        f"(ID: {task_to_delete.id[:8]}...)? (yes/no): "):
        storage.delete_task(task_to_delete.id)
        print(f"🗑️ Task '{task_to_delete.title}' deleted successfully.")
    else:
        print("👍 Task deletion cancelled.")


def update_task_cli(storage: Storage):
    """
    CLI function to update an existing task's title and/or description.
    Prompts the user for a task ID, then new title and description.
    """
    task_id = get_non_empty_input("Enter the ID of the task to update: ", "Task ID cannot be empty.")
    if not task_id:
        return

    tasks = storage.get_all_tasks()
    task_to_update = next((t for t in tasks if t.id.startswith(task_id)), None)

    if not task_to_update:
        print(f"❌ No task found with ID starting with '{task_id}'.")
        return

    print(f"Current Title: {task_to_update.title}")
    new_title = get_optional_input("Enter new title (leave blank to keep current): ")

    print(f"Current Description: {task_to_update.description or '[None]'}")
    new_description = get_optional_input("Enter new description (leave blank to keep current): ")

    if new_title is None and new_description is None:
        print("🤷 No changes provided. Task not updated.")
        return

    storage.update_task(task_to_update.id, new_title, new_description)

    updated_task = next((t for t in storage.get_all_tasks() if t.id == task_to_update.id), None)
    if updated_task:
        print(f"✏️ Task '{updated_task.title}' updated successfully.")
    else:
        print("⚠️ Task updated, but could not reload updated data.")


def mark_complete_task_cli(storage: Storage):
    """
    CLI function to toggle the completion status of a task.
    Prompts the user for a task ID and updates its status.
    """
    task_id = get_non_empty_input(
        "Enter the ID of the task to mark as complete/incomplete: ",
        "Task ID cannot be empty."
    )
    if not task_id:
        return

    tasks = storage.get_all_tasks()
    task_to_toggle = next((t for t in tasks if t.id.startswith(task_id)), None)

    if not task_to_toggle:
        print(f"❌ No task found with ID starting with '{task_id}'.")
        return

    storage.toggle_task_completion(task_to_toggle.id)

    updated_task = next((t for t in storage.get_all_tasks() if t.id == task_to_toggle.id), None)
    if updated_task:
        status = "completed" if updated_task.completed else "incomplete"
        print(f"✅ Task '{updated_task.title}' marked as {status}.")
    else:
        print("⚠️ Task status changed, but could not reload updated data.")


def run_cli():
    """Main CLI loop (optional implementation)."""
    pass