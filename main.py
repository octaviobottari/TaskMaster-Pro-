from database import initialize_database
from task_repository import get_all_tasks


def main() -> None:
    initialize_database()

    print("TaskMaster Pro")
    print("--------------------")

    tasks = get_all_tasks()

    if not tasks:
        print("No tasks found.")
        return

    for task in tasks:
        print(
            f'{task["id"]}. {task["title"]} | '
            f'{task["category"]} | '
            f'{task["priority"]} | '
            f'{task["status"]}'
        )


if __name__ == "__main__":
    main()