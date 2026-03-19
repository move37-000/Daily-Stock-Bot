from config import US_TICKERS, KR_TICKERS, DISCORD_WEBHOOK_URL
from crawler import fetch_us_stocks, fetch_kr_stocks
from report import generate_report, save_report
from database import init_db, save_stock_price, get_stock_history
from notifier import send_discord_message


def main():
    # DB 초기화 (테이블 없으면 생성)
    init_db()

    print("데이터 수집 중...")

    us_results = fetch_us_stocks(US_TICKERS)
    kr_results = fetch_kr_stocks(KR_TICKERS)

    # DB 저장
    print("DB 저장 중...")

    for stock in us_results:
        saved = save_stock_price(
            symbol=stock['symbol'],
            name=stock['symbol'],  # 미국은 심볼이 곧 이름
            market='US',
            close_price=stock['close'],
            change=stock['change'],
            change_pct=stock['change_pct']
        )
        if saved:
            print(f"  저장: {stock['symbol']}")
        else:
            print(f"  스킵(이미 존재): {stock['symbol']}")

    for stock in kr_results:
        saved = save_stock_price(
            symbol=stock['code'],
            name=stock['name'],
            market='KR',
            close_price=stock['close'],
            change=stock['change'],
            change_pct=stock['change_pct']
        )
        if saved:
            print(f"  저장: {stock['name']}")
        else:
            print(f"  스킵(이미 존재): {stock['name']}")

    content = generate_report(us_results, kr_results)
    filename = save_report(content)

    print(f"리포트 저장 완료: {filename}")

    # Discord 알림
    print("Discord 전송 중...")

    if send_discord_message(DISCORD_WEBHOOK_URL, us_results, kr_results):
        print("Discord 전송 완료!") 
    else:
        print("Discord 전송 실패")


if __name__ == "__main__":
    main()