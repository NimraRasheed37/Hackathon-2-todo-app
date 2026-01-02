from dataclasses import dataclass, field
from datetime import datetime
import uuid
from typing import Optional, Dict, Any

@dataclass
class Task:
    id: str = field(init=False)
    title: str
    description: Optional[str] = None
    created_date: str = field(init=False)
    completed: bool = False

    def __post_init__(self):
        self.id = str(uuid.uuid4())
        self.created_date = datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "created_date": self.created_date,
            "completed": self.completed,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Task":
        task = cls(title=data["title"], description=data.get("description"), completed=data.get("completed", False))
        task.id = data["id"]
        task.created_date = data["created_date"]
        return task

    def toggle_completion(self):
        self.completed = not self.completed
