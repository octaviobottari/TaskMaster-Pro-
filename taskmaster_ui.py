import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import re
from mock_manager import MockTaskManager


class TaskApp:
    def __init__(self, root, db_manager=None):
        self.root = root
        self.root.title("TaskMaster Pro")
        self.root.geometry("1150x650")
        self.root.resizable(True, True)


        if db_manager is None:
            self.manager = MockTaskManager()  # Mock 
        else:
            self.manager = db_manager          # real DB

        
        self.filter_var = tk.StringVar(value="All")
        self.search_var = tk.StringVar()

        self._build_widgets()
        self._refresh_treeview()

    def _build_widgets(self):
        # -----------------------------------------------------------
        # top panel
        # -----------------------------------------------------------
        top_frame = ttk.Frame(self.root, padding=10)
        top_frame.pack(fill=tk.X)

        self.stats_label = ttk.Label(
            top_frame,
            text="📊 Total: 0 | ⏳ Pending: 0 | ✅ Completed: 0",
            font=("Arial", 11)
        )
        self.stats_label.pack(side=tk.LEFT, padx=5)

        ttk.Separator(top_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, padx=20, fill=tk.Y)

        # Filters
        filter_frame = ttk.Frame(top_frame)
        filter_frame.pack(side=tk.LEFT)
        ttk.Label(filter_frame, text="Filter:").pack(side=tk.LEFT, padx=5)

        for status in ["All", "Pending", "Completed"]:
            rb = ttk.Radiobutton(
                filter_frame,
                text=status,
                variable=self.filter_var,
                value=status,
                command=self._apply_filter
            )
            rb.pack(side=tk.LEFT, padx=3)

        # Search
        search_frame = ttk.Frame(top_frame)
        search_frame.pack(side=tk.RIGHT)
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=5)
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=20)
        self.search_entry.pack(side=tk.LEFT, padx=3)
        ttk.Button(search_frame, text="🔍 Search", command=self._apply_filter).pack(side=tk.LEFT)
        ttk.Button(search_frame, text="Clear", command=self._clear_search).pack(side=tk.LEFT, padx=3)

        # -----------------------------------------------------------
        # Treeview
        # -----------------------------------------------------------
        tree_frame = ttk.Frame(self.root, padding=10)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("ID", "Title", "Date", "Priority", "Category", "Status")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)

        col_widths = {"ID": 50, "Title": 300, "Date": 120, "Priority": 100, "Category": 120, "Status": 120}
        for col in columns:
            self.tree.heading(
                col,
                text=col,
                command=lambda c=col: self._sort_by_column(c, False)
            )
            self.tree.column(
                col,
                width=col_widths.get(col, 100),
                anchor="center" if col != "Title" else "w"
            )

        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # -----------------------------------------------------------
        # Form
        # -----------------------------------------------------------
        form_frame = ttk.LabelFrame(self.root, text="Task Management", padding=15)
        form_frame.pack(fill=tk.X, padx=10, pady=5)

      
        ttk.Label(form_frame, text="Title:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.title_entry = ttk.Entry(form_frame, width=40)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

       
        ttk.Label(form_frame, text="Description:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.desc_entry = ttk.Entry(form_frame, width=40)
        self.desc_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

      
        ttk.Label(form_frame, text="Date (YYYY-MM-DD):").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.date_entry = ttk.Entry(form_frame, width=15)
        self.date_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        self.date_entry.insert(0, datetime.today().strftime("%Y-%m-%d"))

        ttk.Label(form_frame, text="Priority:").grid(row=2, column=2, padx=5, pady=5, sticky="e")
        self.priority_combo = ttk.Combobox(
            form_frame,
            values=["High", "Medium", "Low"],
            state="readonly",
            width=10
        )
        self.priority_combo.grid(row=2, column=3, padx=5, pady=5, sticky="w")
        self.priority_combo.current(1)  # Medium por defecto

        ttk.Label(form_frame, text="Category:").grid(row=2, column=4, padx=5, pady=5, sticky="e")
        self.category_combo = ttk.Combobox(
            form_frame,
            values=["Work", "Personal", "Study", "Urgent", "Other"],
            state="readonly",
            width=12
        )
        self.category_combo.grid(row=2, column=5, padx=5, pady=5, sticky="w")
        self.category_combo.current(0)

        # Buttons
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=3, column=0, columnspan=6, pady=10)

        ttk.Button(btn_frame, text="➕ Add", command=self._add_task).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="✏️ Edit Selected", command=self._edit_task).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="🗑️ Delete Selected", command=self._delete_task).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="✅ Toggle Status", command=self._toggle_task).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="🔄 Refresh", command=self._refresh_treeview).pack(side=tk.LEFT, padx=5)

     
        self.tree.bind("<Double-1>", lambda e: self._edit_task())

    # ----------------------------------------------------------------
    # Actions: Add, Edit, Delete, Toggle
    # ----------------------------------------------------------------
    def _get_selected_id(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection required", "Please select a task from the list.")
            return None
        item = self.tree.item(selected[0])
        values = item["values"]
        if values:
            return int(values[0])
        return None

    def _add_task(self):
        title = self.title_entry.get().strip()
        description = self.desc_entry.get().strip()
        due_date = self.date_entry.get().strip()
        priority = self.priority_combo.get()
        category = self.category_combo.get()

        if not title:
            messagebox.showerror("Error", "Title is required.")
            return
        if not re.match(r"\d{4}-\d{2}-\d{2}", due_date):
            messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD.")
            return

        self.manager.add_task(title, description, due_date, priority, category)
        self._refresh_treeview()
        self.title_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, datetime.today().strftime("%Y-%m-%d"))

    def _edit_task(self):
        task_id = self._get_selected_id()
        if task_id is None:
            return

        task = self.manager.get_task_by_id(task_id)
        if not task:
            messagebox.showerror("Error", "Task does not exist.")
            return

        edit_win = tk.Toplevel(self.root)
        edit_win.title(f"Edit Task #{task_id}")
        edit_win.geometry("420x280")
        edit_win.transient(self.root)
        edit_win.grab_set()

        title_var = tk.StringVar(value=task["title"])
        desc_var = tk.StringVar(value=task.get("description", ""))
        date_var = tk.StringVar(value=task["due_date"])
        priority_var = tk.StringVar(value=task["priority"])
        category_var = tk.StringVar(value=task["category"])

        ttk.Label(edit_win, text="Title:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        ttk.Entry(edit_win, textvariable=title_var, width=30).grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(edit_win, text="Description:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        ttk.Entry(edit_win, textvariable=desc_var, width=30).grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(edit_win, text="Date (YYYY-MM-DD):").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        ttk.Entry(edit_win, textvariable=date_var, width=30).grid(row=2, column=1, padx=10, pady=10)

        ttk.Label(edit_win, text="Priority:").grid(row=3, column=0, padx=10, pady=10, sticky="e")
        prio_combo = ttk.Combobox(
            edit_win,
            values=["High", "Medium", "Low"],
            textvariable=priority_var,
            state="readonly"
        )
        prio_combo.grid(row=3, column=1, padx=10, pady=10)

        ttk.Label(edit_win, text="Category:").grid(row=4, column=0, padx=10, pady=10, sticky="e")
        cat_combo = ttk.Combobox(
            edit_win,
            values=["Work", "Personal", "Study", "Urgent", "Other"],
            textvariable=category_var,
            state="readonly"
        )
        cat_combo.grid(row=4, column=1, padx=10, pady=10)

        def save_edit():
            new_title = title_var.get().strip()
            new_desc = desc_var.get().strip()
            new_date = date_var.get().strip()
            if not new_title:
                messagebox.showerror("Error", "Title cannot be empty.")
                return
            if not re.match(r"\d{4}-\d{2}-\d{2}", new_date):
                messagebox.showerror("Error", "Invalid date format.")
                return
            self.manager.update_task(
                task_id,
                title=new_title,
                description=new_desc,
                due_date=new_date,
                priority=priority_var.get(),
                category=category_var.get()
            )
            edit_win.destroy()
            self._refresh_treeview()

        ttk.Button(edit_win, text="Save Changes", command=save_edit).grid(row=5, column=0, columnspan=2, pady=20)

    def _delete_task(self):
        task_id = self._get_selected_id()
        if task_id is None:
            return
        if messagebox.askyesno("Confirm", f"Permanently delete task #{task_id}?"):
            self.manager.delete_task(task_id)
            self._refresh_treeview()

    def _toggle_task(self):
        task_id = self._get_selected_id()
        if task_id is None:
            return
        self.manager.toggle_status(task_id)
        self._refresh_treeview()

    def _clear_search(self):
        self.search_var.set("")
        self._apply_filter()

    # ----------------------------------------------------------------
    # Filters, searching and ordering 
    # ----------------------------------------------------------------
    def _apply_filter(self):
        self._refresh_treeview()

    def _sort_by_column(self, col, reverse):
        col_map = {
            "ID": "id",
            "Title": "title",
            "Date": "due_date",
            "Priority": "priority",
            "Category": "category",
            "Status": "status"
        }
        key = col_map.get(col, "id")

        items = self.tree.get_children("")
        if not items:
            return

        data = []
        for item in items:
            values = self.tree.item(item, "values")
            task_id = int(values[0])
            task = self.manager.get_task_by_id(task_id)
            if task:
                data.append((task, item))

        priority_order = {"High": 0, "Medium": 1, "Low": 2}

        def sort_func(task_item):
            task, _ = task_item
            val = task.get(key, "")
            if key == "priority":
                return priority_order.get(val, 99)
            elif key == "due_date":
                try:
                    return datetime.strptime(val, "%Y-%m-%d")
                except:
                    return datetime.min
            else:
                return str(val).lower()

        data.sort(key=sort_func, reverse=reverse)

        for idx, (task, item) in enumerate(data):
            self.tree.move(item, "", idx)

        self.tree.heading(col, command=lambda: self._sort_by_column(col, not reverse))

    def _refresh_treeview(self):
        # Apply filters
        status_filter = self.filter_var.get()
        search_term = self.search_var.get().strip()

        status_map = {"All": None, "Pending": "Pending", "Completed": "Completed"}
        status = status_map.get(status_filter, None)

        filtered = self.manager.filter_tasks(status=status, search_term=search_term if search_term else None)

        # Update statistics 
        total, pending, completed = self.manager.get_stats()
        self.stats_label.config(text=f"📊 Total: {total} | ⏳ Pending: {pending} | ✅ Completed: {completed}")

        # Clean and reload TreeView
        for item in self.tree.get_children(""):
            self.tree.delete(item)

        for task in filtered:
            self.tree.insert("", tk.END, values=(
                task["id"],
                task["title"],
                task["due_date"],
                task["priority"],
                task["category"],
                task["status"]
            ))


# -------------------------------------------------------------------
# EXECUTION
# -------------------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = TaskApp(root)
    root.mainloop()