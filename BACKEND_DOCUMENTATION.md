# TaskMaster Pro - Backend Documentation

## Overview

TaskMaster Pro is a Python desktop task management application that uses Tkinter for the graphical user interface and SQLite for local data storage.

The backend is designed with separation between the user interface, database adapter, repository layer, and SQLite database.

## Architecture

The application follows this general flow:

User Interface
↓
DBManager
↓
Task Repository
↓
SQLite Database

### taskmaster_ui.py

This file contains the Tkinter graphical interface. It collects user input, displays task information, and communicates with DBManager.

The user interface does not directly execute SQL queries.

### db_manager.py

DBManager acts as an adapter between the graphical interface and the repository.

It provides operations for:

- Creating tasks
- Reading tasks
- Updating tasks
- Deleting tasks
- Changing task status
- Filtering tasks
- Searching tasks
- Calculating task statistics

It also centralizes exception handling for repository operations.

### task_repository.py

The repository contains the core CRUD operations and validation logic.

Supported operations include:

- create_task
- get_task_by_id
- get_all_tasks
- update_task
- delete_task
- set_task_status
- toggle_task_status

Validation includes:

- Required task titles
- Minimum title length
- Maximum title length
- Maximum description length
- Valid categories
- Valid priorities
- Valid task statuses
- Valid YYYY-MM-DD dates
- Prevention of past due dates
- Valid positive task IDs

### database.py

The database module manages SQLite connections and initializes the application database.

The database file is:

taskmaster.db

The main table is:

tasks

Fields:

- id
- title
- description
- category
- priority
- due_date
- status
- created_at

Indexes are created for:

- category
- priority
- due_date
- status
- title

The database module also provides an SQLite integrity check.

## Database Storage

TaskMaster Pro uses SQLite because it is lightweight, local, and requires no external database server.

All application data is stored on the user's computer.

The database persists after the application is closed.

## Error Handling

Database errors are caught and converted into clear RuntimeError messages.

Validation errors use ValueError so invalid user data can be displayed safely in the graphical interface.

The application also performs a database integrity check when it starts.

## Testing

TaskMaster Pro includes several testing files.

### test_database.py

Tests repository-level CRUD functionality.

### test_integration.py

Tests complete integration between:

DBManager
Task Repository
SQLite

It verifies:

- Create
- Read
- Update
- Delete
- Status changes
- Search
- Status filters
- Category filters
- Priority filters
- Statistics
- Validation
- Persistence
- Missing task handling

### test_persistence.py

Verifies that saved tasks remain available through separate database manager instances.

## Application Entry Point

The official application entry point is:

python main.py

main.py initializes SQLite, checks database integrity, creates DBManager, and opens the Tkinter graphical interface.

## Final Backend Status

The final backend supports all planned TaskMaster Pro task-management operations and has automated tests for core functionality, validation, database persistence, and integration.