import pytest
from unittest.mock import patch
from io import StringIO # Still useful for some custom mocking if needed, but not for direct stdout capture now
from todo_app.cli import add_task_cli, view_tasks_cli, delete_task_cli, update_task_cli, mark_complete_task_cli
from todo_app.storage import Storage
from todo_app.models import Task
from pathlib import Path
from todo_app import utils # Import utils to patch its functions, if needed for other tests

# Fixture for a temporary storage file to isolate tests
@pytest.fixture
def cli_storage(tmp_path):
    """Fixture to create a temporary todos.json file for testing."""
    file = tmp_path / "todos.json"
    return Storage(filename=str(file))

# Helper to run CLI functions with mocked input and captured output
# This helper now explicitly mocks builtins.input for each scenario
def run_cli_function_with_mocked_input(cli_function, mock_input_values, storage_instance):
    with patch('builtins.input', side_effect=mock_input_values), \
         patch('sys.stdout', new_callable=StringIO) as mock_stdout:
        
        cli_function(storage_instance)

    return mock_stdout.getvalue()


# --- Tests for add_task_cli (from T011) --- 
def test_add_task_cli_adds_and_persists_task(cli_storage, capsys):
    """
    Integration test: Verify that the add_task_cli function correctly
    prompts for input, creates a task, and saves it via storage.
    """
    mock_input_values = ["New Task Title", "Optional description for new task"]
    
    with patch('builtins.input', side_effect=mock_input_values):
        add_task_cli(cli_storage)
    
    captured = capsys.readouterr()
    assert "Task 'New Task Title' added." in captured.out
    
    tasks_in_storage = cli_storage.load_tasks()
    assert len(tasks_in_storage) == 1
    assert tasks_in_storage[0].title == "New Task Title"
    assert tasks_in_storage[0].description == "Optional description for new task"
    assert not tasks_in_storage[0].completed

def test_add_task_cli_adds_task_without_description(cli_storage, capsys):
    """
    Integration test: Verify adding a task without a description.
    """
    mock_input_values = ["Task without Desc", ""] # Empty string for description
    
    with patch('builtins.input', side_effect=mock_input_values):
        add_task_cli(cli_storage)
    
    captured = capsys.readouterr()
    assert "Task 'Task without Desc' added." in captured.out
    
    tasks_in_storage = cli_storage.load_tasks()
    assert len(tasks_in_storage) == 1
    assert tasks_in_storage[0].title == "Task without Desc"
    assert tasks_in_storage[0].description is None

def test_add_task_cli_empty_title(cli_storage, capsys):
    """
    Test that add_task_cli handles an empty title input.
    """
    mock_input_values = ["", "Valid Title", "Description"] # Empty title, then valid title and description
    with patch('builtins.input', side_effect=mock_input_values):
        add_task_cli(cli_storage) # Should try twice due to loop in get_non_empty_input

    captured = capsys.readouterr()
    assert "Task title cannot be empty." in captured.out
    assert "Task 'Valid Title' added." in captured.out # Should eventually add with valid title
    assert len(cli_storage.load_tasks()) == 1


# --- Tests for view_tasks_cli (from T017) --- 
def run_view_tasks_cli_with_captured_output(storage_instance):
    with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
        view_tasks_cli(storage_instance)
    return mock_stdout.getvalue()

def test_view_tasks_cli_empty_list(cli_storage, capsys):
    """
    Test that view_tasks_cli correctly handles an empty task list.
    """
    view_tasks_cli(cli_storage)
    captured = capsys.readouterr()
    assert "No tasks found." in captured.out

def test_view_tasks_cli_single_task(cli_storage, capsys):
    """
    Test that view_tasks_cli correctly displays a single task.
    """
    task = Task(title="Single Task View")
    cli_storage.add_task(task)
    
    view_tasks_cli(cli_storage)
    captured = capsys.readouterr()
    assert "--- Your Tasks ---" in captured.out
    assert f"[ ] {task.id[:8]}... | Single Task View" in captured.out
    assert "------------------" in captured.out

def test_view_tasks_cli_multiple_tasks_sorted(cli_storage, capsys):
    """
    Test that view_tasks_cli correctly displays multiple tasks sorted by created_date.
    """
    task1 = Task(title="Task Z", description="Desc Z")
    task1.created_date = "2025-01-01T12:00:00.000000" # Use specific date for sorting
    
    task2 = Task(title="Task A", completed=True)
    task2.created_date = "2025-01-01T10:00:00.000000" # Use specific date for sorting
    
    task3 = Task(title="Task M", description="Desc M")
    task3.created_date = "2024-12-31T23:59:59.000000" # Use specific date for sorting

    # Add tasks in non-sorted order to ensure sorting logic in cli is tested
    cli_storage.add_task(task1)
    cli_storage.add_task(task2)
    cli_storage.add_task(task3)

    view_tasks_cli(cli_storage)
    captured = capsys.readouterr()
    
    output_lines = [line.strip() for line in captured.out.split('\n') if line.strip()]

    # Expected order based on created_date (task3, task2, task1)
    # Task M (earliest), Task A, Task Z (latest)
    assert f"[ ] {task3.id[:8]}... | {task3.title}" in output_lines
    assert f"[X] {task2.id[:8]}... | {task2.title}" in output_lines
    assert f"[ ] {task1.id[:8]}... | {task1.title}" in output_lines

    # Check descriptions
    assert f"Description: {task3.description}" in output_lines
    assert f"Description: {task1.description}" in output_lines


def test_view_tasks_cli_with_completed_task(cli_storage, capsys):
    task = Task(title="Completed Task")
    task.completed = True
    cli_storage.add_task(task)

    view_tasks_cli(cli_storage)
    captured = capsys.readouterr()
    assert f"[X] {task.id[:8]}... | Completed Task" in captured.out

# --- Tests for delete_task_cli (from T022) --- 
def test_delete_task_cli_deletes_existing_task(cli_storage, capsys):
    """
    Test that delete_task_cli successfully deletes an existing task with confirmation.
    """
    task_to_delete = Task(title="Task to Delete")
    task_to_keep = Task(title="Task to Keep")
    cli_storage.add_task(task_to_delete)
    cli_storage.add_task(task_to_keep)

    mock_input_values = [task_to_delete.id[:8], "yes"] # Provide partial ID and confirmation
    with patch('builtins.input', side_effect=mock_input_values):
        delete_task_cli(cli_storage)

    captured = capsys.readouterr()
    assert f"Task '{task_to_delete.title}' deleted." in captured.out
    
    remaining_tasks = cli_storage.load_tasks()
    assert len(remaining_tasks) == 1
    assert remaining_tasks[0].id == task_to_keep.id

def test_delete_task_cli_cancels_deletion(cli_storage, capsys):
    """
    Test that delete_task_cli cancels deletion if user does not confirm.
    """
    task = Task(title="Task to Cancel Delete")
    cli_storage.add_task(task)

    mock_input_values = [task.id[:8], "no"] # Provide partial ID and no confirmation
    with patch('builtins.input', side_effect=mock_input_values):
        delete_task_cli(cli_storage)

    captured = capsys.readouterr()
    assert "Task deletion cancelled." in captured.out
    assert len(cli_storage.load_tasks()) == 1 # Task should still be there

def test_delete_task_cli_non_existent_id(cli_storage, capsys):
    """
    Test that delete_task_cli handles a non-existent task ID.
    """
    task = Task(title="Existing Task")
    cli_storage.add_task(task)

    mock_input_values = ["non-existent-id", "yes"] # Non-existent ID
    with patch('builtins.input', side_effect=mock_input_values):
        delete_task_cli(cli_storage)

    captured = capsys.readouterr()
    assert "No task found with ID starting with 'non-existent-id'." in captured.out
    assert len(cli_storage.load_tasks()) == 1 # Task should still be there

def test_delete_task_cli_empty_id(cli_storage, capsys):
    """
    Test that delete_task_cli handles an empty task ID input.
    """
    task = Task(title="Existing Task")
    cli_storage.add_task(task)

    mock_input_values = ["", "Valid ID", "yes"] # Empty ID, then valid ID for retry, then confirmation
    with patch('builtins.input', side_effect=mock_input_values):
        delete_task_cli(cli_storage)

    captured = capsys.readouterr()
    assert "Task ID cannot be empty." in captured.out
    assert len(cli_storage.load_tasks()) == 1 # Task should still be there

# --- Tests for update_task_cli (from T027) --- 
def test_update_task_cli_updates_title_and_description(cli_storage, capsys):
    """
    Test that update_task_cli correctly updates an existing task's title and description.
    """
    task = Task(title="Old Title", description="Old Desc")
    cli_storage.add_task(task)

    # Mock inputs: task_id, new_title, new_description
    mock_input_values = [task.id[:8], "New Title", "New Desc"] 
    with patch('builtins.input', side_effect=mock_input_values):
        update_task_cli(cli_storage)

    captured = capsys.readouterr()
    assert "Current Title: Old Title" in captured.out
    assert "Current Description: Old Desc" in captured.out
    assert f"Task 'New Title' updated." in captured.out

    updated_task = cli_storage.load_tasks()[0]
    assert updated_task.title == "New Title"
    assert updated_task.description == "New Desc"

def test_update_task_cli_updates_only_title(cli_storage, capsys):
    """
    Test that update_task_cli updates only the title if description is left blank.
    """
    task = Task(title="Old Title", description="Old Desc")
    cli_storage.add_task(task)

    mock_input_values = [task.id[:8], "New Title Only", ""] # Task ID, new title, blank desc
    with patch('builtins.input', side_effect=mock_input_values):
        update_task_cli(cli_storage)

    captured = capsys.readouterr()
    assert "Current Title: Old Title" in captured.out # These prompts are now explicitly printed
    assert "Current Description: Old Desc" in captured.out # These prompts are now explicitly printed
    assert f"Task 'New Title Only' updated." in captured.out

    updated_task = cli_storage.load_tasks()[0]
    assert updated_task.title == "New Title Only"
    assert updated_task.description == "Old Desc" # Description should be unchanged

def test_update_task_cli_updates_only_description(cli_storage, capsys):
    """
    Test that update_task_cli updates only the description if title is left blank.
    """
    task = Task(title="Old Title", description="Old Desc")
    cli_storage.add_task(task)

    mock_input_values = [task.id[:8], "", "New Desc Only"] # Task ID, blank title, new desc
    with patch('builtins.input', side_effect=mock_input_values):
        update_task_cli(cli_storage)

    captured = capsys.readouterr()
    assert "Current Title: Old Title" in captured.out # These prompts are now explicitly printed
    assert "Current Description: Old Desc" in captured.out # These prompts are now explicitly printed
    assert f"Task 'Old Title' updated." in captured.out

    updated_task = cli_storage.load_tasks()[0]
    assert updated_task.title == "Old Title" # Title should be unchanged
    assert updated_task.description == "New Desc Only"

def test_update_task_cli_no_changes_provided(cli_storage, capsys):
    """
    Test that update_task_cli does nothing if both title and description are left blank.
    """
    task = Task(title="Original", description="Original")
    cli_storage.add_task(task)

    mock_input_values = [task.id[:8], "", ""] # Task ID, blank title, blank desc
    with patch('builtins.input', side_effect=mock_input_values):
        update_task_cli(cli_storage)

    captured = capsys.readouterr()
    assert "Current Title: Original" in captured.out
    assert "Current Description: Original" in captured.out
    assert "No changes provided. Task not updated." in captured.out
    updated_task = cli_storage.load_tasks()[0]
    assert updated_task.title == "Original"
    assert updated_task.description == "Original"

def test_update_task_cli_non_existent_id(cli_storage, capsys):
    """
    Test that update_task_cli handles a non-existent task ID.
    """
    task = Task(title="Existing Task")
    cli_storage.add_task(task)

    mock_input_values = ["non-existent-id", "New Title", "New Desc"]
    with patch('builtins.input', side_effect=mock_input_values):
        update_task_cli(cli_storage)

    captured = capsys.readouterr()
    assert "No task found with ID starting with 'non-existent-id'." in captured.out
    assert len(cli_storage.load_tasks()) == 1 # Task should still be there and unchanged

def test_update_task_cli_empty_id(cli_storage, capsys):
    """
    Test that update_task_cli handles an empty task ID input.
    """
    task = Task(title="Existing Task")
    cli_storage.add_task(task)

    mock_input_values = ["", "Valid ID", "New Title", "New Desc"] # Empty ID, then valid ID for retry
    with patch('builtins.input', side_effect=mock_input_values):
        update_task_cli(cli_storage)

    captured = capsys.readouterr()
    assert "Task ID cannot be empty." in captured.out
    assert len(cli_storage.load_tasks()) == 1 # Task should still be there and unchanged

# --- Tests for mark_complete_task_cli (from T033) --- 
def test_mark_complete_task_cli_marks_incomplete_task_complete(cli_storage, capsys):
    """
    Test that mark_complete_task_cli correctly marks an incomplete task as complete.
    """
    task = Task(title="Incomplete Task", completed=False)
    cli_storage.add_task(task)

    mock_input_values = [task.id[:8]] # Provide partial ID
    with patch('builtins.input', side_effect=mock_input_values):
        mark_complete_task_cli(cli_storage)

    captured = capsys.readouterr()
    assert f"Task '{task.title}' marked as completed." in captured.out

    updated_task = cli_storage.load_tasks()[0]
    assert updated_task.completed is True

def test_mark_complete_task_cli_marks_complete_task_incomplete(cli_storage, capsys):
    """
    Test that mark_complete_task_cli correctly marks a complete task as incomplete.
    """
    task = Task(title="Complete Task", completed=True)
    cli_storage.add_task(task)

    mock_input_values = [task.id[:8]] # Provide partial ID
    with patch('builtins.input', side_effect=mock_input_values):
        mark_complete_task_cli(cli_storage)

    captured = capsys.readouterr()
    assert f"Task '{task.title}' marked as incomplete." in captured.out

    updated_task = cli_storage.load_tasks()[0]
    assert updated_task.completed is False

def test_mark_complete_task_cli_non_existent_id(cli_storage, capsys):
    """
    Test that mark_complete_task_cli handles a non-existent task ID.
    """
    task = Task(title="Existing Task")
    cli_storage.add_task(task)

    mock_input_values = ["non-existent-id"]
    with patch('builtins.input', side_effect=mock_input_values):
        mark_complete_task_cli(cli_storage)

    captured = capsys.readouterr()
    assert "No task found with ID starting with 'non-existent-id'." in captured.out
    assert len(cli_storage.load_tasks()) == 1 # Task should still be there and unchanged

def test_mark_complete_task_cli_empty_id(cli_storage, capsys):
    """
    Test that mark_complete_task_cli handles an empty task ID input.
    """
    task = Task(title="Existing Task")
    cli_storage.add_task(task)

    mock_input_values = ["", "Valid ID"] # Empty ID, then valid ID for retry
    with patch('builtins.input', side_effect=mock_input_values):
        mark_complete_task_cli(cli_storage)

    captured = capsys.readouterr()
    assert "Task ID cannot be empty." in captured.out
    assert len(cli_storage.load_tasks()) == 1 # Task should still be there and unchanged
