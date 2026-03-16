from config import US_TICKERS, KR_TICKERS
from crawler import fetch_us_stocks, fetch_kr_stocks
from report import generate_report, save_report


def main():
    print("데이터 수집 중...")

    us_results = fetch_us_stocks(US_TICKERS)
    kr_results = fetch_kr_stocks(KR_TICKERS)

    print("리포트 생성 중...")

    content = generate_report(us_results, kr_results)
    filename = save_report(content)

    print(f"리포트 저장 완료: {filename}")
    print()
    print(content)


if __name__ == "__main__":
    main()