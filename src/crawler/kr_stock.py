from pykrx import stock as krx
from datetime import datetime, timedelta
import requests


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
    """한국 주식 데이터 수집 (5일치)"""
    today = datetime.now()
    end_date = today - timedelta(days=1)
    start_date = today - timedelta(days=10)  # 넉넉하게 10일 전부터

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
                print(f"  [경고] {name}: 데이터 없음")
                continue

            # 최근 5일치만
            history = history.tail(5)

            # 전체 5일치 데이터 저장
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

            # 최신 데이터
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

        except Exception as e:
            print(f"  [에러] {name}: {e}")
            continue

    return results