# mock_manager.py - Mock para probar la UI sin BD
class MockTaskManager:
    def __init__(self):
        self.tasks = []
        self.next_id = 1
        self._load_mock_data()

    def _load_mock_data(self):
        """Carga tareas de ejemplo para probar la UI."""
        sample = [
            {
                "title": "Review sprint",
                "description": "Check all deliverables",
                "due_date": "2026-07-20",
                "priority": "High",
                "category": "Work",
                "status": "Pending"
            },
            {
                "title": "Buy gift",
                "description": "Birthday present",
                "due_date": "2026-07-18",
                "priority": "Medium",
                "category": "Personal",
                "status": "Completed"
            },
            {
                "title": "Study SQLite",
                "description": "Practice joins and queries",
                "due_date": "2026-07-22",
                "priority": "High",
                "category": "Study",
                "status": "Pending"
            },
        ]
        for task in sample:
            self.add_task(
                task["title"],
                task["description"],
                task["due_date"],
                task["priority"],
                task["category"],
                task["status"]
            )

    def add_task(self, title, description, due_date, priority, category, status="Pending"):
        new_task = {
            "id": self.next_id,
            "title": title,
            "description": description,
            "due_date": due_date,
            "priority": priority,
            "category": category,
            "status": status
        }
        self.tasks.append(new_task)
        self.next_id += 1
        return new_task["id"]

    def get_all_tasks(self):
        return self.tasks

    def get_task_by_id(self, task_id):
        for task in self.tasks:
            if task["id"] == task_id:
                return task
        return None

    def update_task(self, task_id, **kwargs):
        task = self.get_task_by_id(task_id)
        if task:
            for key, value in kwargs.items():
                if key in task:
                    task[key] = value
            return True
        return False

    def delete_task(self, task_id):
        for i, task in enumerate(self.tasks):
            if task["id"] == task_id:
                del self.tasks[i]
                return True
        return False

    def toggle_status(self, task_id):
        task = self.get_task_by_id(task_id)
        if task:
            task["status"] = "Completed" if task["status"] == "Pending" else "Pending"
            return True
        return False

    def filter_tasks(self, status=None, search_term=None):
        result = self.tasks
        if status:
            result = [t for t in result if t["status"] == status]
        if search_term:
            term = search_term.lower()
            result = [
                t for t in result
                if term in t["title"].lower() or term in t.get("description", "").lower()
            ]
        return result

    def get_stats(self):
        total = len(self.tasks)
        pending = sum(1 for t in self.tasks if t["status"] == "Pending")
        completed = total - pending
        return total, pending, completed