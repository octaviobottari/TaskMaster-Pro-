from datetime import datetime
import sqlite3
from typing import Optional

from database import get_connection, initialize_database


VALID_CATEGORIES = {
    "Work",
    "Personal",
    "Study",
    "Urgent",
    "Other",
}

VALID_PRIORITIES = {
    "Low",
    "Medium",
    "High",
}

VALID_STATUSES = {
    "Pending",
    "Completed",
}

MAX_TITLE_LENGTH = 100
MAX_DESCRIPTION_LENGTH = 500


def validate_task_data(
    title: str,
    description: str,
    category: str,
    priority: str,
    due_date: str,
    status: str = "Pending",
) -> None:
    """
    Validates task information before saving it.
    """
    clean_title = title.strip() if title else ""
    clean_description = (
        description.strip()
        if description
        else ""
    )

    if not clean_title:
        raise ValueError(
            "The task title is required."
        )

    if len(clean_title) < 3:
        raise ValueError(
            "The task title must contain at least 3 characters."
        )

    if len(clean_title) > MAX_TITLE_LENGTH:
        raise ValueError(
            f"The task title cannot exceed "
            f"{MAX_TITLE_LENGTH} characters."
        )

    if len(clean_description) > MAX_DESCRIPTION_LENGTH:
        raise ValueError(
            f"The description cannot exceed "
            f"{MAX_DESCRIPTION_LENGTH} characters."
        )

    if category not in VALID_CATEGORIES:
        raise ValueError(
            "Invalid category. Choose one of: "
            f"{', '.join(sorted(VALID_CATEGORIES))}"
        )

    if priority not in VALID_PRIORITIES:
        raise ValueError(
            "Invalid priority. Choose one of: "
            f"{', '.join(sorted(VALID_PRIORITIES))}"
        )

    if status not in VALID_STATUSES:
        raise ValueError(
            "Invalid status. Choose one of: "
            f"{', '.join(sorted(VALID_STATUSES))}"
        )

    try:
        parsed_date = datetime.strptime(
            due_date,
            "%Y-%m-%d",
        ).date()

    except (TypeError, ValueError) as error:
        raise ValueError(
            "The due date must be valid and use "
            "the YYYY-MM-DD format."
        ) from error

    if parsed_date < datetime.today().date():
        raise ValueError(
            "The due date cannot be in the past."
        )


def row_to_dictionary(
    row: Optional[sqlite3.Row],
) -> Optional[dict]:
    """
    Converts a SQLite row into a regular Python dictionary.
    """
    return dict(row) if row is not None else None


def create_task(
    title: str,
    description: str,
    category: str,
    priority: str,
    due_date: str,
) -> int:
    """
    Creates a task and returns its generated ID.
    """
    validate_task_data(
        title=title,
        description=description,
        category=category,
        priority=priority,
        due_date=due_date,
    )

    try:
        with get_connection() as connection:
            cursor = connection.execute(
                """
                INSERT INTO tasks (
                    title,
                    description,
                    category,
                    priority,
                    due_date
                )
                VALUES (?, ?, ?, ?, ?);
                """,
                (
                    title.strip(),
                    description.strip()
                    if description
                    else "",
                    category,
                    priority,
                    due_date,
                ),
            )

            connection.commit()

            if cursor.lastrowid is None:
                raise RuntimeError(
                    "The task ID could not be generated."
                )

            return cursor.lastrowid

    except sqlite3.Error as error:
        raise RuntimeError(
            f"Unable to create the task: {error}"
        ) from error


def get_task_by_id(
    task_id: int,
) -> Optional[dict]:
    """
    Returns one task by ID.

    Returns None if the task does not exist.
    """
    if not isinstance(task_id, int) or task_id <= 0:
        raise ValueError(
            "Task ID must be a positive integer."
        )

    try:
        with get_connection() as connection:
            row = connection.execute(
                """
                SELECT
                    id,
                    title,
                    description,
                    category,
                    priority,
                    due_date,
                    status,
                    created_at
                FROM tasks
                WHERE id = ?;
                """,
                (task_id,),
            ).fetchone()

        return row_to_dictionary(row)

    except sqlite3.Error as error:
        raise RuntimeError(
            f"Unable to retrieve the task: {error}"
        ) from error


def get_all_tasks() -> list[dict]:
    """
    Returns all tasks ordered by due date and creation date.
    """
    try:
        with get_connection() as connection:
            rows = connection.execute(
                """
                SELECT
                    id,
                    title,
                    description,
                    category,
                    priority,
                    due_date,
                    status,
                    created_at
                FROM tasks
                ORDER BY due_date ASC, created_at DESC;
                """
            ).fetchall()

        return [dict(row) for row in rows]

    except sqlite3.Error as error:
        raise RuntimeError(
            f"Unable to retrieve tasks: {error}"
        ) from error


def update_task(
    task_id: int,
    title: str,
    description: str,
    category: str,
    priority: str,
    due_date: str,
    status: str,
) -> bool:
    """
    Updates an existing task.

    Returns True if a task was updated.
    Returns False if the task does not exist.
    """
    if not isinstance(task_id, int) or task_id <= 0:
        raise ValueError(
            "Task ID must be a positive integer."
        )

    validate_task_data(
        title=title,
        description=description,
        category=category,
        priority=priority,
        due_date=due_date,
        status=status,
    )

    try:
        with get_connection() as connection:
            cursor = connection.execute(
                """
                UPDATE tasks
                SET
                    title = ?,
                    description = ?,
                    category = ?,
                    priority = ?,
                    due_date = ?,
                    status = ?
                WHERE id = ?;
                """,
                (
                    title.strip(),
                    description.strip()
                    if description
                    else "",
                    category,
                    priority,
                    due_date,
                    status,
                    task_id,
                ),
            )

            connection.commit()
            return cursor.rowcount > 0

    except sqlite3.Error as error:
        raise RuntimeError(
            f"Unable to update the task: {error}"
        ) from error


def set_task_status(
    task_id: int,
    status: str,
) -> bool:
    """
    Changes a task status to Pending or Completed.
    """
    if not isinstance(task_id, int) or task_id <= 0:
        raise ValueError(
            "Task ID must be a positive integer."
        )

    if status not in VALID_STATUSES:
        raise ValueError(
            "Status must be Pending or Completed."
        )

    try:
        with get_connection() as connection:
            cursor = connection.execute(
                """
                UPDATE tasks
                SET status = ?
                WHERE id = ?;
                """,
                (
                    status,
                    task_id,
                ),
            )

            connection.commit()
            return cursor.rowcount > 0

    except sqlite3.Error as error:
        raise RuntimeError(
            f"Unable to update the task status: {error}"
        ) from error


def toggle_task_status(
    task_id: int,
) -> bool:
    """
    Switches a task between Pending and Completed.
    """
    task = get_task_by_id(task_id)

    if task is None:
        return False

    new_status = (
        "Completed"
        if task["status"] == "Pending"
        else "Pending"
    )

    return set_task_status(
        task_id,
        new_status,
    )


def delete_task(
    task_id: int,
) -> bool:
    """
    Deletes a task by ID.

    Returns True if the task was deleted.
    Returns False if the task did not exist.
    """
    if not isinstance(task_id, int) or task_id <= 0:
        raise ValueError(
            "Task ID must be a positive integer."
        )

    try:
        with get_connection() as connection:
            cursor = connection.execute(
                """
                DELETE FROM tasks
                WHERE id = ?;
                """,
                (task_id,),
            )

            connection.commit()
            return cursor.rowcount > 0

    except sqlite3.Error as error:
        raise RuntimeError(
            f"Unable to delete the task: {error}"
        ) from error


initialize_database()