from datetime import date, timedelta

from database import initialize_database
from db_manager import DBManager


def run_integration_tests() -> None:
    """
    Tests the connection between DBManager,
    task_repository, and SQLite.
    """
    initialize_database()

    manager = DBManager()
    task_id = None

    future_date = (
        date.today()
        + timedelta(days=7)
    ).isoformat()

    try:
        print("1. Testing task creation...")

        task_id = manager.add_task(
            title="W05 Integration Test",
            description=(
                "Testing database stability "
                "and persistence"
            ),
            due_date=future_date,
            priority="High",
            category="Study",
        )

        assert isinstance(task_id, int)
        print("   Task creation passed.")

        print("2. Testing task retrieval...")

        task = manager.get_task_by_id(
            task_id
        )

        assert task is not None
        assert task["title"] == (
            "W05 Integration Test"
        )
        assert task["status"] == "Pending"

        print("   Task retrieval passed.")

        print("3. Testing task update...")

        updated = manager.update_task(
            task_id,
            title="W05 Updated Task",
            description=(
                "Updated integration test"
            ),
            priority="Medium",
            category="Other",
        )

        assert updated is True

        task = manager.get_task_by_id(
            task_id
        )

        assert task["title"] == (
            "W05 Updated Task"
        )
        assert task["priority"] == "Medium"
        assert task["category"] == "Other"

        print("   Task update passed.")

        print("4. Testing status change...")

        changed = manager.toggle_status(
            task_id
        )

        assert changed is True

        task = manager.get_task_by_id(
            task_id
        )

        assert task["status"] == "Completed"

        print("   Status change passed.")

        print("5. Testing search...")

        search_results = manager.filter_tasks(
            search_term="updated task"
        )

        assert any(
            result["id"] == task_id
            for result in search_results
        )

        print("   Search passed.")

        print("6. Testing status filter...")

        completed_results = (
            manager.filter_tasks(
                status="Completed"
            )
        )

        assert any(
            result["id"] == task_id
            for result in completed_results
        )

        print("   Status filter passed.")

        print("7. Testing statistics...")

        total, pending, completed = (
            manager.get_stats()
        )

        assert total >= 1
        assert pending >= 0
        assert completed >= 1

        print("   Statistics passed.")

        print("8. Testing invalid title...")

        try:
            manager.add_task(
                title="",
                description="Invalid title test",
                due_date=future_date,
                priority="High",
                category="Work",
            )

            raise AssertionError(
                "An empty title was accepted."
            )

        except ValueError:
            print(
                "   Invalid title validation passed."
            )

        print("9. Testing short title...")

        try:
            manager.add_task(
                title="Hi",
                description="Short title test",
                due_date=future_date,
                priority="High",
                category="Work",
            )

            raise AssertionError(
                "A short title was accepted."
            )

        except ValueError:
            print(
                "   Short title validation passed."
            )

        print("10. Testing invalid date...")

        try:
            manager.add_task(
                title="Invalid Date Test",
                description="Invalid date",
                due_date="2026-99-99",
                priority="High",
                category="Work",
            )

            raise AssertionError(
                "An invalid date was accepted."
            )

        except ValueError:
            print(
                "   Invalid date validation passed."
            )

        print("11. Testing past date...")

        past_date = (
            date.today()
            - timedelta(days=1)
        ).isoformat()

        try:
            manager.add_task(
                title="Past Date Test",
                description="Past date",
                due_date=past_date,
                priority="High",
                category="Work",
            )

            raise AssertionError(
                "A past date was accepted."
            )

        except ValueError:
            print(
                "   Past date validation passed."
            )

        print("12. Testing persistence...")

        second_manager = DBManager()

        persisted_task = (
            second_manager.get_task_by_id(
                task_id
            )
        )

        assert persisted_task is not None
        assert persisted_task["id"] == task_id

        print("   Persistence passed.")

        print("13. Testing task deletion...")

        deleted = manager.delete_task(
            task_id
        )

        assert deleted is True

        task_id = None

        print("   Task deletion passed.")

        print(
            "\nAll W05 integration tests "
            "passed successfully."
        )

    finally:
        if task_id is not None:
            manager.delete_task(task_id)


if __name__ == "__main__":
    run_integration_tests()