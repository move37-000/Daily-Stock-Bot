import logging

from src.config import US_TICKERS, KR_TICKERS, SLACK_WEBHOOK_URL, DISCORD_WEBHOOK_URL, REPORT_URL
from src.repository import init_db, save_stock_price
from src.service import ReportService, send_slack_message, send_discord_message
from src.crawler import (
    fetch_us_stocks,
    fetch_kr_stocks,
    fetch_us_index,
    fetch_kr_index,
    fetch_usd_krw,
    fetch_us_market_news,
    fetch_kr_market_news,
)

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

US_DOMAINS = {
    'AAPL': 'apple.com',
    'NVDA': 'nvidia.com',
    'TSLA': 'tesla.com',
    'META': 'meta.com',
    'GOOGL': 'google.com',
    'MSFT': 'microsoft.com',
    'AMZN': 'amazon.com',
}


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
                    logger.debug(f"저장: {stock['symbol']} ({day['date']})")


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
                    logger.debug(f"저장: {stock['name']} ({day['date']})")


def transform_us_data(us_results, us_index):
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
    for stock in us_results:
        history = []
        if stock.get('history'):
            sorted_history = sorted(stock['history'], key=lambda h: h['date'])
            history = [{"date": h['date'], "price": h['close']} for h in sorted_history]

        us_stocks.append({
            "symbol": stock['symbol'],
            "name": names.get(stock['symbol'], stock['symbol']),
            "price": f"{stock['close']:,.2f}",
            "change": stock['change'],
            "change_pct": f"{abs(stock['change_pct']):.2f}",
            "logo": f"https://img.logo.dev/{US_DOMAINS.get(stock['symbol'], stock['symbol'].lower() + '.com')}?token=pk_X-1ZO13GSgeOoUrIuJ6GMQ&size=40&format=png",
            "history": history,
            "news": stock.get('news', [])[:3]
        })

    us_market = {
        "sp500": us_index.get("sp500", {"price": "-", "change": 0, "change_pct": "-"}),
        "nasdaq": us_index.get("nasdaq", {"price": "-", "change": 0, "change_pct": "-"}),
    }

    return us_market, us_stocks


def transform_kr_data(kr_results, kr_index):
    """한국 크롤러 데이터 → 템플릿 데이터로 변환"""
    kr_stocks = []
    for stock in kr_results:
        history = []
        if stock.get('history'):
            sorted_history = sorted(stock['history'], key=lambda h: h['date'])
            history = [{"date": h['date'], "price": h['close']} for h in sorted_history]

        kr_stocks.append({
            "symbol": stock['name'],
            "name": stock['code'],
            "price": f"{int(stock['close']):,}",
            "change": stock['change'],
            "change_pct": f"{abs(stock['change_pct']):.2f}",
            "logo": f"https://thumb.tossinvest.com/image/resized/40x0/https%3A%2F%2Fstatic.toss.im%2Fpng-icons%2Fsecurities%2Ficn-sec-fill-{stock['code']}.png",
            "history": history,
            "news": stock.get('news', [])[:3]
        })

    kr_market = {
        "kospi": kr_index.get("kospi", {"price": "-", "change": 0, "change_pct": "-"}),
        "kosdaq": kr_index.get("kosdaq", {"price": "-", "change": 0, "change_pct": "-"}),
    }

    return kr_market, kr_stocks


def main():
    try:
        init_db()
    except Exception as e:
        logger.error(f"DB 초기화 실패: {e}")
        return

    # 1. 데이터 수집
    logger.info("데이터 수집 중...")
    us_results = fetch_us_stocks(US_TICKERS)
    kr_results = fetch_kr_stocks(KR_TICKERS)

    # 2. 지수 데이터 수집
    logger.info("지수 데이터 수집 중...")
    us_index = fetch_us_index()
    kr_index = fetch_kr_index()

    # 3. 시장 뉴스 수집
    logger.info("시장 뉴스 수집 중...")
    us_market_news = fetch_us_market_news()
    kr_market_news = fetch_kr_market_news()

    usd_krw = fetch_usd_krw()

    # 4. DB 저장
    logger.info("DB 저장 중...")
    save_us_stocks(us_results)
    save_kr_stocks(kr_results)

    # 5. 데이터 변환
    logger.info("데이터 변환 중...")
    us_market, us_stocks = transform_us_data(us_results, us_index)
    kr_market, kr_stocks = transform_kr_data(kr_results, kr_index)

    # 6. HTML 리포트 생성
    logger.info("리포트 생성 중...")
    try:
        service = ReportService()
        filename = service.generate_report(
            us_market=us_market,
            kr_market=kr_market,
            us_stocks=us_stocks,
            kr_stocks=kr_stocks,
            us_market_news=us_market_news,
            kr_market_news=kr_market_news,
            usd_krw=usd_krw,
            ai_comment=None
        )
        logger.info(f"리포트 저장 완료: {filename}")
    except Exception as e:
        logger.error(f"리포트 생성 실패: {e}")

    # 7. Slack 알림
    logger.info("Slack 전송 중...")
    try:
        if send_slack_message(
                SLACK_WEBHOOK_URL,
                us_results,
                kr_results,
                us_market=us_market,
                kr_market=kr_market,
                usd_krw=usd_krw,
                report_url=REPORT_URL
        ):
            logger.info("Slack 전송 완료!")
        else:
            logger.warning("Slack 전송 실패")
    except Exception as e:
        logger.error(f"Slack 전송 실패: {e}")

    # 8. Discord 알림
    if DISCORD_WEBHOOK_URL:
        logger.info("Discord 전송 중...")
        try:
            if send_discord_message(
                    DISCORD_WEBHOOK_URL,
                    us_results,
                    kr_results,
                    us_market=us_market,
                    kr_market=kr_market,
                    usd_krw=usd_krw,
                    report_url=REPORT_URL
            ):
                logger.info("Discord 전송 완료!")
            else:
                logger.warning("Discord 전송 실패")
        except Exception as e:
            logger.error(f"Discord 전송 실패: {e}")


if __name__ == "__main__":
    main()