import yfinance as yf

# 애플 주식 데이터
ticker = yf.Ticker("AAPL")

# 최근 5일 주가
history = ticker.history(period = "5d")

print("=== AAPL 최근 5일 주가 ===")
print(history)