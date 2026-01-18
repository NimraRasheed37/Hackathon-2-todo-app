from typing import List, Optional
from src.models.task import Task
import datetime

class TaskRepository:
    def __init__(self):
        self._tasks: dict[int, Task] = {}
        self._next_id = 1

    def get_all(self) -> List[Task]:
        return list(self._tasks.values())

    def get_by_id(self, task_id: int) -> Optional[Task]:
        return self._tasks.get(task_id)

    def add(self, task: Task) -> Task:
        if task.id is None:
            task.id = self._next_id
            self._next_id += 1
        self._tasks[task.id] = task
        return task

    def update(self, task: Task) -> Optional[Task]:
        if task.id in self._tasks:
            task.updated_at = datetime.datetime.now()
            self._tasks[task.id] = task
            return task
        return None

    def delete(self, task_id: int) -> bool:
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False
