from datetime import datetime
from typing import Optional

from database import get_connection, initialize_database


VALID_CATEGORIES = {"Work", "Personal", "Study", "Urgent"}
VALID_PRIORITIES = {"Low", "Medium", "High"}
VALID_STATUSES = {"Pending", "Completed"}


def validate_task_data(
    title: str,
    category: str,
    priority: str,
    due_date: str,
    status: str = "Pending",
) -> None:
    """
    Validates task information before saving it.
    """
    if not title or not title.strip():
        raise ValueError("The task title is required.")

    if category not in VALID_CATEGORIES:
        raise ValueError(
            f"Invalid category. Choose one of: {', '.join(sorted(VALID_CATEGORIES))}"
        )

    if priority not in VALID_PRIORITIES:
        raise ValueError(
            f"Invalid priority. Choose one of: {', '.join(sorted(VALID_PRIORITIES))}"
        )

    if status not in VALID_STATUSES:
        raise ValueError(
            f"Invalid status. Choose one of: {', '.join(sorted(VALID_STATUSES))}"
        )

    try:
        datetime.strptime(due_date, "%Y-%m-%d")
    except ValueError as error:
        raise ValueError("The due date must use YYYY-MM-DD format.") from error


def row_to_dictionary(row) -> Optional[dict]:
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
        category=category,
        priority=priority,
        due_date=due_date,
    )

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
                description.strip() if description else "",
                category,
                priority,
                due_date,
            ),
        )

        connection.commit()
        return cursor.lastrowid


def get_task_by_id(task_id: int) -> Optional[dict]:
    """
    Returns one task by ID.
    Returns None when the task does not exist.
    """
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


def get_all_tasks() -> list[dict]:
    """
    Returns all tasks, ordered by due date.
    """
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
    Returns False if the ID was not found.
    """
    validate_task_data(
        title=title,
        category=category,
        priority=priority,
        due_date=due_date,
        status=status,
    )

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
                description.strip() if description else "",
                category,
                priority,
                due_date,
                status,
                task_id,
            ),
        )

        connection.commit()
        return cursor.rowcount > 0


def set_task_status(task_id: int, status: str) -> bool:
    """
    Changes a task status to Pending or Completed.
    """
    if status not in VALID_STATUSES:
        raise ValueError("Status must be Pending or Completed.")

    with get_connection() as connection:
        cursor = connection.execute(
            """
            UPDATE tasks
            SET status = ?
            WHERE id = ?;
            """,
            (status, task_id),
        )

        connection.commit()
        return cursor.rowcount > 0


def toggle_task_status(task_id: int) -> bool:
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

    return set_task_status(task_id, new_status)


def delete_task(task_id: int) -> bool:
    """
    Deletes a task by ID.

    Returns True if the task was deleted.
    Returns False if the task did not exist.
    """
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


initialize_database()