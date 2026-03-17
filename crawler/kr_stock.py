from pykrx import stock as krx
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup


def fetch_kr_news(code, limit=3):
    """네이버 금융 API에서 종목 뉴스 가져오기"""
    url = f"https://api.stock.naver.com/news/stock/{code}?pageSize={limit}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers)
        data = response.json()

        news = []
        for item in data:
            article = item.get('items', [{}])[0]
            if article:
                office_id = article.get('officeId', '')
                article_id = article.get('articleId', '')
                news.append({
                    'title': article.get('title', ''),
                    'link': f"https://n.news.naver.com/mnews/article/{office_id}/{article_id}"
                })

        return news
    except Exception:
        return []

def fetch_kr_stocks(tickers):
    """한국 주식 데이터 수집"""
    today = datetime.now()
    end_date = today - timedelta(days=1)
    start_date = today - timedelta(days=7)

    start_str = start_date.strftime("%Y%m%d")
    end_str = end_date.strftime("%Y%m%d")

    results = []

    for code, name in tickers.items():
        history = krx.get_market_ohlcv_by_date(
            fromdate=start_str,
            todate=end_str,
            ticker=code
        )

        if history.empty:
            continue

        latest = history.iloc[-1]
        prev = history.iloc[-2]

        close = latest['종가']
        change = close - prev['종가']
        change_pct = (change / prev['종가']) * 100

        # 뉴스 가져오기
        news = fetch_kr_news(code)

        results.append({
            'code': code,
            'name': name,
            'close': close,
            'change': change,
            'change_pct': change_pct,
            'news': news
        })

    return results