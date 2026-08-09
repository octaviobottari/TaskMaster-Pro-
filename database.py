from pathlib import Path
import sqlite3


BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "taskmaster.db"


def get_connection() -> sqlite3.Connection:
    """
    Creates and returns a connection to the SQLite database.

    SQLite rows are configured so columns can be accessed by name.
    """
    connection = sqlite3.connect(
        DATABASE_PATH,
        timeout=10,
    )
    connection.row_factory = sqlite3.Row

    # Recommended SQLite setting for local desktop applications.
    connection.execute("PRAGMA foreign_keys = ON;")

    return connection


def initialize_database() -> None:
    """
    Creates the tasks table and supporting indexes if they do not exist.
    """
    try:
        with get_connection() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT,
                    category TEXT NOT NULL,
                    priority TEXT NOT NULL,
                    due_date TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'Pending',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """
            )

            connection.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_tasks_category
                ON tasks(category);
                """
            )

            connection.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_tasks_priority
                ON tasks(priority);
                """
            )

            connection.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_tasks_due_date
                ON tasks(due_date);
                """
            )

            connection.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_tasks_status
                ON tasks(status);
                """
            )

            connection.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_tasks_title
                ON tasks(title);
                """
            )

            connection.commit()

    except sqlite3.Error as error:
        raise RuntimeError(
            f"Unable to initialize the database: {error}"
        ) from error


def check_database_health() -> bool:
    """
    Performs a simple SQLite integrity check.

    Returns True when the database passes the integrity check.
    """
    try:
        with get_connection() as connection:
            result = connection.execute(
                "PRAGMA integrity_check;"
            ).fetchone()

        return (
            result is not None
            and result[0] == "ok"
        )

    except sqlite3.Error:
        return False


if __name__ == "__main__":
    initialize_database()

    print(
        f"Database initialized successfully at: {DATABASE_PATH}"
    )

    print(
        "Database integrity:",
        "OK" if check_database_health() else "FAILED",
    )