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
us_ticker = ["AAPL", "MSFT", "GOOGL", "TSLA", "NVDA"]

print("============= 미국 주식 =============")
for symbol in us_ticker:
        ticker = yf.Ticker(symbol)
        history = ticker.history(period="5d")

        if history.empty:
            print(f"{symbol}: 데이터 없음")
            continue

        latest = history.iloc[-1]   # 가장 최근 데이터
        prev = history.iloc[-2]     # 그 전날 데이터

        close = latest['Close']
        change = close - prev['Close']
        change_pct = (change / prev['Close']) * 100

        print(f"{symbol}")
        print(f"    종가: ${close:.2f}")
        print(f"    변동: {change:+.2f} ({change_pct:+.2f}%)")