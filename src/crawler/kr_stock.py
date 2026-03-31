import logging
from datetime import datetime, timedelta
from typing import Any

import requests
from pykrx import stock as krx

from src.config import NEWS_LIMIT, KR_MARKET_NEWS_CODES, NAVER_STOCK_NEWS_API, HISTORY_DAYS
from src.utils import format_kr_news_time

logger = logging.getLogger(__name__)

_HEADERS = {"User-Agent": "Mozilla/5.0"}


def fetch_kr_stocks(tickers: dict[str, str]) -> list[dict[str, Any]]:
    """
    한국 주식 데이터 수집 (5일치)

    Args:
        tickers: 종목코드-종목명 딕셔너리 (예: {"005930": "삼성전자"})

    Returns:
        종목별 주가 데이터 리스트
    """
    today = datetime.now()
    end_date = today - timedelta(days=1)
    start_date = today - timedelta(days=HISTORY_DAYS * 2)  # 여유있게 2배

    start_str = start_date.strftime("%Y%m%d")
    end_str = end_date.strftime("%Y%m%d")

    results = []

    for code, name in tickers.items():
        try:
            history = krx.get_market_ohlcv_by_date(
                fromdate=start_str,
                todate=end_str,
                ticker=code
            )

            if history.empty:
                logger.warning(f"한국 주식 데이터 없음: {name}")
                continue

            # 최근 N일치만
            history = history.tail(HISTORY_DAYS)

            daily_data = _parse_kr_history(history)
            close, change, change_pct = _calculate_kr_change(history)
            news = fetch_kr_news(code)

            results.append({
                'code': code,
                'name': name,
                'close': close,
                'change': change,
                'change_pct': change_pct,
                'news': news,
                'history': daily_data
            })

        except Exception as e:
            logger.error(f"한국 주식 조회 실패 ({name}): {e}")
            continue

    return results


def fetch_kr_news(code: str, limit: int = NEWS_LIMIT) -> list[dict[str, Any]]:
    """
    네이버 금융 API에서 종목 뉴스 가져오기

    Args:
        code: 종목 코드
        limit: 뉴스 개수

    Returns:
        뉴스 리스트
    """
    url = NAVER_STOCK_NEWS_API.format(code=code, limit=limit)

    try:
        response = requests.get(url, headers=_HEADERS, timeout=10)
        data = response.json()

        news = []
        for item in data:
            article = item.get('items', [{}])[0]
            if article:
                news.append(_parse_kr_news_article(article))

        return news
    except Exception as e:
        logger.warning(f"한국 종목 뉴스 조회 실패 ({code}): {e}")
        return []


def fetch_kr_market_news() -> list[dict[str, Any]]:
    """한국 시장 뉴스 (대형주에서 1개씩, 중복 제거)"""
    news = []
    seen_titles = set()  # 중복 체크용

    for code in KR_MARKET_NEWS_CODES:
        try:
            url = NAVER_STOCK_NEWS_API.format(code=code, limit=1)
            response = requests.get(url, headers=_HEADERS, timeout=10)
            data = response.json()

            if data and len(data) > 0:
                article = data[0].get('items', [{}])[0]
                if article:
                    title = article.get('title', '')

                    # 중복 체크
                    if title in seen_titles:
                        continue
                    seen_titles.add(title)

                    parsed = _parse_kr_news_article(article)
                    parsed['publisher'] = article.get('officeName', '네이버 금융')
                    news.append(parsed)

        except Exception as e:
            logger.warning(f"한국 시장 뉴스 조회 실패 ({code}): {e}")
            continue

    return news


def _parse_kr_history(history) -> list[dict[str, Any]]:
    """pykrx 히스토리 데이터 파싱"""
    daily_data = []
    for date, row in history.iterrows():
        daily_data.append({
            'date': date.strftime("%Y-%m-%d"),
            'close': row['종가'],
            'open': row['시가'],
            'high': row['고가'],
            'low': row['저가'],
            'volume': row['거래량']
        })
    return daily_data


def _calculate_kr_change(history) -> tuple[float, float, float]:
    """전일 대비 변동 계산"""
    latest = history.iloc[-1]
    prev = history.iloc[-2]
    close = latest['종가']
    change = close - prev['종가']
    change_pct = (change / prev['종가']) * 100
    return close, change, change_pct


def _parse_kr_news_article(article: dict) -> dict[str, Any]:
    """네이버 뉴스 기사 파싱"""
    office_id = article.get('officeId', '')
    article_id = article.get('articleId', '')
    datetime_str = article.get('datetime', '')

    return {
        'title': article.get('title', ''),
        'link': f"https://n.news.naver.com/mnews/article/{office_id}/{article_id}",
        'time': format_kr_news_time(datetime_str)
    }
