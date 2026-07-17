from database import initialize_database
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

    print("1. Creating task...")

    task_id = create_task(
        title="Complete Sprint 1",
        description="Finish database and CRUD operations",
        category="Study",
        priority="High",
        due_date="2026-07-20",
    )

    print(f"Task created with ID: {task_id}")

    print("\n2. Reading task...")

    task = get_task_by_id(task_id)
    print(task)

    print("\n3. Updating task...")

    updated = update_task(
        task_id=task_id,
        title="Complete TaskMaster Pro Sprint 1",
        description="Finish and test SQLite CRUD operations",
        category="Study",
        priority="High",
        due_date="2026-07-21",
        status="Pending",
    )

    print(f"Task updated: {updated}")
    print(get_task_by_id(task_id))

    print("\n4. Changing task status...")

    status_changed = toggle_task_status(task_id)
    print(f"Status changed: {status_changed}")
    print(get_task_by_id(task_id))

    print("\n5. Showing all tasks...")

    for task in get_all_tasks():
        print(task)

    print("\n6. Deleting test task...")

    deleted = delete_task(task_id)
    print(f"Task deleted: {deleted}")

    print("\n7. Confirming deletion...")

    deleted_task = get_task_by_id(task_id)
    print(deleted_task)

    print("\nAll tests completed successfully.")


if __name__ == "__main__":
    run_tests()