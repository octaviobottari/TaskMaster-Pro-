from datetime import date, timedelta

from database import (
    check_database_health,
    initialize_database,
)
from db_manager import DBManager


def run_integration_tests() -> None:
    """
    Complete final integration test for TaskMaster Pro.
    """
    initialize_database()

    assert check_database_health() is True

    manager = DBManager()
    task_id = None

    future_date = (
        date.today()
        + timedelta(days=7)
    ).isoformat()

    future_date_2 = (
        date.today()
        + timedelta(days=14)
    ).isoformat()

    try:
        print("1. Testing task creation...")

        task_id = manager.add_task(
            title="W06 Final Integration Test",
            description=(
                "Testing final application integration"
            ),
            due_date=future_date,
            priority="High",
            category="Study",
        )

        assert isinstance(task_id, int)

        print("   PASS")

        print("2. Testing task retrieval...")

        task = manager.get_task_by_id(
            task_id
        )

        assert task is not None
        assert task["status"] == "Pending"

        print("   PASS")

        print("3. Testing task update...")

        updated = manager.update_task(
            task_id,
            title="W06 Updated Final Task",
            description="Final integration test",
            due_date=future_date_2,
            priority="Medium",
            category="Other",
        )

        assert updated is True

        task = manager.get_task_by_id(
            task_id
        )

        assert task["title"] == (
            "W06 Updated Final Task"
        )

        print("   PASS")

        print("4. Testing status toggle...")

        changed = manager.toggle_status(
            task_id
        )

        assert changed is True

        task = manager.get_task_by_id(
            task_id
        )

        assert task["status"] == "Completed"

        print("   PASS")

        print("5. Testing title search...")

        results = manager.filter_tasks(
            search_term="updated final"
        )

        assert any(
            task["id"] == task_id
            for task in results
        )

        print("   PASS")

        print("6. Testing description search...")

        results = manager.filter_tasks(
            search_term="integration"
        )

        assert any(
            task["id"] == task_id
            for task in results
        )

        print("   PASS")

        print("7. Testing status filter...")

        results = manager.filter_tasks(
            status="Completed"
        )

        assert any(
            task["id"] == task_id
            for task in results
        )

        print("   PASS")

        print("8. Testing category filter...")

        results = manager.filter_tasks(
            category="Other"
        )

        assert any(
            task["id"] == task_id
            for task in results
        )

        print("   PASS")

        print("9. Testing priority filter...")

        results = manager.filter_tasks(
            priority="Medium"
        )

        assert any(
            task["id"] == task_id
            for task in results
        )

        print("   PASS")

        print("10. Testing statistics...")

        total, pending, completed = (
            manager.get_stats()
        )

        assert total >= 1
        assert pending >= 0
        assert completed >= 1

        print("   PASS")

        print("11. Testing invalid empty title...")

        try:
            manager.add_task(
                title="",
                description="Bad task",
                due_date=future_date,
                priority="High",
                category="Work",
            )

            raise AssertionError(
                "Empty title was accepted."
            )

        except ValueError:
            pass

        print("   PASS")

        print("12. Testing short title...")

        try:
            manager.add_task(
                title="Hi",
                description="Bad task",
                due_date=future_date,
                priority="High",
                category="Work",
            )

            raise AssertionError(
                "Short title was accepted."
            )

        except ValueError:
            pass

        print("   PASS")

        print("13. Testing invalid date...")

        try:
            manager.add_task(
                title="Invalid Date Task",
                description="Bad date",
                due_date="2026-99-99",
                priority="High",
                category="Work",
            )

            raise AssertionError(
                "Invalid date was accepted."
            )

        except ValueError:
            pass

        print("   PASS")

        print("14. Testing past date...")

        past_date = (
            date.today()
            - timedelta(days=1)
        ).isoformat()

        try:
            manager.add_task(
                title="Past Date Task",
                description="Past date test",
                due_date=past_date,
                priority="High",
                category="Work",
            )

            raise AssertionError(
                "Past date was accepted."
            )

        except ValueError:
            pass

        print("   PASS")

        print("15. Testing invalid category...")

        try:
            manager.add_task(
                title="Invalid Category Task",
                description="Category test",
                due_date=future_date,
                priority="High",
                category="FakeCategory",
            )

            raise AssertionError(
                "Invalid category was accepted."
            )

        except ValueError:
            pass

        print("   PASS")

        print("16. Testing persistence...")

        second_manager = DBManager()

        persisted_task = (
            second_manager.get_task_by_id(
                task_id
            )
        )

        assert persisted_task is not None
        assert persisted_task["id"] == task_id

        print("   PASS")

        print("17. Testing nonexistent task...")

        nonexistent = (
            manager.get_task_by_id(
                999999999
            )
        )

        assert nonexistent is None

        print("   PASS")

        print("18. Testing task deletion...")

        deleted = manager.delete_task(
            task_id
        )

        assert deleted is True

        task_id = None

        print("   PASS")

        print(
            "\nAll W06 final integration tests "
            "passed successfully."
        )

    finally:
        if task_id is not None:
            manager.delete_task(task_id)


if __name__ == "__main__":
    run_integration_tests()