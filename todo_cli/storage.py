import json
from pathlib import Path
from typing import List, Dict, Any, Optional

from todo_cli.models import Task

class Storage:
    """Handles reading from and writing to the todos.json file."""

    def __init__(self, filename: str = "todos.json"):
        """
        Initializes the Storage with a given filename.
        Ensures the JSON file exists, creating it if necessary.
        """
        self.filepath = Path(filename)
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """Ensures the todos.json file exists and is a valid empty JSON array."""
        if not self.filepath.exists():
            self.filepath.write_text("[]")

    def load_tasks(self) -> List[Task]:
        """
        Loads all tasks from the JSON file.
        Handles cases where the file is empty or corrupted.
        """
        self._ensure_file_exists()
        with open(self.filepath, "r") as f:
            try:
                data = json.load(f)
                return [Task.from_dict(item) for item in data]
            except json.JSONDecodeError:
                # Handle corrupted JSON or empty file that's not '[]'
                return []

    def save_tasks(self, tasks: List[Task]):
        """
        Saves a list of Task objects to the JSON file.
        """
        with open(self.filepath, "w") as f:
            json.dump([task.to_dict() for task in tasks], f, indent=4)

    def add_task(self, task: Task):
        """
        Adds a new task to the list and saves the updated list to the JSON file.
        """
        tasks = self.load_tasks()
        tasks.append(task)
        self.save_tasks(tasks)

    def get_all_tasks(self) -> List[Task]:
        """
        Retrieves all tasks from storage.
        """
        return self.load_tasks()

    def delete_task(self, task_id: str):
        """
        Deletes a task by its ID and saves the updated list.
        If the task is not found, no action is taken.
        """
        tasks = self.load_tasks()
        initial_len = len(tasks)
        tasks = [task for task in tasks if task.id != task_id]
        if len(tasks) < initial_len: # Only save if a task was actually removed
            self.save_tasks(tasks)

    def update_task(self, task_id: str, new_title: Optional[str] = None, new_description: Optional[str] = None):
        """
        Updates an existing task's title and/or description by its ID.
        If the task is not found, no action is taken.
        """
        tasks = self.load_tasks()
        updated = False
        for task in tasks:
            if task.id == task_id:
                if new_title is not None:
                    task.title = new_title
                if new_description is not None:
                    task.description = new_description
                updated = True
                break
        if updated:
            self.save_tasks(tasks)

    def toggle_task_completion(self, task_id: str):
        """
        Toggles the completion status of a task by its ID and saves the updated list.
        If the task is not found, no action is taken.
        """
        tasks = self.load_tasks()
        toggled = False
        for task in tasks:
            if task.id == task_id:
                task.toggle_completion()
                toggled = True
                break
        if toggled:
            self.save_tasks(tasks)