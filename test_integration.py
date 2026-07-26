# test_integration.py - Integration test with Victor's real database
import tkinter as tk
from taskmaster_ui import TaskApp
from db_manager import DBManager  # Real DB adapter

if __name__ == "__main__":
    root = tk.Tk()

    # Use Victor's real database
    print("🚀 Running with DBManager (SQLite)")
    app = TaskApp(root, db_manager=DBManager())

    root.mainloop()