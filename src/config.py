"""
Daily Stock Bot 설정 모듈

환경변수, 티커 목록, 상수 등 모든 설정값을 중앙 관리합니다.
"""
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
US_TICKERS: list[str] = ["AAPL", "MSFT", "GOOGL", "TSLA", "NVDA"]

# 미국 종목 회사명 매핑
US_STOCK_NAMES: dict[str, str] = {
    "AAPL": "Apple Inc.",
    "NVDA": "NVIDIA Corp.",
    "TSLA": "Tesla Inc.",
    "META": "Meta Platforms",
    "GOOGL": "Alphabet Inc.",
    "MSFT": "Microsoft Corp.",
    "AMZN": "Amazon.com",
}

# 미국 종목 도메인 매핑 (로고 URL용)
US_STOCK_DOMAINS: dict[str, str] = {
    "AAPL": "apple.com",
    "NVDA": "nvidia.com",
    "TSLA": "tesla.com",
    "META": "meta.com",
    "GOOGL": "google.com",
    "MSFT": "microsoft.com",
    "AMZN": "amazon.com",
}

# =============================================================================
# 한국 주식 설정
# =============================================================================
KR_TICKERS: dict[str, str] = {
    "005930": "삼성전자",
    "000660": "SK하이닉스",
    "035720": "카카오",
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