import os
from dotenv import load_dotenv

load_dotenv()

# 환경변수
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

# 미국 주식 관심 종목
US_TICKERS = ["AAPL", "MSFT", "GOOGL", "TSLA", "NVDA"]

# 한국 주식 관심 종목 (종목코드: 종목명)
KR_TICKERS = {
    "005930": "삼성전자",
    "000660": "SK하이닉스",
    "035720": "카카오"
}