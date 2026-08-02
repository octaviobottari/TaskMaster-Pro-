from database import initialize_database
from db_manager import DBManager


def show_saved_tasks() -> None:
    """
    Displays all tasks currently stored in SQLite.
    """
    initialize_database()

    manager = DBManager()
    tasks = manager.get_all_tasks()

    print(
        f"Tasks currently stored: {len(tasks)}"
    )

    if not tasks:
        print("No saved tasks were found.")
        return

    for task in tasks:
        print(
            f'ID: {task["id"]} | '
            f'Title: {task["title"]} | '
            f'Date: {task["due_date"]} | '
            f'Priority: {task["priority"]} | '
            f'Category: {task["category"]} | '
            f'Status: {task["status"]}'
        )


if __name__ == "__main__":
    show_saved_tasks()