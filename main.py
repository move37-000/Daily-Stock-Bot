from config import US_TICKERS, KR_TICKERS
from crawler import fetch_us_stocks, fetch_kr_stocks

def main():
    # 미국 주식
    print("========== 미국 주식 ==========\n")
    us_results = fetch_us_stocks(US_TICKERS)

    for stock in us_results:
        print(f"{stock['symbol']}")
        print(f"  종가: ${stock['close']:.2f}")
        print(f"  변동: ${stock['change']:+.2f} ({stock['change_pct']:+.2f}%)")
        print()

    # 한국 주식
    print("========== 한국 주식 ==========\n")
    kr_results = fetch_kr_stocks(KR_TICKERS)

    for stock in kr_results:
        print(f"{stock['name']}({stock['code']})")
        print(f"  종가: {stock['close']:,}원")
        print(f"  변동: {stock['change']:+,}원 ({stock['change_pct']:+.2f}%)")
        print()


if __name__ == "__main__":
    main()