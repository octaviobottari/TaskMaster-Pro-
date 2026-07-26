# db_manager.py - Adapter to use Victor's task_repository with the UI
from task_repository import (
    create_task,
    get_all_tasks,
    get_task_by_id,
    update_task,
    delete_task,
    toggle_task_status,
)


class DBManager:
    """
    Adapter that implements the DatabaseManager interface
    using Victor's task_repository functions.
    """

    def add_task(self, title, description, due_date, priority, category):
        """
        Creates a task and returns its ID.
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
        Returns all tasks as a list of dictionaries.
        """
        return get_all_tasks()

    def get_task_by_id(self, task_id):
        """
        Returns a task by ID or None.
        """
        return get_task_by_id(task_id)

    def update_task(self, task_id, **kwargs):
        """
        Updates a task. Returns True if successful.
        """
        # Get current task data
        task = self.get_task_by_id(task_id)
        if not task:
            return False

        # Use existing values if not provided
        title = kwargs.get("title", task["title"])
        description = kwargs.get("description", task["description"])
        category = kwargs.get("category", task["category"])
        priority = kwargs.get("priority", task["priority"])
        due_date = kwargs.get("due_date", task["due_date"])
        status = kwargs.get("status", task["status"])

        return update_task(
            task_id=task_id,
            title=title,
            description=description,
            category=category,
            priority=priority,
            due_date=due_date,
            status=status,
        )

    def delete_task(self, task_id):
        """
        Deletes a task. Returns True if successful.
        """
        return delete_task(task_id)

    def toggle_status(self, task_id):
        """
        Toggles status between Pending and Completed. Returns True if successful.
        """
        return toggle_task_status(task_id)

    def filter_tasks(self, status=None, search_term=None):
        """
        Filters tasks by status and search term.
        Victor's repository doesn't have filters, so we implement them here.
        """
        tasks = self.get_all_tasks()
        if status:
            tasks = [t for t in tasks if t["status"] == status]
        if search_term:
            term = search_term.lower()
            tasks = [
                t for t in tasks
                if term in t["title"].lower() or term in t.get("description", "").lower()
            ]
        return tasks

    def get_stats(self):
        """
        Returns (total, pending, completed).
        """
        tasks = self.get_all_tasks()
        total = len(tasks)
        pending = sum(1 for t in tasks if t["status"] == "Pending")
        completed = total - pending
        return total, pending, completed