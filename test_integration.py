from datetime import date, timedelta

from database import initialize_database
from db_manager import DBManager


def run_integration_test() -> None:
    """
    Tests the integration between DBManager,
    task_repository and SQLite.
    """
    initialize_database()

    manager = DBManager()

    test_title = "W04 Integration Test"

    due_date = (
        date.today()
        + timedelta(days=7)
    ).isoformat()

    task_id = None

    try:
        print(
            "1. Creating a task through DBManager..."
        )

        task_id = manager.add_task(
            title=test_title,
            description=(
                "Test UI and SQLite integration"
            ),
            due_date=due_date,
            priority="High",
            category="Study",
        )

        assert isinstance(task_id, int)

        print(
            "2. Reading the created task..."
        )

        task = manager.get_task_by_id(task_id)

        assert task is not None
        assert task["title"] == test_title
        assert task["status"] == "Pending"

        print(
            "3. Updating the task..."
        )

        updated = manager.update_task(
            task_id,
            title=(
                "W04 Integration Test Updated"
            ),
            priority="Medium",
            category="Other",
        )

        assert updated is True

        task = manager.get_task_by_id(task_id)

        assert (
            task["title"]
            == "W04 Integration Test Updated"
        )

        assert task["priority"] == "Medium"
        assert task["category"] == "Other"

        print(
            "4. Toggling the task status..."
        )

        toggled = manager.toggle_status(
            task_id
        )

        assert toggled is True

        task = manager.get_task_by_id(task_id)

        assert task["status"] == "Completed"

        print(
            "5. Testing search and filters..."
        )

        search_results = manager.filter_tasks(
            search_term=(
                "integration test updated"
            )
        )

        assert any(
            task["id"] == task_id
            for task in search_results
        )

        completed_tasks = (
            manager.filter_tasks(
                status="Completed"
            )
        )

        assert any(
            task["id"] == task_id
            for task in completed_tasks
        )

        print(
            "6. Testing task statistics..."
        )

        total, pending, completed = (
            manager.get_stats()
        )

        assert total >= 1
        assert completed >= 1
        assert pending >= 0

        print(
            "7. Deleting the test task..."
        )

        deleted = manager.delete_task(task_id)

        assert deleted is True

        task_id = None

        print(
            "\nAll integration tests "
            "passed successfully."
        )

    finally:
        if task_id is not None:
            manager.delete_task(task_id)


if __name__ == "__main__":
    run_integration_test()