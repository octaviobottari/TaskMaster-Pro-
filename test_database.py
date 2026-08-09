from datetime import date, timedelta

from database import (
    check_database_health,
    initialize_database,
)
from task_repository import (
    create_task,
    delete_task,
    get_all_tasks,
    get_task_by_id,
    toggle_task_status,
    update_task,
)


def run_tests() -> None:
    initialize_database()

    assert check_database_health() is True

    future_date = (
        date.today()
        + timedelta(days=7)
    ).isoformat()

    updated_date = (
        date.today()
        + timedelta(days=10)
    ).isoformat()

    task_id = None

    try:
        print("1. Creating task...")

        task_id = create_task(
            title="Complete Final Sprint",
            description=(
                "Test database CRUD operations "
                "for the final sprint"
            ),
            category="Study",
            priority="High",
            due_date=future_date,
        )

        assert isinstance(task_id, int)

        print(
            f"   Task created with ID: {task_id}"
        )

        print("2. Reading task...")

        task = get_task_by_id(task_id)

        assert task is not None
        assert task["title"] == (
            "Complete Final Sprint"
        )

        print("   Read passed.")

        print("3. Updating task...")

        updated = update_task(
            task_id=task_id,
            title="Complete TaskMaster Pro",
            description=(
                "Finish and verify final "
                "database implementation"
            ),
            category="Study",
            priority="Medium",
            due_date=updated_date,
            status="Pending",
        )

        assert updated is True

        task = get_task_by_id(task_id)

        assert task["title"] == (
            "Complete TaskMaster Pro"
        )

        print("   Update passed.")

        print("4. Changing task status...")

        status_changed = (
            toggle_task_status(task_id)
        )

        assert status_changed is True

        task = get_task_by_id(task_id)

        assert task["status"] == "Completed"

        print("   Status change passed.")

        print("5. Reading all tasks...")

        tasks = get_all_tasks()

        assert any(
            task["id"] == task_id
            for task in tasks
        )

        print("   Read all passed.")

        print("6. Testing nonexistent task...")

        missing_task = get_task_by_id(
            999999999
        )

        assert missing_task is None

        print(
            "   Nonexistent task handling passed."
        )

        print("7. Deleting task...")

        deleted = delete_task(task_id)

        assert deleted is True

        task_id = None

        print("   Delete passed.")

        print(
            "\nAll database tests passed successfully."
        )

    finally:
        if task_id is not None:
            delete_task(task_id)


if __name__ == "__main__":
    run_tests()