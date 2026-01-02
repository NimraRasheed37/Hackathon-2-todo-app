import pytest
from datetime import datetime
import uuid
from todo_app.models import Task

def test_task_creation():
    title = "Test Task"
    task = Task(title=title)
    assert task.title == title
    assert isinstance(task.id, str)
    assert uuid.UUID(task.id, version=4)  # Check if it's a valid UUID
    assert isinstance(task.created_date, str)
    assert datetime.fromisoformat(task.created_date)  # Check if valid ISO format
    assert task.completed is False
    assert task.description is None

def test_task_creation_with_description():
    title = "Test Task with Desc"
    description = "This is a detailed description."
    task = Task(title=title, description=description)
    assert task.title == title
    assert task.description == description

def test_task_to_dict():
    title = "Dict Task"
    description = "Convert to dictionary."
    task = Task(title=title, description=description, completed=True)
    task_dict = task.to_dict()

    assert task_dict["id"] == task.id
    assert task_dict["title"] == title
    assert task_dict["description"] == description
    assert task_dict["created_date"] == task.created_date
    assert task_dict["completed"] is True

def test_task_from_dict():
    data = {
        "id": str(uuid.uuid4()),
        "title": "From Dict Task",
        "description": "Created from dictionary.",
        "created_date": datetime.now().isoformat(),
        "completed": False,
    }
    task = Task.from_dict(data)

    assert task.id == data["id"]
    assert task.title == data["title"]
    assert task.description == data["description"]
    assert task.created_date == data["created_date"]
    assert task.completed == data["completed"]

def test_task_from_dict_minimal():
    data = {
        "id": str(uuid.uuid4()),
        "title": "From Dict Minimal",
        "created_date": datetime.now().isoformat(),
    }
    task = Task.from_dict(data)

    assert task.id == data["id"]
    assert task.title == data["title"]
    assert task.description is None
    assert task.created_date == data["created_date"]
    assert task.completed is False

def test_task_sorting_by_created_date():
    # Create tasks with specific creation dates for predictable sorting
    # Use different dates to ensure order
    task1_data = {
        "id": str(uuid.uuid4()), "title": "Task A",
        "created_date": "2025-01-01T10:00:00.000000", "completed": False
    }
    task2_data = {
        "id": str(uuid.uuid4()), "title": "Task B",
        "created_date": "2025-01-01T11:00:00.000000", "completed": False
    }
    task3_data = {
        "id": str(uuid.uuid4()), "title": "Task C",
        "created_date": "2024-12-31T23:59:59.000000", "completed": False
    }

    task1 = Task.from_dict(task1_data)
    task2 = Task.from_dict(task2_data)
    task3 = Task.from_dict(task3_data)

    unsorted_tasks = [task1, task2, task3]

    # Sort the tasks based on created_date
    sorted_tasks = sorted(unsorted_tasks, key=lambda t: t.created_date)

    # Assert the correct order
    assert sorted_tasks[0].id == task3.id # Task C (earliest date)
    assert sorted_tasks[1].id == task1.id # Task A
    assert sorted_tasks[2].id == task2.id # Task B (latest date)

def test_task_toggle_completion():
    task = Task(title="Toggle Test")
    assert task.completed is False
    task.toggle_completion()
    assert task.completed is True
    task.toggle_completion()
    assert task.completed is False
