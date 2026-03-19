from datetime import datetime
from .connection import get_connection

def save_stock_price(symbol, name, market, close_price, change, change_pct):
    """주가 데이터 저장"""
    conn = get_connection()
    cursor = conn.cursor()

    today = datetime.now().strftime("%Y-%m-%d")

    # 오늘 이미 저장된 데이터가 있으면 스킵
    cursor.execute("""
        SELECT id FROM stock_prices 
        WHERE symbol = ? AND collected_at = ?
    """, (symbol, today))

    if cursor.fetchone():
        conn.close()
        return False  # 이미 존재

    cursor.execute("""
        INSERT INTO stock_prices (symbol, name, market, close_price, change, change_pct, collected_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (symbol, name, market, close_price, change, change_pct, today))

    conn.commit()
    conn.close()
    return True  # 저장 성공


def get_stock_history(symbol, days=30):
    """종목 히스토리 조회"""
    conn = get_connection()
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