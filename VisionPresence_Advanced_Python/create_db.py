import sqlite3
from config import DATABASE_FILE

def create_database():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    # ================= STAFF TABLE =================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS staff (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        emp_id TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT NOT NULL,
        dob TEXT NOT NULL,
        department TEXT NOT NULL,
        image_path TEXT NOT NULL,
        registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # ================= ATTENDANCE TABLE =================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        emp_id TEXT NOT NULL,
        name TEXT NOT NULL,
        date TEXT NOT NULL,
        time_in TEXT,
        time_out TEXT
    )
    """)

    conn.commit()
    conn.close()

    print("✅ Database created successfully!")

if __name__ == "__main__":
    create_database()
