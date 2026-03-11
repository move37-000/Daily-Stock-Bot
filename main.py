import yfinance as yf

us_ticker = ["AAPL", "MSFT", "GOOGL", "TSLA", "NVDA"]

for symbol in us_ticker:
    ticker = yf.Ticker(symbol)
    history = ticker.history(period = "5d")

    print(f"=== {symbol} 최근 5일 ===")
    print(history)
    print()