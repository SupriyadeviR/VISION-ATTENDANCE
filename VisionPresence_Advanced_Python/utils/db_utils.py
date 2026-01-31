import sqlite3
from flask import g, current_app
from config import DATABASE_FILE

DATABASE_PATH = DATABASE_FILE  # Ensure this is absolute


def get_db():
    db = g.get("db")
    if db is None:
        db = sqlite3.connect(DATABASE_PATH)
        db.row_factory = sqlite3.Row
        g.db = db
    return db


def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        try:
            db.close()
        except Exception:
            pass


def init_db():
    # Always use absolute path
    db = sqlite3.connect(DATABASE_PATH)
    cursor = db.cursor()

    # Drop old tables if they exist (to reset schema)
    cursor.execute("DROP TABLE IF EXISTS attendance")
    cursor.execute("DROP TABLE IF EXISTS staff")

    # Staff table with extended info
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS staff (
            emp_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            department TEXT,
            gender TEXT,
            joining_date TEXT,
            dob TEXT,
            native TEXT,
            image_path TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Attendance table with time in/out tracking
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            emp_id INTEGER NOT NULL,
            attendance_date DATE DEFAULT CURRENT_DATE,
            time_in DATETIME,
            time_out DATETIME,
            status TEXT DEFAULT 'Present',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(emp_id) REFERENCES staff(emp_id),
            UNIQUE(emp_id, attendance_date)
        )
    """)

    db.commit()
    db.close()
    print(f"Database initialized at {DATABASE_PATH}")

