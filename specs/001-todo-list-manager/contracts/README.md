# Contracts: Todo List Manager

**Feature Branch**: `001-todo-list-manager`  
**Created**: 2025-12-05
**Input**: Feature specification (`specs/001-todo-list-manager/spec.md`)

## API Contracts

Given that the "Todo List Manager" is a console-based application that persists data to a local JSON file (`todos.json`), there are no external APIs or traditional network-based contracts to define in this phase.

The primary "contract" is the structure of the `todos.json` file, which is detailed in `data-model.md`, and the command-line interface itself, which will be specified during the implementation phase.

## Internal Module Contracts

Internal contracts will be defined by the Python module interfaces within the `todo_cli/` directory (e.g., `storage.py`'s functions for reading/writing tasks, `models.py`'s `Task` class interface). These will be implicitly defined through the Python code itself, adhering to clear function signatures and type hints as per the project constitution.
