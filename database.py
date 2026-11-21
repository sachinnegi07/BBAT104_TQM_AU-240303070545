
import sqlite3
from pathlib import Path

# Project and database location
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "data" / "hostel.db"


def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DB_PATH)
    connection.execute("PRAGMA foreign_keys = ON")
    connection.row_factory = sqlite3.Row

    return connection


def initialize_database():
    with get_connection() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_code TEXT NOT NULL UNIQUE,
                full_name TEXT NOT NULL,
                phone TEXT,
                course TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS rooms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                room_number TEXT NOT NULL UNIQUE,
                capacity INTEGER NOT NULL CHECK(capacity > 0),
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS allocations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                room_id INTEGER NOT NULL,
                allocation_date TEXT DEFAULT CURRENT_DATE,
                vacated_at TEXT,
                FOREIGN KEY (student_id)
                    REFERENCES students(id)
                    ON DELETE RESTRICT,
                FOREIGN KEY (room_id)
                    REFERENCES rooms(id)
                    ON DELETE RESTRICT
            );

            CREATE UNIQUE INDEX IF NOT EXISTS
                idx_active_student_allocation
            ON allocations(student_id)
            WHERE vacated_at IS NULL;

            CREATE TABLE IF NOT EXISTS complaints (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                status TEXT NOT NULL DEFAULT 'Pending'
                    CHECK(status IN (
                        'Pending', 'In Progress', 'Resolved'
                    )),
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id)
                    REFERENCES students(id)
                    ON DELETE RESTRICT
            );
        """)

        tables = conn.execute("""
            SELECT name FROM sqlite_master
            WHERE type = 'table'
              AND name NOT LIKE 'sqlite_%'
            ORDER BY name
        """).fetchall()

        print("Database initialized successfully!")
        print("Database:", DB_PATH)
        print("Tables:")
        for table in tables:
            print("-", table["name"])


if __name__ == "__main__":
    initialize_database()
