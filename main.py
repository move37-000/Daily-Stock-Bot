from config import US_TICKERS, KR_TICKERS, SLACK_WEBHOOK_URL
from crawler import fetch_us_stocks, fetch_kr_stocks
from report import generate_report, save_report
from database import init_db, save_stock_price
from notifier import send_slack_message


def save_us_stocks(results):
    """미국 주식 DB 저장"""
    for stock in results:
        saved = save_stock_price(
            symbol=stock['symbol'],
            name=stock['symbol'],
            market='US',
            close_price=stock['close'],
            change=stock['change'],
            change_pct=stock['change_pct']
        )
        status = "저장" if saved else "스킵(이미 존재)"
        print(f"  {status}: {stock['symbol']}")


def save_kr_stocks(results):
    """한국 주식 DB 저장"""
    for stock in results:
        saved = save_stock_price(
            symbol=stock['code'],
            name=stock['name'],
            market='KR',
            close_price=stock['close'],
            change=stock['change'],
            change_pct=stock['change_pct']
        )
        status = "저장" if saved else "스킵(이미 존재)"
        print(f"  {status}: {stock['name']}")


def main():
    init_db()

    # 1. 데이터 수집
    print("데이터 수집 중...")
    us_results = fetch_us_stocks(US_TICKERS)
    kr_results = fetch_kr_stocks(KR_TICKERS)

    # 2. DB 저장
    print("DB 저장 중...")
    save_us_stocks(us_results)
    save_kr_stocks(kr_results)

    # 3. 리포트 생성
    print("리포트 생성 중...")
    content = generate_report(us_results, kr_results)
    filename = save_report(content)
    print(f"리포트 저장 완료: {filename}")

    # 4. Slack 알림
    print("Slack 전송 중...")
    if send_slack_message(SLACK_WEBHOOK_URL, us_results, kr_results):
        print("Slack 전송 완료!")
    else:
        print("Slack 전송 실패")


if __name__ == "__main__":
    main()