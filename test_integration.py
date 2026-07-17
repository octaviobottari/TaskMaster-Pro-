# test_integration.py 
import tkinter as tk

# whenever db is done:
# from db_manager import DBManager
from taskmaster_ui import TaskApp
from mock_manager import MockTaskManager

if __name__ == "__main__":
    root = tk.Tk()

    # Option 1: execute Mock 
    print("Executing Mock")
    app = TaskApp(root)  

    # Option 2: When db_manager:
    # print(" Executing with DBManager (SQLite)")
    # app = TaskApp(root, db_manager=DBManager())

    root.mainloop()