import sqlite3
import os

def get_connection():
    """SQLite 연결 반환"""
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect("data/stock.db")
    return conn

def init_db():
    """테이블 생성"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stock_prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL,
            name TEXT NOT NULL,
            market TEXT NOT NULL,
            close_price REAL NOT NULL,
            change REAL NOT NULL,
            change_pct REAL NOT NULL,
            collected_at TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()