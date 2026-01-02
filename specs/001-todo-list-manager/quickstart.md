# Quickstart Guide: Todo List Manager

**Feature Branch**: `001-todo-list-manager`  
**Created**: 2025-12-05
**Input**: Implementation Plan (`specs/001-todo-list-manager/plan.md`)

This guide provides basic instructions to get the Todo List Manager running and perform initial operations.

## Prerequisites

-   Python 3.11+ installed on your system.
-   Access to a command-line terminal (e.g., PowerShell, Bash, CMD).

## Setup

1.  **Clone the Repository**:
    If you haven't already, clone the project repository:
    ```bash
    git clone [REPOSITORY_URL]
    cd [PROJECT_DIRECTORY]
    ```

2.  **Navigate to the Application Directory**:
    The main application logic resides in the `todo_cli/` directory.
    ```bash
    cd todo_cli/
    ```

## Running the Application

To start the Todo List Manager, execute the `main.py` script:

```bash
python main.py
```

This will launch the interactive command-line interface.

## Basic Usage

Once the application is running, you will be presented with a main menu. Follow the numbered prompts to perform actions:

```
Todo List Manager started.

--- Main Menu ---
1. Add Task
2. View All Tasks
3. Delete Task
4. Update Task
5. Mark as Complete/Incomplete
0. Exit
Enter your choice:
```

1.  **Add Task**: Choose option `1`.
    ```
    Enter your choice: 1
    Enter task title: Buy Groceries
    Enter task description (optional): Milk, eggs, bread
    Task 'Buy Groceries' added.
    ```
2.  **View All Tasks**: Choose option `2`.
    ```
    Enter your choice: 2

    --- Your Tasks ---
    [ ] a1b2c3d4... | Buy Groceries
        Description: Milk, eggs, bread
    ------------------
    ```
3.  **Delete Task**: Choose option `3`, then enter the ID of the task you wish to remove. Confirm your choice when prompted.
4.  **Update Task**: Choose option `4`, then enter the ID of the task to modify, followed by the new title and/or description.
5.  **Mark as Complete**: Choose option `5`, then enter the ID of the task whose status you wish to toggle.

The application will automatically save your tasks to `todos.json` in the application's root directory.

## Running Tests

To run the unit tests for the application:

1.  Ensure you have `pytest` installed:
    ```bash
    pip install pytest
    ```
2.  From the project root directory, run `pytest`:
    ```bash
    pytest
    ```