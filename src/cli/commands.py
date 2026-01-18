from src.services.task_service import TaskService
from src.repository import TaskRepository
from typing import Optional

def display_task(task):
    status = "✓" if task.completed else " "
    print(f"{task.id: <4} [{status}] {task.title: <30} {task.updated_at.strftime('%Y-%m-%d %H:%M')}")

def add_task_command(task_service: TaskService):
    title = input("Enter task title: ")
    if not title:
        print("Task title cannot be empty.")
        return

    description = input("Enter task description (optional): ")
    task = task_service.add_task(title=title, description=description if description else None)
    print(f"Task '{task.title}' added with ID: {task.id}")

def view_tasks_command(task_service: TaskService):
    tasks = task_service.get_all_tasks()
    if not tasks:
        print("No tasks found.")
        return

    print("\nID   Status Title                         Last Updated")
    print("---- ------ ------------------------------ -------------------")
    for task in tasks:
        display_task(task)
    print("---------------------------------------------------------------")

def update_task_command(task_service: TaskService):
    task_id_str = input("Enter the ID of the task to update: ")
    try:
        task_id = int(task_id_str)
    except ValueError:
        print("Invalid task ID. Please enter a number.")
        return

    task = task_service.get_task_by_id(task_id)
    if not task:
        print(f"Task with ID {task_id} not found.")
        return

    print(f"Current Title: {task.title}")
    new_title = input(f"Enter new title (leave blank to keep current: '{task.title}'): ")
    print(f"Current Description: {task.description if task.description else 'N/A'}")
    new_description = input(f"Enter new description (leave blank to keep current): ")
    
    updated_task = task_service.update_task(
        task_id=task_id,
        title=new_title if new_title else None,
        description=new_description if new_description else task.description
    )

    if updated_task:
        print(f"Task {updated_task.id} updated successfully.")
    else:
        print(f"Failed to update task {task_id}.")


def delete_task_command(task_service: TaskService):
    task_id_str = input("Enter the ID of the task to delete: ")
    try:
        task_id = int(task_id_str)
    except ValueError:
        print("Invalid task ID. Please enter a number.")
        return

    if task_service.delete_task(task_id):
        print(f"Task {task_id} deleted successfully.")
    else:
        print(f"Task with ID {task_id} not found.")

def mark_task_complete_command(task_service: TaskService):
    task_id_str = input("Enter the ID of the task to mark complete/incomplete: ")
    try:
        task_id = int(task_id_str)
    except ValueError:
        print("Invalid task ID. Please enter a number.")
        return

    task = task_service.get_task_by_id(task_id)
    if not task:
        print(f"Task with ID {task_id} not found.")
        return
    
    new_status = "incomplete" if task.completed else "complete"
    confirm = input(f"Mark task '{task.title}' as {new_status}? (y/n): ").lower()
    if confirm == 'y':
        updated_task = task_service.mark_task_complete(task_id, not task.completed)
        if updated_task:
            print(f"Task {updated_task.id} marked as {new_status}.")
        else:
            print(f"Failed to update task {task_id}.")
    else:
        print("Operation cancelled.")
