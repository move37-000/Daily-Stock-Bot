import yfinance as yf

def fetch_us_stocks(tickers):
    """미국 주식 데이터 수집"""
    results = []

    for symbol in tickers:
        ticker = yf.Ticker(symbol)
        history = ticker.history(period="5d")

        if history.empty:
            continue

        latest = history.iloc[-1]
        prev = history.iloc[-2]

        close = latest['Close']
        change = close - prev['Close']
        change_pct = (change / prev['Close']) * 100

        # 뉴스 가져오기 (최신 3개)
        news = []
        for item in ticker.news[:3]:
            news.append({
                'title': item.get('title', ''),
                'link': item.get('link', ''),
                'publisher': item.get('publisher', '')
            })

        results.append({
            'symbol': symbol,
            'close': close,
            'change': change,
            'change_pct': change_pct,
        })

    return results