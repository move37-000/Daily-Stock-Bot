from pykrx import stock as krx
from datetime import datetime, timedelta

def fetch_kr_stocks(tickers):
    """한국 주식 데이터 수집"""
    today = datetime.now()
    end_date = today - timedelta(days=1)
    start_date = today - timedelta(days=7)

    start_str = start_date.strftime("%Y%m%d")
    end_str = end_date.strftime("%Y%m%d")

    results = []

    for code, name in tickers.items():
        history = krx.get_market_ohlcv_by_date(
            fromdate=start_str,
            todate=end_str,
            ticker=code
        )

        if history.empty:
            continue

        latest = history.iloc[-1]
        prev = history.iloc[-2]

        close = latest['종가']
        change = close - prev['종가']
        change_pct = (change / prev['종가']) * 100

        results.append({
            'code': code,
            'name': name,
            'close': close,
            'change': change,
            'change_pct': change_pct
        })

    return results