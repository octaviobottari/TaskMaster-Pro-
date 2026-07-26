from db_interface import DatabaseManager
from task_repository import (
    create_task,
    delete_task,
    get_all_tasks,
    get_task_by_id,
    toggle_task_status,
    update_task,
)


class DBManager(DatabaseManager):
    """
    Connects the Tkinter user interface with the SQLite repository.
    """

    def add_task(
        self,
        title,
        description,
        due_date,
        priority,
        category,
    ):
        """
        Creates a new task and returns its generated ID.
        """
        return create_task(
            title=title,
            description=description,
            category=category,
            priority=priority,
            due_date=due_date,
        )

    def get_all_tasks(self):
        """
        Returns all tasks stored in SQLite.
        """
        return get_all_tasks()

    def get_task_by_id(self, task_id):
        """
        Returns one task or None if it does not exist.
        """
        return get_task_by_id(task_id)

    def update_task(self, task_id, **kwargs):
        """
        Updates only the fields provided by the interface.
        Existing values are preserved when a field is omitted.
        """
        task = self.get_task_by_id(task_id)

        if task is None:
            return False

        return update_task(
            task_id=task_id,
            title=kwargs.get("title", task["title"]),
            description=kwargs.get(
                "description",
                task["description"],
            ),
            category=kwargs.get(
                "category",
                task["category"],
            ),
            priority=kwargs.get(
                "priority",
                task["priority"],
            ),
            due_date=kwargs.get(
                "due_date",
                task["due_date"],
            ),
            status=kwargs.get(
                "status",
                task["status"],
            ),
        )

    def delete_task(self, task_id):
        """
        Deletes a task from SQLite.
        """
        return delete_task(task_id)

    def toggle_status(self, task_id):
        """
        Switches the task between Pending and Completed.
        """
        return toggle_task_status(task_id)

    def filter_tasks(
        self,
        status=None,
        search_term=None,
    ):
        """
        Filters tasks by status and search text.
        """
        tasks = self.get_all_tasks()

        if status:
            tasks = [
                task
                for task in tasks
                if task["status"] == status
            ]

        if search_term:
            term = search_term.strip().lower()

            tasks = [
                task
                for task in tasks
                if term in task["title"].lower()
                or term
                in (task.get("description") or "").lower()
            ]

        return tasks

    def get_stats(self):
        """
        Returns the total, pending and completed task counts.
        """
        tasks = self.get_all_tasks()

        total = len(tasks)

        pending = sum(
            task["status"] == "Pending"
            for task in tasks
        )

        completed = sum(
            task["status"] == "Completed"
            for task in tasks
        )

        return total, pending, completed