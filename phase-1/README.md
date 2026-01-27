# Phase 1 - Todo CLI Application

This folder contains all files and artifacts from Phase 1 of the Todo App project.

## Overview
Phase 1 implements a basic command-line todo application with in-memory storage and CRUD operations.

## Contents

### Source Code (`src/`)
- `main.py` - Application entry point
- `models/task.py` - Task data model
- `repository.py` - In-memory task repository
- `services/task_service.py` - Task business logic
- `cli/commands.py` - CLI command implementations

### Specifications (`specs/001-task-crud-operations/`)
- `spec.md` - Feature specification
- `plan.md` - Implementation plan
- `tasks.md` - Task breakdown
- `data-model.md` - Data modeling decisions
- `checklists/requirements.md` - Requirements checklist
- `contracts/README.md` - API contracts
- `quickstart.md` - Quick start guide
- `research.md` - Research notes

### History (`history/prompts/`)
- Prompt History Records (PHRs) documenting the development process
- Constitution records defining project principles

### Configuration Files
- `requirements.txt` - Python dependencies
- `.gitignore` - Git ignore patterns
- `.flake8` - Flake8 linter configuration
- `.pylintrc` - Pylint configuration

## Features Implemented
- Create tasks with title and description
- Read/list all tasks
- Update task properties
- Delete tasks
- Mark tasks as complete/incomplete
- In-memory storage (no persistence)

## Running the Application
```bash
cd phase-1
python src/main.py
```

## Dependencies
Install dependencies with:
```bash
pip install -r requirements.txt
```
