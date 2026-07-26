import tkinter as tk

from database import initialize_database
from db_manager import DBManager
from taskmaster_ui import TaskApp


def main() -> None:
    """
    Initializes the SQLite database and starts TaskMaster Pro
    using the real database manager.
    """
    initialize_database()

    root = tk.Tk()
    TaskApp(root, db_manager=DBManager())
    root.mainloop()


if __name__ == "__main__":
    main()