# Phase 1: Console Todo Application

This is the Phase 1 implementation of the Todo application as part of the Evolution of Todo project. This is a console-based application developed in Python following object-oriented principles.

## Architecture

The application follows a 4-layer architecture:
- **Models**: Task entity definitions
- **Services**: Business logic for task management
- **CLI**: Command-line interface and user interaction
- **Validators**: Input validation logic
- **Exceptions**: Custom exception handling

## Features

- Add, update, delete, and view tasks
- Mark tasks as complete/incomplete
- Console-based menu interface
- Input validation
- Error handling

## Project Structure

```
console-todo/
├── main.py                 # Entry point
├── models/
│   └── task.py            # Task entity
├── services/
│   └── task_service.py    # Task business logic
├── cli/
│   ├── menu.py            # Menu interface
│   ├── handlers.py        # Command handlers
│   └── colors.py          # Color utilities
├── validators/
│   └── input_validators.py # Input validation
└── exceptions/
    └── errors.py          # Custom exceptions
```

## Running the Application

To run this console application:

```bash
cd phase-1/console-todo
python main.py
```

This represents the initial phase of the Evolution of Todo project before transitioning to a full-stack web application in Phase 2.