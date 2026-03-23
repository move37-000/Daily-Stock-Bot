from src.service.report_service import ReportService


def main():
    # Mock 데이터 준비
    us_market = {
        "sp500": {"price": "5,864.01", "change": 0.30, "change_pct": "0.30"},
        "nasdaq": {"price": "19,630.20", "change": -0.23, "change_pct": "0.23"},
        "chart_base64": None  # 차트는 나중에
    }

    kr_market = {
        "kospi": {"price": "2,481.12", "change": -0.52, "change_pct": "0.52"},
        "kosdaq": {"price": "718.05", "change": 0.35, "change_pct": "0.35"},
        "chart_base64": None
    }

    us_stocks = [
        {"symbol": "AAPL", "name": "Apple Inc.", "price": "228.44", "change": 1.24, "change_pct": "1.24",
         "color": "blue"},
        {"symbol": "NVDA", "name": "NVIDIA Corp.", "price": "134.30", "change": 2.87, "change_pct": "2.87",
         "color": "green"},
        {"symbol": "TSLA", "name": "Tesla Inc.", "price": "403.84", "change": -1.52, "change_pct": "1.52",
         "color": "red"},
    ]

    kr_stocks = [
        {"symbol": "삼성전자", "name": "005930", "price": "71,800", "change": -0.83, "change_pct": "0.83", "color": "blue"},
        {"symbol": "SK하이닉스", "name": "000660", "price": "178,500", "change": 2.15, "change_pct": "2.15",
         "color": "purple"},
        {"symbol": "카카오", "name": "035720", "price": "42,300", "change": 1.08, "change_pct": "1.08", "color": "orange"},
    ]

    news_list = [
        {"source": "Reuters", "time": "2시간 전", "headline": "Fed, 금리 동결 시사... 인플레이션 우려 지속"},
        {"source": "Bloomberg", "time": "3시간 전", "headline": "NVIDIA, AI 칩 수요 급증으로 실적 전망 상향"},
        {"source": "한국경제", "time": "5시간 전", "headline": "외국인 코스피 3거래일 연속 순매도"},
    ]

    # 리포트 생성
    service = ReportService()
    output_path = service.generate_report(
        us_market=us_market,
        kr_market=kr_market,
        us_stocks=us_stocks,
        kr_stocks=kr_stocks,
        news_list=news_list,
        ai_comment="테스트용 AI 코멘트입니다. NVIDIA가 강세를 보이고 있습니다."
    )

    print(f"✅ 리포트 생성 완료: {output_path}")


if __name__ == "__main__":
    main()