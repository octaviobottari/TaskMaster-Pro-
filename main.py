import tkinter as tk
from tkinter import messagebox

from database import (
    check_database_health,
    initialize_database,
)
from db_manager import DBManager
from taskmaster_ui import TaskApp


def main() -> None:
    """
    Main entry point for TaskMaster Pro.
    """
    try:
        initialize_database()

        if not check_database_health():
            raise RuntimeError(
                "The database integrity check failed."
            )

        root = tk.Tk()

        TaskApp(
            root,
            db_manager=DBManager(),
        )

        root.mainloop()

    except Exception as error:
        try:
            root = tk.Tk()
            root.withdraw()

            messagebox.showerror(
                "TaskMaster Pro",
                f"Application startup failed:\n\n{error}",
            )

            root.destroy()

        except Exception:
            print(
                f"Application startup failed: {error}"
            )


if __name__ == "__main__":
    main()