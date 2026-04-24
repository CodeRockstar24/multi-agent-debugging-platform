import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DB_PATH = BASE_DIR / "code_debugger.db"


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS issues (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            issue_type TEXT NOT NULL DEFAULT 'bug',
            project_name TEXT NOT NULL,
            error_summary TEXT NOT NULL,
            problem_details TEXT,
            code_snippet TEXT,
            status TEXT DEFAULT 'new'
        )
        """
    )

    cursor.execute("PRAGMA table_info(issues)")
    columns = [row["name"] for row in cursor.fetchall()]

    if "issue_type" not in columns:
        cursor.execute(
            "ALTER TABLE issues ADD COLUMN issue_type TEXT NOT NULL DEFAULT 'bug'"
        )

    connection.commit()
    connection.close()
