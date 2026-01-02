import pytest
import json
from pathlib import Path
from typing import Optional
from todo_cli.storage import Storage
from todo_cli.models import Task

@pytest.fixture
def temp_todos_file(tmp_path):
    """Fixture to create a temporary todos.json file for testing."""
    file = tmp_path / "todos.json"
    return file

@pytest.fixture
def storage(temp_todos_file):
    """Fixture to provide a Storage instance with a temporary file."""
    return Storage(filename=str(temp_todos_file))

def test_storage_initializes_empty_file(temp_todos_file):
    """Test that Storage creates an empty JSON file if it doesn't exist."""
    assert not temp_todos_file.exists()
    Storage(filename=str(temp_todos_file))
    assert temp_todos_file.exists()
    assert temp_todos_file.read_text() == "[]"

def test_storage_load_empty_file(storage):
    """Test loading tasks from an empty '[]' JSON file."""
    tasks = storage.load_tasks()
    assert tasks == []

def test_storage_load_missing_file(storage, temp_todos_file):
    """Test loading tasks when the file is missing."""
    temp_todos_file.unlink()  # Ensure file is missing
    tasks = storage.load_tasks()
    assert tasks == []
    assert temp_todos_file.exists() # Should recreate it as empty

def test_storage_load_corrupted_file(storage, temp_todos_file):
    """Test loading tasks from a corrupted JSON file."""
    temp_todos_file.write_text("this is not json")
    tasks = storage.load_tasks()
    assert tasks == []

def test_storage_save_and_load_single_task(storage):
    """Test saving and loading a single task."""
    task = Task(title="Buy milk")
    storage.add_task(task) # Use add_task for consistency

    loaded_tasks = storage.load_tasks()
    assert len(loaded_tasks) == 1
    assert loaded_tasks[0].id == task.id
    assert loaded_tasks[0].title == task.title
    assert loaded_tasks[0].description == task.description
    assert loaded_tasks[0].created_date == task.created_date
    assert loaded_tasks[0].completed == task.completed

def test_storage_save_and_load_multiple_tasks(storage):
    """Test saving and loading multiple tasks."""
    task1 = Task(title="Task One")
    task2 = Task(title="Task Two", description="Description for task two")
    storage.add_task(task1)
    storage.add_task(task2)

    loaded_tasks = storage.load_tasks()
    assert len(loaded_tasks) == 2
    assert loaded_tasks[0].id == task1.id
    assert loaded_tasks[1].id == task2.id
    assert loaded_tasks[1].description == task2.description

def test_storage_task_data_integrity(storage):
    """Test that all task attributes are correctly saved and loaded."""
    original_task = Task(title="Integrity Check", description="Details", completed=True)
    storage.add_task(original_task)
    loaded_task = storage.load_tasks()[0]

    assert loaded_task.id == original_task.id
    assert loaded_task.title == original_task.title
    assert loaded_task.description == original_task.description
    assert loaded_task.created_date == original_task.created_date
    assert loaded_task.completed == original_task.completed

def test_storage_delete_existing_task(storage):
    """Test deleting an existing task."""
    task1 = Task(title="Task to delete")
    task2 = Task(title="Task to keep")
    storage.add_task(task1)
    storage.add_task(task2)
    
    initial_tasks = storage.load_tasks()
    assert len(initial_tasks) == 2

    storage.delete_task(task1.id)
    
    remaining_tasks = storage.load_tasks()
    assert len(remaining_tasks) == 1
    assert remaining_tasks[0].id == task2.id

def test_storage_delete_non_existent_task(storage):
    """Test deleting a non-existent task does not change anything."""
    task = Task(title="Existing Task")
    storage.add_task(task)
    
    initial_tasks = storage.load_tasks()
    assert len(initial_tasks) == 1

    storage.delete_task("non-existent-id")
    
    remaining_tasks = storage.load_tasks()
    assert len(remaining_tasks) == 1
    assert remaining_tasks[0].id == task.id

def test_storage_update_existing_task(storage):
    """Test updating an existing task's title and description."""
    task = Task(title="Original Title", description="Original Desc")
    storage.add_task(task)

    updated_title = "New Title"
    updated_description = "New Description"
    storage.update_task(task.id, updated_title, updated_description)

    loaded_tasks = storage.load_tasks()
    assert len(loaded_tasks) == 1
    updated_task = loaded_tasks[0]

    assert updated_task.id == task.id
    assert updated_task.title == updated_title
    assert updated_task.description == updated_description
    assert updated_task.completed == task.completed # Should not change completion status

def test_storage_update_task_partial_title(storage):
    """Test updating only the title of an existing task."""
    task = Task(title="Original Title", description="Original Desc")
    storage.add_task(task)

    updated_title = "New Title Only"
    storage.update_task(task.id, updated_title, None) # Pass None for description

    loaded_tasks = storage.load_tasks()
    updated_task = loaded_tasks[0]

    assert updated_task.title == updated_title
    assert updated_task.description == task.description # Description should remain unchanged

def test_storage_update_task_partial_description(storage):
    """Test updating only the description of an existing task."""
    task = Task(title="Original Title", description="Original Desc")
    storage.add_task(task)

    updated_description = "New Description Only"
    storage.update_task(task.id, None, updated_description) # Pass None for title

    loaded_tasks = storage.load_tasks()
    updated_task = loaded_tasks[0]

    assert updated_task.title == task.title # Title should remain unchanged
    assert updated_task.description == updated_description

def test_storage_update_non_existent_task(storage):
    """Test updating a non-existent task does not change anything."""
    task = Task(title="Existing Task")
    storage.add_task(task)
    
    initial_tasks = storage.load_tasks()
    assert len(initial_tasks) == 1

    storage.update_task("non-existent-id", "Fake Title", "Fake Desc")
    
    remaining_tasks = storage.load_tasks()
    assert len(remaining_tasks) == 1
    assert remaining_tasks[0].id == task.id
    assert remaining_tasks[0].title == task.title
    assert remaining_tasks[0].description == task.description

def test_storage_toggle_existing_task_completion(storage):
    """Test toggling completion status of an existing task."""
    task = Task(title="Toggle Me", completed=False)
    storage.add_task(task)

    # Toggle to True
    storage.toggle_task_completion(task.id)
    loaded_task = storage.load_tasks()[0]
    assert loaded_task.completed is True

    # Toggle back to False
    storage.toggle_task_completion(task.id)
    loaded_task = storage.load_tasks()[0]
    assert loaded_task.completed is False

def test_storage_toggle_non_existent_task_completion(storage):
    """Test toggling completion of a non-existent task does not change anything."""
    task = Task(title="Existing Task")
    storage.add_task(task)
    
    initial_tasks = storage.load_tasks()
    assert len(initial_tasks) == 1
    assert initial_tasks[0].completed is False

    storage.toggle_task_completion("non-existent-id")
    
    remaining_tasks = storage.load_tasks()
    assert len(remaining_tasks) == 1
    assert remaining_tasks[0].id == task.id
    assert remaining_tasks[0].completed is False # Status should remain unchanged