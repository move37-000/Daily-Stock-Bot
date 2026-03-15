import yfinance as yf
from pykrx import stock as krx
from datetime import datetime, timedelta

# 날짜 계산 (오늘 기준 5일 전 ~ 어제)
today = datetime.now()
end_date = today - timedelta(days=1)
start_date = today - timedelta(days=7)

# pykrx용 날짜 포맷 (YYYYMMDD)
start_str = start_date.strftime("%Y%m%d")
end_str = end_date.strftime("%Y%m%d")

# === 미국 주식 ===
us_tickers = ["AAPL", "MSFT", "GOOGL", "TSLA", "NVDA"]

print("========== 미국 주식 ==========\n")
for symbol in us_tickers:
    ticker = yf.Ticker(symbol)
    history = ticker.history(period="5d")

    if history.empty:
        print(f"{symbol}: 데이터 없음\n")
        continue

    latest = history.iloc[-1]  # 가장 최근 데이터
    prev = history.iloc[-2]  # 그 전날 데이터

    close = latest['Close']
    change = close - prev['Close']
    change_pct = (change / prev['Close']) * 100

    print(f"{symbol}")
    print(f"  종가: ${close:.2f}")
    print(f"  변동: {change:+.2f} ({change_pct:+.2f}%)")
    print()

# === 한국 주식 ===
kr_tickers = {
    "005930": "삼성전자",
    "000660": "SK하이닉스",
    "035720": "카카오"
}

print("========== 한국 주식 ==========\n")
for code, name in kr_tickers.items():
    history = krx.get_market_ohlcv_by_date(
        fromdate=start_str,
        todate=end_str,
        ticker=code
    )

    if history.empty:
        print(f"{name}({code}): 데이터 없음\n")
        continue

    latest = history.iloc[-1]
    prev = history.iloc[-2]

    close = latest['종가']
    change = close - prev['종가']
    change_pct = (change / prev['종가']) * 100

    print(f"{name}({code})")
    print(f"  종가: {close:,}원")
    print(f"  변동: {change:+,} ({change_pct:+.2f}%)")
    print()