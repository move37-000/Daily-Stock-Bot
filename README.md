# 📈 Daily Stock Bot (v1.0 - Deprecated)

> `yfinance` 및 `pykrx` 라이브러리 문제로 인해 **현재 정상적으로 동작하지 않음.**
> 
> 해당 프로젝트의 구조적 문제와 데이터 수집 방식을 개선하여 **새로운 repository 에서 v2.0 리팩토링 및 개발을 진행 중**
> 
> 👉 **새로운 리팩토링 프로젝트**: `[새로운 레포지토리 URL 주소 입력]`

- **라이브러리 리스크**: KRX(한국거래소)가 비인증 크롤링을 차단하면서 pykrx로 한국 지수를 가져올 수 없게 되었고, yfinance로 우회하니 오전 7시 반에 전일 한국 지수가 누락되는 문제 발생
- **구조적 한계**: 빈약한 아키텍쳐와 도메인 모델링, 테스트를 전혀 고려하지 않은 설계, 에러 전략 미존재 등
- **개선 방향**: 라이브러리 리스크 해소, 헥사고날 방식의 아키텍쳐 수립 

## 📁 (구) 프로젝트 구조 및 기능 (참고용)

<details>
<summary>기존 v1.0 상세 내용 펼치기</summary>

### 주요 기능
- **미국/한국 주식 데이터 수집** (yfinance, pykrx)
- **시장 지수** (S&P500, NASDAQ, KOSPI, KOSDAQ)
- **환율 정보** (USD/KRW)
- **종목별 뉴스 크롤링** (Yahoo Finance, 네이버 금융)
- **AI 시황 분석** (Gemini API)
- **HTML 리포트 생성** (다크/라이트 모드, 인터랙티브 차트)
- **Slack/Discord 알림**
- **GitHub Actions 자동화** (매일 오전 7시 KST)

### 기술 스택
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

### 프로젝트 구조
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


</details>