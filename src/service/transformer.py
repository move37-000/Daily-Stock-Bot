from typing import Any

from src.config import (
    US_STOCK_NAMES,
    US_STOCK_DOMAINS,
    LOGO_API_TOKEN,
    LOGO_API_URL,
    TOSS_LOGO_URL,
    NEWS_LIMIT,
)


def transform_us_data(
        us_results: list[dict[str, Any]],
        us_index: dict[str, Any]
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """
    미국 크롤러 데이터 → 템플릿 데이터로 변환

    Args:
        us_results: 크롤러에서 수집한 미국 주식 데이터
        us_index: 미국 지수 데이터

    Returns:
        (시장 지수 데이터, 종목별 데이터) 튜플
    """
    us_stocks = [_transform_us_stock(stock) for stock in us_results]

    us_market = {
        "sp500": us_index.get("sp500", _default_index()),
        "nasdaq": us_index.get("nasdaq", _default_index()),
    }

    return us_market, us_stocks


def transform_kr_data(
        kr_results: list[dict[str, Any]],
        kr_index: dict[str, Any]
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """
    한국 크롤러 데이터 → 템플릿 데이터로 변환

    Args:
        kr_results: 크롤러에서 수집한 한국 주식 데이터
        kr_index: 한국 지수 데이터

    Returns:
        (시장 지수 데이터, 종목별 데이터) 튜플
    """
    kr_stocks = [_transform_kr_stock(stock) for stock in kr_results]

    kr_market = {
        "kospi": kr_index.get("kospi", _default_index()),
        "kosdaq": kr_index.get("kosdaq", _default_index()),
    }

    return kr_market, kr_stocks


# =============================================================================
# Private Helper Functions
# =============================================================================

def _transform_us_stock(stock: dict[str, Any]) -> dict[str, Any]:
    """미국 개별 종목 데이터 변환"""
    history = _sort_and_format_history(stock.get('history', []))

    return {
        "symbol": stock['symbol'],
        "name": US_STOCK_NAMES.get(stock['symbol'], stock['symbol']),
        "price": f"{stock['close']:,.2f}",
        "change": stock['change'],
        "change_pct": f"{abs(stock['change_pct']):.2f}",
        "logo": _get_us_logo_url(stock['symbol']),
        "history": history,
        "news": stock.get('news', [])[:NEWS_LIMIT]
    }


def _transform_kr_stock(stock: dict[str, Any]) -> dict[str, Any]:
    """한국 개별 종목 데이터 변환"""
    history = _sort_and_format_history(stock.get('history', []))

    return {
        "symbol": stock['name'],
        "name": stock['code'],
        "price": f"{int(stock['close']):,}",
        "change": stock['change'],
        "change_pct": f"{abs(stock['change_pct']):.2f}",
        "logo": _get_kr_logo_url(stock['code']),
        "history": history,
        "news": stock.get('news', [])[:NEWS_LIMIT]
    }


def _sort_and_format_history(history: list[dict]) -> list[dict[str, Any]]:
    """히스토리 데이터 정렬 및 스파크라인용 포맷 변환"""
    if not history:
        return []

    sorted_history = sorted(history, key=lambda h: h['date'])
    return [{"date": h['date'], "price": h['close']} for h in sorted_history]


def _get_us_logo_url(symbol: str) -> str:
    """미국 주식 로고 URL 생성"""
    domain = US_STOCK_DOMAINS.get(symbol, f"{symbol.lower()}.com")
    return LOGO_API_URL.format(domain=domain, token=LOGO_API_TOKEN)


def _get_kr_logo_url(code: str) -> str:
    """한국 주식 로고 URL 생성"""
    return TOSS_LOGO_URL.format(code=code)


def _default_index() -> dict[str, Any]:
    """지수 기본값"""
    return {"price": "-", "change": 0, "change_pct": "-"}
