import sqlite3

DB_PATH = "data/crypto.sqlite"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS movimientos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            moneda_from TEXT NOT NULL,
            cantidad_from REAL NOT NULL,
            moneda_to TEXT NOT NULL,
            cantidad_to REAL NOT NULL
        )
    """)

    conn.commit()
    conn.close()
