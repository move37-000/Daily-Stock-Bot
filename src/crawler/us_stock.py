import yfinance as yf

def fetch_us_stocks(tickers):
    """미국 주식 데이터 수집 (5일치)"""
    results = []

    for symbol in tickers:
        try:
            ticker = yf.Ticker(symbol)
            history = ticker.history(period="5d")

            if history.empty:
                print(f"  [경고] {symbol}: 데이터 없음")
                continue

            # 전체 5일치 데이터 저장
            daily_data = []
            for date, row in history.iterrows():
                daily_data.append({
                    'date': date.strftime("%Y-%m-%d"),
                    'close': row['Close'],
                    'open': row['Open'],
                    'high': row['High'],
                    'low': row['Low'],
                    'volume': row['Volume']
                })

            # 최신 데이터 (어제)
            latest = history.iloc[-1]
            prev = history.iloc[-2]
            close = latest['Close']
            change = close - prev['Close']
            change_pct = (change / prev['Close']) * 100

            # 뉴스 가져오기 (최신 3개)
            news = []
            try:
                for item in ticker.news[:3]:
                    content = item.get('content', {})
                    news.append({
                        'title': content.get('title', ''),
                        'link': content.get('previewUrl', ''),
                        'publisher': content.get('provider', {}).get('displayName', '')
                    })
            except Exception:
                pass  # 뉴스 실패해도 주가 데이터는 유지

            results.append({
                'symbol': symbol,
                'close': close,
                'change': change,
                'change_pct': change_pct,
                'news': news,
                'history': daily_data  # 5일치 히스토리 추가
            })

        except Exception as e:
            print(f"  [에러] {symbol}: {e}")
            continue

    return results