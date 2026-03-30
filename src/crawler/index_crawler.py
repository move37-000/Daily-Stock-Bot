import logging
from typing import Any

import yfinance as yf

from src.config import US_INDEX_SYMBOLS, KR_INDEX_SYMBOLS, USD_KRW_SYMBOL, HISTORY_DAYS

logger = logging.getLogger(__name__)

# 데이터 조회 실패 시 반환할 기본값
_DEFAULT_INDEX_DATA: dict[str, Any] = {
    "price": "-",
    "change": 0,
    "change_pct": "-",
    "history": []
}


def fetch_us_index() -> dict[str, dict[str, Any]]:
    """미국 시장 지수 (S&P 500, NASDAQ) 조회"""
    return _fetch_multiple_indices(US_INDEX_SYMBOLS, "미국")


def fetch_kr_index() -> dict[str, dict[str, Any]]:
    """한국 시장 지수 (KOSPI, KOSDAQ) 조회"""
    return _fetch_multiple_indices(KR_INDEX_SYMBOLS, "한국")


def fetch_usd_krw() -> dict[str, Any]:
    """USD/KRW 환율 조회"""
    return _fetch_single_index(USD_KRW_SYMBOL, "USD/KRW")


def _fetch_multiple_indices(
    symbols: dict[str, str],
    market_name: str
) -> dict[str, dict[str, Any]]:
    """
    여러 지수를 한 번에 조회

    Args:
        symbols: 지수명-심볼 딕셔너리 (예: {"sp500": "^GSPC"})
        market_name: 로깅용 시장명

    Returns:
        지수명별 데이터 딕셔너리
    """
    result = {}

    for name, symbol in symbols.items():
        try:
            data = _fetch_single_index(symbol, f"{market_name} {name}")

            print(f"data: {data}")

            result[name] = data
        except Exception as e:
            logger.error(f"{market_name} 지수 조회 실패 ({name}): {e}")
            result[name] = _DEFAULT_INDEX_DATA.copy()

    return result


def _fetch_single_index(symbol: str, name: str) -> dict[str, Any]:
    """
    단일 지수/환율 조회

    Args:
        symbol: yfinance 심볼 (예: "^GSPC", "USDKRW=X")
        name: 로깅용 이름

    Returns:
        지수 데이터 (price, change, change_pct, history)
    """
    try:
        ticker = yf.Ticker(symbol)
        history = ticker.history(period=f"{HISTORY_DAYS}d")

        if len(history) < 2:
            logger.warning(f"{name} 데이터 부족: {len(history)}일치")
            return _DEFAULT_INDEX_DATA.copy()

        close, change, change_pct = _calculate_change(history)
        daily_data = _parse_history(history)

        return {
            "price": f"{close:,.2f}",
            "change": change,
            "change_pct": f"{abs(change_pct):.2f}",
            "history": daily_data
        }

    except Exception as e:
        logger.error(f"{name} 조회 실패: {e}")
        return _DEFAULT_INDEX_DATA.copy()


def _calculate_change(history) -> tuple[float, float, float]:
    """전일 대비 변동 계산"""
    latest = history.iloc[-1]
    prev = history.iloc[-2]
    close = latest['Close']
    change = close - prev['Close']
    change_pct = (change / prev['Close']) * 100
    return close, change, change_pct


def _parse_history(history) -> list[dict[str, Any]]:
    """히스토리 데이터 파싱 (스파크라인용)"""
    daily_data = []
    for date, row in history.iterrows():
        daily_data.append({
            'date': date.strftime("%Y-%m-%d"),
            'price': row['Close']
        })
    return daily_data
