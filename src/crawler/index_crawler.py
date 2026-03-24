import logging

import yfinance as yf

logger = logging.getLogger(__name__)


def fetch_us_index():
    """
    미국 시장 지수 (S&P 500, NASDAQ) 조회
    """
    result = {}

    tickers = {
        "sp500": "^GSPC",
        "nasdaq": "^IXIC"
    }

    for name, symbol in tickers.items():
        try:
            ticker = yf.Ticker(symbol)
            history = ticker.history(period="5d")

            if len(history) < 2:
                result[name] = {"price": "-", "change": 0, "change_pct": "-", "history": []}
                continue

            latest = history.iloc[-1]
            prev = history.iloc[-2]

            close = latest['Close']
            change = close - prev['Close']
            change_pct = (change / prev['Close']) * 100

            # 5일치 히스토리 추가
            daily_data = []
            for date, row in history.iterrows():
                daily_data.append({
                    'date': date.strftime("%Y-%m-%d"),
                    'price': row['Close']
                })

            result[name] = {
                "price": f"{close:,.2f}",
                "change": change,
                "change_pct": f"{abs(change_pct):.2f}",
                "history": daily_data
            }

        except Exception as e:
            logger.error(f"미국 지수 조회 실패 ({name}): {e}")
            result[name] = {"price": "-", "change": 0, "change_pct": "-", "history": []}

    return result


def fetch_kr_index():
    """
    한국 시장 지수 (KOSPI, KOSDAQ) 조회
    Yahoo Finance 사용
    """
    result = {}

    tickers = {
        "kospi": "^KS11",
        "kosdaq": "^KQ11"
    }

    for name, symbol in tickers.items():
        try:
            ticker = yf.Ticker(symbol)
            history = ticker.history(period="5d")

            if len(history) < 2:
                result[name] = {"price": "-", "change": 0, "change_pct": "-", "history": []}
                continue

            latest = history.iloc[-1]
            prev = history.iloc[-2]

            close = latest['Close']
            change = close - prev['Close']
            change_pct = (change / prev['Close']) * 100

            # 5일치 히스토리 추가
            daily_data = []
            for date, row in history.iterrows():
                daily_data.append({
                    'date': date.strftime("%Y-%m-%d"),
                    'price': row['Close']
                })

            result[name] = {
                "price": f"{close:,.2f}",
                "change": change,
                "change_pct": f"{abs(change_pct):.2f}",
                "history": daily_data
            }

        except Exception as e:
            logger.error(f"한국 지수 조회 실패 ({name}): {e}")
            result[name] = {"price": "-", "change": 0, "change_pct": "-", "history": []}

    return result

def fetch_usd_krw():
    """
    USD/KRW 환율 조회
    """
    try:
        ticker = yf.Ticker("USDKRW=X")
        history = ticker.history(period="5d")

        if len(history) < 2:
            return {"price": "-", "change": 0, "change_pct": "-", "history": []}

        latest = history.iloc[-1]
        prev = history.iloc[-2]

        close = latest['Close']
        change = close - prev['Close']
        change_pct = (change / prev['Close']) * 100

        # 5일치 히스토리
        daily_data = []
        for date, row in history.iterrows():
            daily_data.append({
                'date': date.strftime("%Y-%m-%d"),
                'price': row['Close']
            })

        return {
            "price": f"{close:,.2f}",
            "change": change,
            "change_pct": f"{abs(change_pct):.2f}",
            "history": daily_data
        }

    except Exception as e:
        logger.error(f"USD/KRW 환율 조회 실패: {e}")
        return {"price": "-", "change": 0, "change_pct": "-", "history": []}