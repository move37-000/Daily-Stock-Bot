import logging
from datetime import datetime, timedelta

import requests
from pykrx import stock as krx

logger = logging.getLogger(__name__)


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
                datetime_str = article.get('datetime', '')

                # 시간 포맷 변환
                time_str = ''
                if datetime_str and len(datetime_str) >= 12:
                    try:
                        month = int(datetime_str[4:6])
                        day = int(datetime_str[6:8])
                        hour = int(datetime_str[8:10])
                        minute = int(datetime_str[10:12])
                        if hour < 12:
                            ampm = '오전'
                            display_hour = hour if hour != 0 else 12
                        else:
                            ampm = '오후'
                            display_hour = hour - 12 if hour != 12 else 12
                        time_str = f"{month}월 {day}일 {ampm} {display_hour}시 {minute}분"
                    except ValueError as e:
                        logger.debug(f"뉴스 시간 파싱 실패 ({code}): {e}")

                news.append({
                    'title': article.get('title', ''),
                    'link': f"https://n.news.naver.com/mnews/article/{office_id}/{article_id}",
                    'time': time_str
                })

        return news
    except Exception as e:
        logger.warning(f"한국 종목 뉴스 조회 실패 ({code}): {e}")
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
                logger.warning(f"한국 주식 데이터 없음: {name}")
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
                'news': news,
                'history': daily_data
            })

        except Exception as e:
            logger.error(f"한국 주식 조회 실패 ({name}): {e}")
            continue

    return results


def fetch_kr_market_news():
    """한국 시장 뉴스 (대형주 3개에서 1개씩)"""
    codes = ['005930', '000660', '005380']  # 삼성전자, SK하이닉스, 현대차
    headers = {"User-Agent": "Mozilla/5.0"}

    news = []

    for code in codes:
        try:
            url = f"https://api.stock.naver.com/news/stock/{code}?pageSize=1"
            response = requests.get(url, headers=headers)
            data = response.json()

            if data and len(data) > 0:
                article = data[0].get('items', [{}])[0]
                if article:
                    datetime_str = article.get('datetime', '')

                    time_str = ''
                    if datetime_str and len(datetime_str) >= 12:
                        try:
                            month = int(datetime_str[4:6])
                            day = int(datetime_str[6:8])
                            hour = int(datetime_str[8:10])
                            minute = int(datetime_str[10:12])
                            if hour < 12:
                                ampm = '오전'
                                display_hour = hour if hour != 0 else 12
                            else:
                                ampm = '오후'
                                display_hour = hour - 12 if hour != 12 else 12
                            time_str = f"{month}월 {day}일 {ampm} {display_hour}시 {minute}분"
                        except ValueError as e:
                            logger.debug(f"시장 뉴스 시간 파싱 실패 ({code}): {e}")

                    news.append({
                        'title': article.get('title', ''),
                        'publisher': article.get('officeName', '네이버 금융'),
                        'time': time_str,
                        'link': f"https://n.news.naver.com/mnews/article/{article.get('officeId', '')}/{article.get('articleId', '')}"
                    })
        except Exception as e:
            logger.warning(f"한국 시장 뉴스 조회 실패 ({code}): {e}")
            continue

    return news