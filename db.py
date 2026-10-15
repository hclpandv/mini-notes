
import sqlite3
from pathlib import Path

# Always locate the database beside this file, regardless of
# which directory we run Python from.
DB_PATH = Path(__file__).parent / "notes.db"


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                body TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)


def list_notes():
    """Return all notes, newest first."""
    with get_connection() as connection:
        rows = connection.execute("""
            SELECT id, title, body, created_at
            FROM notes
            ORDER BY id DESC
        """).fetchall()

        return [dict(row) for row in rows]


def create_note(title, body):
    """Save a note and return its new ID."""
    with get_connection() as connection:
        cursor = connection.execute(
            "INSERT INTO notes (title, body) VALUES (?, ?)",
            (title, body),
        )
        return cursor.lastrowid


def delete_note(note_id):
    """Delete a note. Return True if it existed."""
    with get_connection() as connection:
        cursor = connection.execute(
            "DELETE FROM notes WHERE id = ?",
            (note_id,),
        )
        return cursor.rowcount > 0


if __name__ == "__main__":
    init_db()
    print(f"Database ready: {DB_PATH}")
