from pykrx import stock as krx
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup


def fetch_kr_news(code, limit=3):
    """네이버 금융에서 종목 뉴스 크롤링"""
    url = f"https://finance.naver.com/item/news_news.naver?code={code}"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    news = []
    rows = soup.select("table.type5 tbody tr.tit")

    for row in rows[:limit]:
        a_tag = row.select_one("a")
        if a_tag:
            title = a_tag.get_text(strip=True)
            link = "https://finance.naver.com" + a_tag["href"]
            news.append({
                "title": title,
                "link": link
            })

    return news

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