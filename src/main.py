from src.config import US_TICKERS, KR_TICKERS, SLACK_WEBHOOK_URL
from src.crawler import fetch_us_stocks, fetch_kr_stocks
from src.service import ReportService, send_slack_message, generate_chart_base64
from src.repository import init_db, save_stock_price, get_stock_history

# 아이콘 색상 로테이션
COLORS = ["blue", "green", "purple", "orange", "red"]


def save_us_stocks(results):
    """미국 주식 DB 저장 (5일치)"""
    for stock in results:
        if 'history' in stock:
            for i, day in enumerate(stock['history']):
                if i == 0:
                    change = 0
                    change_pct = 0
                else:
                    prev_close = stock['history'][i - 1]['close']
                    change = day['close'] - prev_close
                    change_pct = (change / prev_close) * 100

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
                    print(f"  저장: {stock['symbol']} ({day['date']})")


def save_kr_stocks(results):
    """한국 주식 DB 저장 (5일치)"""
    for stock in results:
        if 'history' in stock:
            for i, day in enumerate(stock['history']):
                if i == 0:
                    change = 0
                    change_pct = 0
                else:
                    prev_close = stock['history'][i - 1]['close']
                    change = day['close'] - prev_close
                    change_pct = (change / prev_close) * 100

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
                    print(f"  저장: {stock['name']} ({day['date']})")


def transform_us_data(us_results):
    """미국 크롤러 데이터 → 템플릿 데이터로 변환"""
    names = {
        'AAPL': 'Apple Inc.',
        'NVDA': 'NVIDIA Corp.',
        'TSLA': 'Tesla Inc.',
        'META': 'Meta Platforms',
        'GOOGL': 'Alphabet Inc.',
        'MSFT': 'Microsoft Corp.',
        'AMZN': 'Amazon.com',
    }

    us_stocks = []
    for i, stock in enumerate(us_results):
        us_stocks.append({
            "symbol": stock['symbol'],
            "name": names.get(stock['symbol'], stock['symbol']),
            "price": f"{stock['close']:,.2f}",
            "change": stock['change'],
            "change_pct": f"{abs(stock['change_pct']):.2f}",
            "color": COLORS[i % len(COLORS)]
        })

    # 첫 번째 종목의 히스토리로 차트 생성
    chart_base64 = None
    if us_results and us_results[0].get('history'):
        chart_base64 = generate_chart_base64('US', us_results[0]['history'])

    us_market = {
        "sp500": {"price": "-", "change": 0, "change_pct": "-"},
        "nasdaq": {"price": "-", "change": 0, "change_pct": "-"},
        "chart_base64": chart_base64
    }

    return us_market, us_stocks


def transform_kr_data(kr_results):
    """한국 크롤러 데이터 → 템플릿 데이터로 변환"""
    kr_stocks = []
    for i, stock in enumerate(kr_results):
        kr_stocks.append({
            "symbol": stock['name'],
            "name": stock['code'],
            "price": f"{stock['close']:,}",
            "change": stock['change'],
            "change_pct": f"{abs(stock['change_pct']):.2f}",
            "color": COLORS[i % len(COLORS)]
        })

    # 첫 번째 종목의 히스토리로 차트 생성
    chart_base64 = None
    if kr_results and kr_results[0].get('history'):
        chart_base64 = generate_chart_base64('KR', kr_results[0]['history'])

    kr_market = {
        "kospi": {"price": "-", "change": 0, "change_pct": "-"},
        "kosdaq": {"price": "-", "change": 0, "change_pct": "-"},
        "chart_base64": chart_base64
    }

    return kr_market, kr_stocks


def transform_news(us_results, kr_results):
    """뉴스 데이터 통합"""
    news_list = []

    # 미국 뉴스
    for stock in us_results:
        for news in stock.get('news', [])[:1]:  # 종목당 1개씩만
            if news.get('title'):
                news_list.append({
                    "source": news.get('publisher', 'US News'),
                    "time": "",
                    "headline": news['title']
                })

    # 한국 뉴스
    for stock in kr_results:
        for news in stock.get('news', [])[:1]:
            if news.get('title'):
                news_list.append({
                    "source": "네이버 금융",
                    "time": "",
                    "headline": news['title']
                })

    return news_list[:6]  # 최대 6개


def main():
    try:
        init_db()
    except Exception as e:
        print(f"[에러] DB 초기화 실패: {e}")
        return

    # 1. 데이터 수집
    print("데이터 수집 중...")
    us_results = fetch_us_stocks(US_TICKERS)
    kr_results = fetch_kr_stocks(KR_TICKERS)

    # 2. DB 저장
    print("DB 저장 중...")
    save_us_stocks(us_results)
    save_kr_stocks(kr_results)

    # 4. 데이터 변환 (크롤러 → 템플릿)
    print("데이터 변환 중...")
    us_market, us_stocks = transform_us_data(us_results)
    kr_market, kr_stocks = transform_kr_data(kr_results)
    news_list = transform_news(us_results, kr_results)

    # 5. HTML 리포트 생성
    print("리포트 생성 중...")
    try:
        service = ReportService()
        filename = service.generate_report(
            us_market=us_market,
            kr_market=kr_market,
            us_stocks=us_stocks,
            kr_stocks=kr_stocks,
            news_list=news_list,
            ai_comment=None  # 나중에 Claude API 연동
        )
        print(f"리포트 저장 완료: {filename}")
    except Exception as e:
        print(f"[에러] 리포트 생성 실패: {e}")

    # 6. Slack 알림
    print("Slack 전송 중...")
    try:
        if send_slack_message(SLACK_WEBHOOK_URL, us_results, kr_results):
            print("Slack 전송 완료!")
        else:
            print("[경고] Slack 전송 실패")
    except Exception as e:
        print(f"[에러] Slack 전송 실패: {e}")


if __name__ == "__main__":
    main()