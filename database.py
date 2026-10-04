import sqlite3

def get_connection():
    conn = sqlite3.connect("money.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    conn.execute("""
       CREATE TABLE IF NOT EXISTS transactions (
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           amount REAL NOT NULL,
           type TEXT NOT NULL,
           category TEXT NOT NULL,
           date TEXT NOT NULL,
           note TEXT
       )
    """)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database ready")