import logging
from typing import Any

import yfinance as yf

from src.config import NEWS_LIMIT, US_INDEX_SYMBOLS
from src.utils import format_us_news_time

logger = logging.getLogger(__name__)


def fetch_us_stocks(tickers: list[str]) -> list[dict[str, Any]]:
    """
    미국 주식 데이터 수집 (5일치)

    Args:
        tickers: 종목 심볼 리스트 (예: ["AAPL", "MSFT"])

    Returns:
        종목별 주가 데이터 리스트
    """
    results = []

    for symbol in tickers:
        try:
            ticker = yf.Ticker(symbol)
            history = ticker.history(period="5d")

            if history.empty:
                logger.warning(f"미국 주식 데이터 없음: {symbol}")
                continue

            daily_data = _parse_history(history)
            close, change, change_pct = _calculate_change(history)
            news = _fetch_ticker_news(ticker, symbol)

            results.append({
                'symbol': symbol,
                'close': close,
                'change': change,
                'change_pct': change_pct,
                'news': news,
                'history': daily_data
            })

        except Exception as e:
            logger.error(f"미국 주식 조회 실패 ({symbol}): {e}")
            continue

    return results


def fetch_us_market_news() -> list[dict[str, Any]]:
    """미국 시장 전체 뉴스 (S&P 500 기준)"""
    try:
        ticker = yf.Ticker(US_INDEX_SYMBOLS["sp500"])
        return _fetch_ticker_news(ticker, "market")
    except Exception as e:
        logger.error(f"미국 시장 뉴스 조회 실패: {e}")
        return []


def _parse_history(history) -> list[dict[str, Any]]:
    """yfinance 히스토리 데이터 파싱"""
    daily_data = []
    for date, row in history.iterrows():
        daily_data.append({
            'date': date.strftime("%Y-%m-%d"),
            'close': row['Close'],
            'open': row['Open'],
            'high': row['High'],
            'low': row['Low'],
            'volume': row['Volume']
        })
    return daily_data


def _calculate_change(history) -> tuple[float, float, float]:
    """전일 대비 변동 계산"""
    latest = history.iloc[-1]
    prev = history.iloc[-2]
    close = latest['Close']
    change = close - prev['Close']
    change_pct = (change / prev['Close']) * 100
    return close, change, change_pct


def _fetch_ticker_news(ticker, symbol: str) -> list[dict[str, Any]]:
    """종목/시장 뉴스 조회"""
    news = []
    try:
        for item in ticker.news[:NEWS_LIMIT]:
            content = item.get('content', {})
            news.append({
                'title': content.get('title', ''),
                'link': _get_news_link(content),
                'publisher': content.get('provider', {}).get('displayName', ''),
                'time': format_us_news_time(content.get('pubDate', ''))
            })
    except Exception as e:
        logger.warning(f"뉴스 조회 실패 ({symbol}): {e}")
    return news


def _get_news_link(content: dict) -> str:
    """뉴스 링크 추출 (clickThroughUrl 우선, canonicalUrl 폴백)"""
    return (
        content.get('clickThroughUrl', {}).get('url', '') or
        content.get('canonicalUrl', {}).get('url', '')
    )