import tkinter as tk
from datetime import datetime
from tkinter import messagebox, ttk

from mock_manager import MockTaskManager


CATEGORIES = [
    "Work",
    "Personal",
    "Study",
    "Urgent",
    "Other",
]

PRIORITIES = [
    "High",
    "Medium",
    "Low",
]


class TaskApp:
    def __init__(self, root, db_manager=None):
        self.root = root
        self.root.title("TaskMaster Pro")
        self.root.geometry("1150x650")
        self.root.minsize(900, 600)

        if db_manager is None:
            self.manager = MockTaskManager()
        else:
            self.manager = db_manager

        self.filter_var = tk.StringVar(value="All")
        self.search_var = tk.StringVar()

        self._build_widgets()
        self._refresh_treeview()

    def _build_widgets(self):
        self._build_top_panel()
        self._build_task_table()
        self._build_task_form()

    def _build_top_panel(self):
        top_frame = ttk.Frame(
            self.root,
            padding=10,
        )
        top_frame.pack(fill=tk.X)

        self.stats_label = ttk.Label(
            top_frame,
            text=(
                "Total: 0 | "
                "Pending: 0 | "
                "Completed: 0"
            ),
            font=("Arial", 11),
        )
        self.stats_label.pack(
            side=tk.LEFT,
            padx=5,
        )

        ttk.Separator(
            top_frame,
            orient=tk.VERTICAL,
        ).pack(
            side=tk.LEFT,
            padx=20,
            fill=tk.Y,
        )

        filter_frame = ttk.Frame(top_frame)
        filter_frame.pack(side=tk.LEFT)

        ttk.Label(
            filter_frame,
            text="Filter:",
        ).pack(
            side=tk.LEFT,
            padx=5,
        )

        for status in [
            "All",
            "Pending",
            "Completed",
        ]:
            ttk.Radiobutton(
                filter_frame,
                text=status,
                variable=self.filter_var,
                value=status,
                command=self._apply_filter,
            ).pack(
                side=tk.LEFT,
                padx=3,
            )

        search_frame = ttk.Frame(top_frame)
        search_frame.pack(side=tk.RIGHT)

        ttk.Label(
            search_frame,
            text="Search:",
        ).pack(
            side=tk.LEFT,
            padx=5,
        )

        self.search_entry = ttk.Entry(
            search_frame,
            textvariable=self.search_var,
            width=22,
        )
        self.search_entry.pack(
            side=tk.LEFT,
            padx=3,
        )

        self.search_entry.bind(
            "<Return>",
            lambda event: self._apply_filter(),
        )

        ttk.Button(
            search_frame,
            text="Search",
            command=self._apply_filter,
        ).pack(side=tk.LEFT)

        ttk.Button(
            search_frame,
            text="Clear",
            command=self._clear_search,
        ).pack(
            side=tk.LEFT,
            padx=3,
        )

    def _build_task_table(self):
        tree_frame = ttk.Frame(
            self.root,
            padding=10,
        )
        tree_frame.pack(
            fill=tk.BOTH,
            expand=True,
        )

        columns = (
            "ID",
            "Title",
            "Date",
            "Priority",
            "Category",
            "Status",
        )

        self.tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            height=15,
        )

        column_widths = {
            "ID": 50,
            "Title": 300,
            "Date": 120,
            "Priority": 100,
            "Category": 120,
            "Status": 120,
        }

        for column in columns:
            self.tree.heading(
                column,
                text=column,
                command=lambda selected_column=column:
                self._sort_by_column(
                    selected_column,
                    False,
                ),
            )

            self.tree.column(
                column,
                width=column_widths.get(
                    column,
                    100,
                ),
                anchor=(
                    "w"
                    if column == "Title"
                    else "center"
                ),
            )

        scrollbar = ttk.Scrollbar(
            tree_frame,
            orient=tk.VERTICAL,
            command=self.tree.yview,
        )

        self.tree.configure(
            yscrollcommand=scrollbar.set,
        )

        self.tree.pack(
            side=tk.LEFT,
            fill=tk.BOTH,
            expand=True,
        )

        scrollbar.pack(
            side=tk.RIGHT,
            fill=tk.Y,
        )

        self.tree.bind(
            "<Double-1>",
            lambda event: self._edit_task(),
        )

    def _build_task_form(self):
        form_frame = ttk.LabelFrame(
            self.root,
            text="Task Management",
            padding=15,
        )
        form_frame.pack(
            fill=tk.X,
            padx=10,
            pady=5,
        )

        ttk.Label(
            form_frame,
            text="Title:",
        ).grid(
            row=0,
            column=0,
            padx=5,
            pady=5,
            sticky="e",
        )

        self.title_entry = ttk.Entry(
            form_frame,
            width=40,
        )
        self.title_entry.grid(
            row=0,
            column=1,
            padx=5,
            pady=5,
            sticky="w",
        )

        ttk.Label(
            form_frame,
            text="Description:",
        ).grid(
            row=1,
            column=0,
            padx=5,
            pady=5,
            sticky="e",
        )

        self.desc_entry = ttk.Entry(
            form_frame,
            width=40,
        )
        self.desc_entry.grid(
            row=1,
            column=1,
            padx=5,
            pady=5,
            sticky="w",
        )

        ttk.Label(
            form_frame,
            text="Date (YYYY-MM-DD):",
        ).grid(
            row=2,
            column=0,
            padx=5,
            pady=5,
            sticky="e",
        )

        self.date_entry = ttk.Entry(
            form_frame,
            width=15,
        )
        self.date_entry.grid(
            row=2,
            column=1,
            padx=5,
            pady=5,
            sticky="w",
        )

        self.date_entry.insert(
            0,
            datetime.today().strftime(
                "%Y-%m-%d"
            ),
        )

        ttk.Label(
            form_frame,
            text="Priority:",
        ).grid(
            row=2,
            column=2,
            padx=5,
            pady=5,
            sticky="e",
        )

        self.priority_combo = ttk.Combobox(
            form_frame,
            values=PRIORITIES,
            state="readonly",
            width=10,
        )
        self.priority_combo.grid(
            row=2,
            column=3,
            padx=5,
            pady=5,
            sticky="w",
        )
        self.priority_combo.set("Medium")

        ttk.Label(
            form_frame,
            text="Category:",
        ).grid(
            row=2,
            column=4,
            padx=5,
            pady=5,
            sticky="e",
        )

        self.category_combo = ttk.Combobox(
            form_frame,
            values=CATEGORIES,
            state="readonly",
            width=12,
        )
        self.category_combo.grid(
            row=2,
            column=5,
            padx=5,
            pady=5,
            sticky="w",
        )
        self.category_combo.set("Work")

        button_frame = ttk.Frame(form_frame)
        button_frame.grid(
            row=3,
            column=0,
            columnspan=6,
            pady=10,
        )

        ttk.Button(
            button_frame,
            text="Add",
            command=self._add_task,
        ).pack(
            side=tk.LEFT,
            padx=5,
        )

        ttk.Button(
            button_frame,
            text="Edit Selected",
            command=self._edit_task,
        ).pack(
            side=tk.LEFT,
            padx=5,
        )

        ttk.Button(
            button_frame,
            text="Delete Selected",
            command=self._delete_task,
        ).pack(
            side=tk.LEFT,
            padx=5,
        )

        ttk.Button(
            button_frame,
            text="Toggle Status",
            command=self._toggle_task,
        ).pack(
            side=tk.LEFT,
            padx=5,
        )

        ttk.Button(
            button_frame,
            text="Refresh",
            command=self._refresh_treeview,
        ).pack(
            side=tk.LEFT,
            padx=5,
        )

    @staticmethod
    def _validate_task_data(
        title,
        due_date,
        priority,
        category,
    ):
        if not title:
            raise ValueError(
                "Title is required."
            )

        try:
            datetime.strptime(
                due_date,
                "%Y-%m-%d",
            )
        except ValueError as error:
            raise ValueError(
                "The date must be valid and use "
                "the YYYY-MM-DD format."
            ) from error

        if priority not in PRIORITIES:
            raise ValueError(
                "Please select a valid priority."
            )

        if category not in CATEGORIES:
            raise ValueError(
                "Please select a valid category."
            )

    def _get_selected_id(self):
        selected_items = self.tree.selection()

        if not selected_items:
            messagebox.showwarning(
                "Selection required",
                "Please select a task from the list.",
            )
            return None

        values = self.tree.item(
            selected_items[0],
            "values",
        )

        if not values:
            return None

        return int(values[0])

    def _add_task(self):
        title = self.title_entry.get().strip()
        description = self.desc_entry.get().strip()
        due_date = self.date_entry.get().strip()
        priority = self.priority_combo.get()
        category = self.category_combo.get()

        try:
            self._validate_task_data(
                title=title,
                due_date=due_date,
                priority=priority,
                category=category,
            )

            self.manager.add_task(
                title=title,
                description=description,
                due_date=due_date,
                priority=priority,
                category=category,
            )

        except ValueError as error:
            messagebox.showerror(
                "Validation Error",
                str(error),
            )
            return

        except Exception as error:
            messagebox.showerror(
                "Database Error",
                f"The task could not be saved.\n\n{error}",
            )
            return

        self._clear_form()
        self._refresh_treeview()

        messagebox.showinfo(
            "Task created",
            "The task was created successfully.",
        )

    def _clear_form(self):
        self.title_entry.delete(
            0,
            tk.END,
        )

        self.desc_entry.delete(
            0,
            tk.END,
        )

        self.date_entry.delete(
            0,
            tk.END,
        )

        self.date_entry.insert(
            0,
            datetime.today().strftime(
                "%Y-%m-%d"
            ),
        )

        self.priority_combo.set("Medium")
        self.category_combo.set("Work")
        self.title_entry.focus_set()

    def _edit_task(self):
        task_id = self._get_selected_id()

        if task_id is None:
            return

        task = self.manager.get_task_by_id(
            task_id
        )

        if task is None:
            messagebox.showerror(
                "Error",
                "The selected task does not exist.",
            )
            return

        edit_window = tk.Toplevel(self.root)
        edit_window.title(
            f"Edit Task #{task_id}"
        )
        edit_window.geometry("440x330")
        edit_window.resizable(False, False)
        edit_window.transient(self.root)
        edit_window.grab_set()

        title_var = tk.StringVar(
            value=task["title"]
        )

        description_var = tk.StringVar(
            value=task.get(
                "description",
                "",
            )
        )

        date_var = tk.StringVar(
            value=task["due_date"]
        )

        priority_var = tk.StringVar(
            value=task["priority"]
        )

        category_var = tk.StringVar(
            value=task["category"]
        )

        ttk.Label(
            edit_window,
            text="Title:",
        ).grid(
            row=0,
            column=0,
            padx=10,
            pady=10,
            sticky="e",
        )

        ttk.Entry(
            edit_window,
            textvariable=title_var,
            width=32,
        ).grid(
            row=0,
            column=1,
            padx=10,
            pady=10,
        )

        ttk.Label(
            edit_window,
            text="Description:",
        ).grid(
            row=1,
            column=0,
            padx=10,
            pady=10,
            sticky="e",
        )

        ttk.Entry(
            edit_window,
            textvariable=description_var,
            width=32,
        ).grid(
            row=1,
            column=1,
            padx=10,
            pady=10,
        )

        ttk.Label(
            edit_window,
            text="Date (YYYY-MM-DD):",
        ).grid(
            row=2,
            column=0,
            padx=10,
            pady=10,
            sticky="e",
        )

        ttk.Entry(
            edit_window,
            textvariable=date_var,
            width=32,
        ).grid(
            row=2,
            column=1,
            padx=10,
            pady=10,
        )

        ttk.Label(
            edit_window,
            text="Priority:",
        ).grid(
            row=3,
            column=0,
            padx=10,
            pady=10,
            sticky="e",
        )

        ttk.Combobox(
            edit_window,
            values=PRIORITIES,
            textvariable=priority_var,
            state="readonly",
            width=29,
        ).grid(
            row=3,
            column=1,
            padx=10,
            pady=10,
        )

        ttk.Label(
            edit_window,
            text="Category:",
        ).grid(
            row=4,
            column=0,
            padx=10,
            pady=10,
            sticky="e",
        )

        ttk.Combobox(
            edit_window,
            values=CATEGORIES,
            textvariable=category_var,
            state="readonly",
            width=29,
        ).grid(
            row=4,
            column=1,
            padx=10,
            pady=10,
        )

        def save_changes():
            new_title = title_var.get().strip()
            new_description = (
                description_var.get().strip()
            )
            new_date = date_var.get().strip()
            new_priority = priority_var.get()
            new_category = category_var.get()

            try:
                self._validate_task_data(
                    title=new_title,
                    due_date=new_date,
                    priority=new_priority,
                    category=new_category,
                )

                updated = self.manager.update_task(
                    task_id,
                    title=new_title,
                    description=new_description,
                    due_date=new_date,
                    priority=new_priority,
                    category=new_category,
                )

                if not updated:
                    raise ValueError(
                        "The task could not be updated."
                    )

            except ValueError as error:
                messagebox.showerror(
                    "Validation Error",
                    str(error),
                    parent=edit_window,
                )
                return

            except Exception as error:
                messagebox.showerror(
                    "Database Error",
                    (
                        "The task could not be "
                        f"updated.\n\n{error}"
                    ),
                    parent=edit_window,
                )
                return

            edit_window.destroy()
            self._refresh_treeview()

            messagebox.showinfo(
                "Task updated",
                "The task was updated successfully.",
            )

        ttk.Button(
            edit_window,
            text="Save Changes",
            command=save_changes,
        ).grid(
            row=5,
            column=0,
            columnspan=2,
            pady=20,
        )

    def _delete_task(self):
        task_id = self._get_selected_id()

        if task_id is None:
            return

        confirmed = messagebox.askyesno(
            "Confirm deletion",
            (
                "Are you sure you want to "
                f"delete task #{task_id}?"
            ),
        )

        if not confirmed:
            return

        try:
            deleted = self.manager.delete_task(
                task_id
            )

            if not deleted:
                messagebox.showerror(
                    "Error",
                    "The task could not be deleted.",
                )
                return

        except Exception as error:
            messagebox.showerror(
                "Database Error",
                (
                    "The task could not be "
                    f"deleted.\n\n{error}"
                ),
            )
            return

        self._refresh_treeview()

        messagebox.showinfo(
            "Task deleted",
            "The task was deleted successfully.",
        )

    def _toggle_task(self):
        task_id = self._get_selected_id()

        if task_id is None:
            return

        try:
            changed = self.manager.toggle_status(
                task_id
            )

            if not changed:
                messagebox.showerror(
                    "Error",
                    "The task status could not be changed.",
                )
                return

        except Exception as error:
            messagebox.showerror(
                "Database Error",
                (
                    "The task status could not "
                    f"be changed.\n\n{error}"
                ),
            )
            return

        self._refresh_treeview()

    def _clear_search(self):
        self.search_var.set("")
        self._apply_filter()

    def _apply_filter(self):
        self._refresh_treeview()

    def _sort_by_column(
        self,
        column,
        reverse,
    ):
        column_map = {
            "ID": "id",
            "Title": "title",
            "Date": "due_date",
            "Priority": "priority",
            "Category": "category",
            "Status": "status",
        }

        key = column_map.get(
            column,
            "id",
        )

        items = self.tree.get_children("")

        if not items:
            return

        data = []

        for item in items:
            values = self.tree.item(
                item,
                "values",
            )

            task_id = int(values[0])

            task = self.manager.get_task_by_id(
                task_id
            )

            if task:
                data.append(
                    (
                        task,
                        item,
                    )
                )

        priority_order = {
            "High": 0,
            "Medium": 1,
            "Low": 2,
        }

        def sort_value(task_item):
            task, _ = task_item
            value = task.get(key, "")

            if key == "priority":
                return priority_order.get(
                    value,
                    99,
                )

            if key == "due_date":
                try:
                    return datetime.strptime(
                        value,
                        "%Y-%m-%d",
                    )
                except ValueError:
                    return datetime.min

            if key == "id":
                return int(value)

            return str(value).lower()

        data.sort(
            key=sort_value,
            reverse=reverse,
        )

        for index, (_, item) in enumerate(data):
            self.tree.move(
                item,
                "",
                index,
            )

        self.tree.heading(
            column,
            command=lambda:
            self._sort_by_column(
                column,
                not reverse,
            ),
        )

    def _refresh_treeview(self):
        status_filter = self.filter_var.get()
        search_term = self.search_var.get().strip()

        status_map = {
            "All": None,
            "Pending": "Pending",
            "Completed": "Completed",
        }

        status = status_map.get(
            status_filter
        )

        try:
            tasks = self.manager.filter_tasks(
                status=status,
                search_term=(
                    search_term
                    if search_term
                    else None
                ),
            )

            total, pending, completed = (
                self.manager.get_stats()
            )

        except Exception as error:
            messagebox.showerror(
                "Database Error",
                (
                    "The tasks could not be "
                    f"loaded.\n\n{error}"
                ),
            )
            return

        self.stats_label.config(
            text=(
                f"Total: {total} | "
                f"Pending: {pending} | "
                f"Completed: {completed}"
            )
        )

        for item in self.tree.get_children(""):
            self.tree.delete(item)

        for task in tasks:
            self.tree.insert(
                "",
                tk.END,
                values=(
                    task["id"],
                    task["title"],
                    task["due_date"],
                    task["priority"],
                    task["category"],
                    task["status"],
                ),
            )


if __name__ == "__main__":
    root = tk.Tk()
    TaskApp(root)
    root.mainloop()