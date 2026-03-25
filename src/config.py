import os
from dotenv import load_dotenv

load_dotenv()

# =============================================================================
# 환경변수
# =============================================================================
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

# =============================================================================
# GitHub Pages 설정
# =============================================================================
GITHUB_USERNAME = "move37-000"
REPO_NAME = "Daily-Stock-Bot"
REPORT_URL = f"https://{GITHUB_USERNAME}.github.io/{REPO_NAME}/"

# =============================================================================
# 데이터 수집 설정
# =============================================================================
HISTORY_DAYS = 5  # 히스토리 조회 일수
NEWS_LIMIT = 3    # 뉴스 조회 개수

# =============================================================================
# 미국 주식 설정
# =============================================================================
# US_TICKERS: list[str] = ["AAPL", "MSFT", "GOOGL", "TSLA", "NVDA"]
US_TICKERS = ["NVDA", "QQQ", "SCHD"]

# 미국 종목 회사명 매핑
# US_STOCK_NAMES: dict[str, str] = {
#     "AAPL": "Apple Inc.",
#     "MSFT": "Microsoft Corp.",
#     "GOOGL": "Alphabet Inc.",
#     "TSLA": "Tesla Inc.",
#     "NVDA": "NVIDIA Corp.",
# }
US_STOCK_NAMES = {
    "NVDA": "NVIDIA Corporation",
    "QQQ": "Invesco QQQ Trust",
    "SCHD": "Schwab US Dividend Equity ETF",
}

# 미국 종목 도메인 매핑 (로고 URL용)
# US_STOCK_DOMAINS: dict[str, str] = {
#     "AAPL": "apple.com",
#     "MSFT": "microsoft.com",
#     "GOOGL": "google.com",
#     "TSLA": "tesla.com",
#     "NVDA": "nvidia.com",
# }
US_STOCK_DOMAINS = {
    "NVDA": "nvidia.com",
    "QQQ": "invesco.com",
    "SCHD": "schwab.com",
}

# =============================================================================
# 한국 주식 설정
# =============================================================================
# KR_TICKERS: dict[str, str] = {
#     "005930": "삼성전자",
#     "000660": "SK하이닉스",
#     "035720": "카카오",
# }
KR_TICKERS = {
    "471760": "TIGER AI반도체핵심공정",
}

# 한국 시장 뉴스 조회용 대형주 코드
KR_MARKET_NEWS_CODES: list[str] = ["005930", "000660", "005380"]  # 삼성전자, SK하이닉스, 현대차

# =============================================================================
# 지수 심볼 매핑
# =============================================================================
US_INDEX_SYMBOLS: dict[str, str] = {
    "sp500": "^GSPC",
    "nasdaq": "^IXIC",
}

KR_INDEX_SYMBOLS: dict[str, str] = {
    "kospi": "^KS11",
    "kosdaq": "^KQ11",
}

USD_KRW_SYMBOL = "USDKRW=X"

# =============================================================================
# 외부 API 설정
# =============================================================================
LOGO_API_TOKEN = "pk_X-1ZO13GSgeOoUrIuJ6GMQ"
LOGO_API_URL = "https://img.logo.dev/{domain}?token={token}&size=40&format=png"
TOSS_LOGO_URL = "https://thumb.tossinvest.com/image/resized/40x0/https%3A%2F%2Fstatic.toss.im%2Fpng-icons%2Fsecurities%2Ficn-sec-fill-{code}.png"
NAVER_STOCK_NEWS_API = "https://api.stock.naver.com/news/stock/{code}?pageSize={limit}"