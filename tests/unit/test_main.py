import pytest
from unittest.mock import patch
from io import StringIO
from todo_cli.main import main
from todo_cli.storage import Storage
from todo_cli.models import Task
from pathlib import Path

@pytest.fixture
def main_app_storage(tmp_path):
    """Fixture to provide a Storage instance for main app tests."""
    file = tmp_path / "todos.json"
    return Storage(filename=str(file))

def test_main_menu_exit(main_app_storage, monkeypatch, capsys):
    """
    Test that selecting '0' exits the main application loop gracefully.
    """
    inputs = iter(["0"]) # Choose Exit
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    # Mock the Storage.__init__ so that main uses our fixture's storage
    with patch('todo_cli.main.Storage', return_value=main_app_storage):
        main()

    captured = capsys.readouterr()
    assert "Todo List Manager started." in captured.out
    assert "┌──────────────────────────────────────────┐" in captured.out
    assert "│ 📝 Todo List Manager                     │" in captured.out
    assert "└──────────────────────────────────────────┘" in captured.out
    assert "Exiting Todo List Manager." in captured.out
    
def test_main_menu_invalid_choice(main_app_storage, monkeypatch, capsys):
    """
    Test that an invalid menu choice is handled and the menu is reprinted.
    """
    inputs = iter(["99", "0"]) # Invalid choice, then Exit
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    with patch('todo_cli.main.Storage', return_value=main_app_storage):
        main()

    captured = capsys.readouterr()
    assert "Invalid choice. Please try again." in captured.out
    assert captured.out.count("┌──────────────────────────────────────────┐") == 2
    assert captured.out.count("│ 📝 Todo List Manager                     │") == 2
    assert captured.out.count("└──────────────────────────────────────────┘") == 2
    assert "Exiting Todo List Manager." in captured.out

def test_main_menu_add_task_then_exit(main_app_storage, monkeypatch, capsys):
    """
    Test adding a task via the main menu and then exiting.
    """
    inputs = iter([
        "1", # Choose Add Task
        "New Main Task", # Title
        "Description for main task", # Description
        "0" # Choose Exit
    ])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    with patch('todo_cli.main.Storage', return_value=main_app_storage):
        main()

    captured = capsys.readouterr()
    assert "Task 'New Main Task' added." in captured.out
    assert "Exiting Todo List Manager." in captured.out
    
    tasks_in_storage = main_app_storage.load_tasks()
    assert len(tasks_in_storage) == 1
    assert tasks_in_storage[0].title == "New Main Task"

def test_main_menu_view_tasks_then_exit(main_app_storage, monkeypatch, capsys):
    """
    Test viewing tasks via the main menu and then exiting.
    """
    task = Task(title="View From Main")
    main_app_storage.add_task(task)

    inputs = iter([
        "2", # Choose View Tasks
        "0" # Choose Exit
    ])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    with patch('todo_cli.main.Storage', return_value=main_app_storage):
        main()

    captured = capsys.readouterr()

    task_id = task.id[:8] + "..."
    status = "❌"
    title = "View From Main"
    description = ""

    expected_row = f"│ {status:^5} │ {task_id:<8} │ {title:<20} │ {description:<40} │"

    assert "┌───────┬──────────┬──────────────────────┬──────────────────────────────────────────┐" in captured.out
    assert "│ Status│    ID    │        Title         │               Description                │" in captured.out
    assert "├───────┼──────────┼──────────────────────┼──────────────────────────────────────────┤" in captured.out
    assert expected_row in captured.out
    assert "└───────┴──────────┴──────────────────────┴──────────────────────────────────────────┘" in captured.out
    assert "Exiting Todo List Manager." in captured.out

def test_main_menu_delete_task_then_exit(main_app_storage, monkeypatch, capsys):
    """
    Test deleting a task via the main menu and then exiting.
    """
    task = Task(title="Delete From Main")
    main_app_storage.add_task(task)

    inputs = iter([
        "3", # Choose Delete Task
        task.id[:8], # Task ID
        "yes", # Confirmation
        "0" # Choose Exit
    ])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    with patch('todo_cli.main.Storage', return_value=main_app_storage):
        main()

    captured = capsys.readouterr()
    assert f"Task '{task.title}' deleted." in captured.out
    assert "Exiting Todo List Manager." in captured.out
    assert len(main_app_storage.load_tasks()) == 0

def test_main_menu_update_task_then_exit(main_app_storage, monkeypatch, capsys):
    """
    Test updating a task via the main menu and then exiting.
    """
    task = Task(title="Update From Main")
    main_app_storage.add_task(task)

    inputs = iter([
        "4", # Choose Update Task
        task.id[:8], # Task ID
        "Updated Title", # New title
        "", # No new description
        "0" # Choose Exit
    ])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    with patch('todo_cli.main.Storage', return_value=main_app_storage):
        main()

    captured = capsys.readouterr()
    assert f"Task 'Updated Title' updated." in captured.out
    assert "Exiting Todo List Manager." in captured.out
    updated_task = main_app_storage.load_tasks()[0]
    assert updated_task.title == "Updated Title"

def test_main_menu_mark_complete_task_then_exit(main_app_storage, monkeypatch, capsys):
    """
    Test marking a task complete via the main menu and then exiting.
    """
    task = Task(title="Mark Complete From Main", completed=False)
    main_app_storage.add_task(task)

    inputs = iter([
        "5", # Choose Mark Complete
        task.id[:8], # Task ID
        "0" # Choose Exit
    ])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    with patch('todo_cli.main.Storage', return_value=main_app_storage):
        main()

    captured = capsys.readouterr()
    assert f"Task '{task.title}' marked as completed." in captured.out
    assert "Exiting Todo List Manager." in captured.out
    updated_task = main_app_storage.load_tasks()[0]
    assert updated_task.completed is True
