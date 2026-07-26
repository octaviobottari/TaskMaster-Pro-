# db_interface.py - Contract that Victor's db_manager must fulfill
from abc import ABC, abstractmethod

class DatabaseManager(ABC):
    """Interface that Victor's db_manager must implement."""

    @abstractmethod
    def add_task(self, title, description, due_date, priority, category):
        """
        Saves a task to the database.
        Returns: ID of the created task.
        """
        pass

    @abstractmethod
    def get_all_tasks(self):
        """
        Returns: List of dictionaries with all tasks.
        Each dictionary must contain: id, title, description, due_date, priority, category, status
        """
        pass

    @abstractmethod
    def get_task_by_id(self, task_id):
        """
        Returns: Task dictionary or None if not found.
        """
        pass

    @abstractmethod
    def update_task(self, task_id, **kwargs):
        """
        Updates fields of a task.
        Returns: True if updated, False if not found.
        """
        pass

    @abstractmethod
    def delete_task(self, task_id):
        """
        Deletes a task.
        Returns: True if deleted, False if not found.
        """
        pass

    @abstractmethod
    def toggle_status(self, task_id):
        """
        Toggles status between Pending and Completed.
        Returns: True if toggled, False if not found.
        """
        pass