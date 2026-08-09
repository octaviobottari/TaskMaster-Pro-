from datetime import date, timedelta

from database import (
    check_database_health,
    initialize_database,
)
from db_manager import DBManager


def run_persistence_test() -> None:
    """
    Verifies that tasks remain available across
    separate DBManager instances.
    """
    initialize_database()

    assert check_database_health() is True

    manager = DBManager()

    future_date = (
        date.today()
        + timedelta(days=30)
    ).isoformat()

    task_id = None

    try:
        print(
            "Creating persistence test task..."
        )

        task_id = manager.add_task(
            title="Persistence Verification Task",
            description=(
                "Final Sprint persistence test"
            ),
            due_date=future_date,
            priority="Low",
            category="Personal",
        )

        assert isinstance(task_id, int)

        print(
            f"Task created with ID: {task_id}"
        )

        print(
            "Opening a new database manager..."
        )

        second_manager = DBManager()

        task = second_manager.get_task_by_id(
            task_id
        )

        assert task is not None
        assert task["id"] == task_id
        assert task["title"] == (
            "Persistence Verification Task"
        )

        print(
            "Persistence test passed successfully."
        )

    finally:
        if task_id is not None:
            manager.delete_task(task_id)

            print(
                "Persistence test task removed."
            )


if __name__ == "__main__":
    run_persistence_test()