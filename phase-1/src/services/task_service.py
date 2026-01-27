from typing import List, Optional
from src.models.task import Task
from src.repository import TaskRepository
from datetime import datetime

class TaskService:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def add_task(self, title: str, description: Optional[str] = None) -> Task:
        task = Task(title=title, description=description)
        return self.repository.add(task)

    def get_all_tasks(self) -> List[Task]:
        return self.repository.get_all()

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        return self.repository.get_by_id(task_id)

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None, completed: Optional[bool] = None) -> Optional[Task]:
        task = self.repository.get_by_id(task_id)
        if task:
            if title is not None:
                task.title = title
            if description is not None:
                task.description = description
            if completed is not None:
                task.completed = completed
            task.updated_at = datetime.now()
            return self.repository.update(task)
        return None

    def delete_task(self, task_id: int) -> bool:
        return self.repository.delete(task_id)
    
    def mark_task_complete(self, task_id: int, completed: bool) -> Optional[Task]:
        task = self.repository.get_by_id(task_id)
        if task:
            task.completed = completed
            task.updated_at = datetime.now()
            return self.repository.update(task)
        return None
