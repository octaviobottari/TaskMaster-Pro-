from collections.abc import Callable
from typing import Any

from task_repository import (
    create_task,
    delete_task,
    get_all_tasks,
    get_task_by_id,
    toggle_task_status,
    update_task,
)


class DBManager:
    """
    Adapter that connects the graphical interface
    with the task repository.
    """

    @staticmethod
    def _execute(
        operation: Callable[[], Any],
        operation_name: str,
    ) -> Any:
        """
        Executes a repository operation and provides
        a clearer error message if it fails.
        """
        try:
            return operation()

        except ValueError:
            raise

        except RuntimeError:
            raise

        except Exception as error:
            raise RuntimeError(
                f"{operation_name} failed: {error}"
            ) from error

    def add_task(
        self,
        title,
        description,
        due_date,
        priority,
        category,
    ):
        """
        Creates a task and returns its generated ID.
        """
        return self._execute(
            lambda: create_task(
                title=title,
                description=description,
                category=category,
                priority=priority,
                due_date=due_date,
            ),
            "Creating the task",
        )

    def get_all_tasks(self):
        """
        Returns all tasks as dictionaries.
        """
        return self._execute(
            get_all_tasks,
            "Loading tasks",
        )

    def get_task_by_id(
        self,
        task_id,
    ):
        """
        Returns a task by ID or None.
        """
        return self._execute(
            lambda: get_task_by_id(task_id),
            "Loading the task",
        )

    def update_task(
        self,
        task_id,
        **kwargs,
    ):
        """
        Updates a task while preserving values
        that were not supplied.
        """
        task = self.get_task_by_id(task_id)

        if task is None:
            return False

        title = kwargs.get(
            "title",
            task["title"],
        )

        description = kwargs.get(
            "description",
            task["description"],
        )

        category = kwargs.get(
            "category",
            task["category"],
        )

        priority = kwargs.get(
            "priority",
            task["priority"],
        )

        due_date = kwargs.get(
            "due_date",
            task["due_date"],
        )

        status = kwargs.get(
            "status",
            task["status"],
        )

        return self._execute(
            lambda: update_task(
                task_id=task_id,
                title=title,
                description=description,
                category=category,
                priority=priority,
                due_date=due_date,
                status=status,
            ),
            "Updating the task",
        )

    def delete_task(
        self,
        task_id,
    ):
        """
        Deletes a task.
        """
        return self._execute(
            lambda: delete_task(task_id),
            "Deleting the task",
        )

    def toggle_status(
        self,
        task_id,
    ):
        """
        Changes the task between Pending and Completed.
        """
        return self._execute(
            lambda: toggle_task_status(task_id),
            "Changing the task status",
        )

    def filter_tasks(
        self,
        status=None,
        search_term=None,
        category=None,
        priority=None,
    ):
        """
        Filters tasks by status, search term,
        category, and priority.
        """
        tasks = self.get_all_tasks()

        if status:
            tasks = [
                task
                for task in tasks
                if task["status"] == status
            ]

        if category:
            tasks = [
                task
                for task in tasks
                if task["category"] == category
            ]

        if priority:
            tasks = [
                task
                for task in tasks
                if task["priority"] == priority
            ]

        if search_term:
            term = search_term.strip().lower()

            tasks = [
                task
                for task in tasks
                if (
                    term
                    in task["title"].lower()
                    or term
                    in (
                        task.get("description")
                        or ""
                    ).lower()
                )
            ]

        return tasks

    def get_stats(self):
        """
        Returns total, pending, and completed counts.
        """
        tasks = self.get_all_tasks()

        total = len(tasks)

        pending = sum(
            1
            for task in tasks
            if task["status"] == "Pending"
        )

        completed = sum(
            1
            for task in tasks
            if task["status"] == "Completed"
        )

        return (
            total,
            pending,
            completed,
        )