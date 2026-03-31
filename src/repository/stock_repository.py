import os
import sqlite3
from datetime import datetime
from typing import Any
from pathlib import Path

# 데이터베이스 경로 (프로젝트 루트 기준)
_PROJECT_ROOT = Path(__file__).parent.parent.parent
_DB_DIR = _PROJECT_ROOT / "data"
_DB_PATH = _DB_DIR / "stock.db"


def _get_connection() -> sqlite3.Connection:
    """SQLite 연결 반환"""
    os.makedirs(_DB_DIR, exist_ok=True)
    return sqlite3.connect(_DB_PATH)


def init_db() -> None:
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


def save_stock_price(
    symbol: str,
    name: str,
    market: str,
    close_price: float,
    change: float,
    change_pct: float,
    collected_at: str | None = None
) -> bool:
    """
    주가 데이터 저장

    Args:
        symbol: 종목 심볼/코드
        name: 종목명
        market: 시장 (US/KR)
        close_price: 종가
        change: 전일 대비 변동
        change_pct: 전일 대비 변동률
        collected_at: 수집 일자 (기본값: 오늘)

    Returns:
        저장 성공 여부 (이미 존재하면 False)
    """
    conn = _get_connection()
    cursor = conn.cursor()

    if collected_at is None:
        collected_at = datetime.now().strftime("%Y-%m-%d")

    # 중복 체크
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


def get_stock_history(symbol: str, days: int = 30) -> list[dict[str, Any]]:
    """
    종목 히스토리 조회

    Args:
        symbol: 종목 심볼/코드
        days: 조회 일수 (기본값: 30)

    Returns:
        날짜별 주가 데이터 리스트
    """
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
