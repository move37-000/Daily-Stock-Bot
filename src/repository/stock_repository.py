import sqlite3
import os
from datetime import datetime


def _get_connection():
    """SQLite 연결 반환"""
    os.makedirs("data", exist_ok=True)
    return sqlite3.connect("data/stock.db")


def init_db():
    """테이블 생성"""
    conn = _get_connection()
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


def save_stock_price(symbol, name, market, close_price, change, change_pct, collected_at=None):
    """주가 데이터 저장"""
    conn = _get_connection()
    cursor = conn.cursor()

    if collected_at is None:
        collected_at = datetime.now().strftime("%Y-%m-%d")

    cursor.execute("""
        SELECT id FROM stock_prices 
        WHERE symbol = ? AND collected_at = ?
    """, (symbol, collected_at))

    if cursor.fetchone():
        conn.close()
        return False

    cursor.execute("""
        INSERT INTO stock_prices (symbol, name, market, close_price, change, change_pct, collected_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (symbol, name, market, close_price, change, change_pct, collected_at))

    conn.commit()
    conn.close()
    return True


def get_stock_history(symbol, days=30):
    """종목 히스토리 조회"""
    conn = _get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT collected_at, close_price, change, change_pct
        FROM stock_prices
        WHERE symbol = ?
        ORDER BY collected_at DESC
        LIMIT ?
    """, (symbol, days))

    rows = cursor.fetchall()
    conn.close()

    return [{
        'date': row[0],
        'close': row[1],
        'change': row[2],
        'change_pct': row[3]
    } for row in rows]