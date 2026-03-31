import logging
from typing import Any

from src.repository import save_stock_price

logger = logging.getLogger(__name__)


def save_stocks(
        us_results: list[dict[str, Any]],
        kr_results: list[dict[str, Any]]
) -> None:
    """
    미국/한국 주식 데이터 일괄 저장

    Args:
        us_results: 미국 주식 크롤링 결과
        kr_results: 한국 주식 크롤링 결과
    """
    _save_us_stocks(us_results)
    _save_kr_stocks(kr_results)


def _save_us_stocks(results: list[dict[str, Any]]) -> None:
    """미국 주식 DB 저장 (히스토리 포함)"""
    for stock in results:
        if 'history' not in stock:
            continue

        for i, day in enumerate(stock['history']):
            change, change_pct = _calculate_daily_change(stock['history'], i)

            saved = save_stock_price(
                symbol=stock['symbol'],
                name=stock['symbol'],
                market='US',
                close_price=day['close'],
                change=change,
                change_pct=change_pct,
                collected_at=day['date']
            )
            if saved:
                logger.debug(f"저장: {stock['symbol']} ({day['date']})")


def _save_kr_stocks(results: list[dict[str, Any]]) -> None:
    """한국 주식 DB 저장 (히스토리 포함)"""
    for stock in results:
        if 'history' not in stock:
            continue

        for i, day in enumerate(stock['history']):
            change, change_pct = _calculate_daily_change(stock['history'], i)

            saved = save_stock_price(
                symbol=stock['code'],
                name=stock['name'],
                market='KR',
                close_price=day['close'],
                change=change,
                change_pct=change_pct,
                collected_at=day['date']
            )
            if saved:
                logger.debug(f"저장: {stock['name']} ({day['date']})")


def _calculate_daily_change(history: list[dict], index: int) -> tuple[float, float]:
    """
    일별 변동 계산

    Args:
        history: 히스토리 데이터
        index: 현재 인덱스

    Returns:
        (변동금액, 변동률) 튜플
    """
    if index == 0:
        return 0, 0

    prev_close = history[index - 1]['close']
    current_close = history[index]['close']
    change = current_close - prev_close
    change_pct = (change / prev_close) * 100

    return change, change_pct
