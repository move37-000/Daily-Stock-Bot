# 📈 Daily Stock Bot

매일 아침 미국/한국 주식 시황을 수집하고, AI 분석이 포함된 HTML 리포트를 생성하여 Slack/Discord로 알림을 보내는 자동화 봇입니다.

## ✨ 주요 기능

- **미국/한국 주식 데이터 수집** (yfinance, pykrx)
- **시장 지수** (S&P500, NASDAQ, KOSPI, KOSDAQ)
- **환율 정보** (USD/KRW)
- **종목별 뉴스 크롤링** (Yahoo Finance, 네이버 금융)
- **AI 시황 분석** (Gemini API)
- **HTML 리포트 생성** (다크/라이트 모드, 인터랙티브 차트)
- **Slack/Discord 알림**
- **GitHub Actions 자동화** (매일 오전 7시 KST)

## 📊 리포트 미리보기

- 5일간 주가 차트 (LightweightCharts)
- 종목 클릭 시 관련 뉴스 표시
- AI 기반 시황 브리핑

## 🛠️ 기술 스택

| 구분 | 기술 |
|------|------|
| Language | Python 3.11+ |
| 미국 주식 | yfinance |
| 한국 주식 | pykrx |
| AI 분석 | Google Gemini API |
| 템플릿 | Jinja2 |
| 차트 | LightweightCharts |
| DB | SQLite |
| 자동화 | GitHub Actions |
| 알림 | Slack, Discord Webhook |

## 📁 프로젝트 구조

```
daily-stock-bot/
├── .github/workflows/
│   └── daily-report.yml    # GitHub Actions 워크플로우
├── src/
│   ├── config.py           # 설정값 중앙 관리
│   ├── main.py             # 오케스트레이션
│   ├── crawler/            # 데이터 수집
│   │   ├── us_stock.py
│   │   ├── kr_stock.py
│   │   └── index_crawler.py
│   ├── repository/         # DB 저장
│   │   └── stock_repository.py
│   ├── service/            # 비즈니스 로직
│   │   ├── stock_service.py
│   │   ├── transformer.py
│   │   ├── report_service.py
│   │   ├── notification_service.py
│   │   └── ai_service.py
│   └── utils/
│       └── date_utils.py
├── templates/
│   └── report.html         # Jinja2 HTML 템플릿
├── data/                   # SQLite DB
├── reports/                # 생성된 리포트
└── tests/                  # 테스트 코드
```

## ⚙️ 설정

### 환경변수

| 변수 | 설명 | 필수 |
|------|------|------|
| `SLACK_WEBHOOK_URL` | Slack 웹훅 URL | O |
| `DISCORD_WEBHOOK_URL` | Discord 웹훅 URL | X |
| `GEMINI_API_KEY` | Google Gemini API Key | X |

### 종목 설정 (config.py)

```python
# 한국 주식
KR_TICKERS = {
    "471760": "TIGER AI반도체핵심공정",
}

# 미국 주식
US_TICKERS = ["NVDA", "QQQ", "SCHD"]
```

## 🚀 실행 방법

### 로컬 실행

```bash
# 의존성 설치
pip install -r requirements.txt

# 환경변수 설정
cp .env.example .env
# .env 파일 편집

# 실행
python -m src.main
```

### GitHub Actions

1. Repository Settings → Secrets에 환경변수 등록
2. 매일 오전 7시(KST) 자동 실행
3. 수동 실행: Actions → Run workflow

## 📝 리포트 타이밍

| 시장 | 장 마감 시간 | 리포트 시점 | 데이터 신선도 |
|------|-------------|------------|--------------|
| 🇺🇸 미국 | 오전 6시 (KST) | 오전 7시 | ✅ 1시간 전 |
| 🇰🇷 한국 | 오후 3:30 (KST) | 다음날 오전 7시 | ⚠️ 전일 마감 |

→ 한국장 개장(9시) 전에 미국장 영향 분석 + 오늘 전망 확인용

## 🧪 테스트

```bash
pytest
```

## 📄 라이선스

MIT License

---