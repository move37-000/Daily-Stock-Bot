"""
리포트 생성 서비스 모듈

Jinja2 템플릿을 사용하여 HTML 리포트를 생성합니다.
"""
from datetime import datetime
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader


class ReportService:
    """HTML 리포트 생성 서비스"""

    def __init__(self) -> None:
        self._project_root = Path(__file__).parent.parent.parent
        self._env = Environment(
            loader=FileSystemLoader(self._project_root / "templates"),
            autoescape=True
        )

    def generate_report(
        self,
        us_market: dict[str, Any],
        kr_market: dict[str, Any],
        us_stocks: list[dict[str, Any]],
        kr_stocks: list[dict[str, Any]],
        us_market_news: list[dict[str, Any]],
        kr_market_news: list[dict[str, Any]],
        usd_krw: dict[str, Any] | None = None,
        ai_comment: str | None = None
    ) -> str:
        """
        HTML 리포트 생성

        Args:
            us_market: 미국 시장 지수 데이터
            kr_market: 한국 시장 지수 데이터
            us_stocks: 미국 종목별 데이터
            kr_stocks: 한국 종목별 데이터
            us_market_news: 미국 시장 뉴스
            kr_market_news: 한국 시장 뉴스
            usd_krw: USD/KRW 환율 데이터
            ai_comment: AI 생성 코멘트

        Returns:
            생성된 리포트 파일 경로
        """
        template = self._env.get_template("report.html")
        now = datetime.now()

        html_content = template.render(
            report_date=now.strftime("%Y-%m-%d"),
            generated_at=now.strftime("%Y-%m-%d %H:%M KST"),
            us_market=us_market,
            kr_market=kr_market,
            us_stocks=us_stocks,
            kr_stocks=kr_stocks,
            us_market_news=us_market_news,
            kr_market_news=kr_market_news,
            usd_krw=usd_krw,
            ai_comment=ai_comment
        )

        output_path = self._save_report(html_content, now)
        return output_path

    def _save_report(self, content: str, timestamp: datetime) -> str:
        """리포트 파일 저장"""
        reports_dir = self._project_root / "reports"
        reports_dir.mkdir(exist_ok=True)

        filename = f"report_{timestamp.strftime('%Y%m%d_%H%M%S')}.html"
        file_path = reports_dir / filename

        file_path.write_text(content, encoding="utf-8")
        return str(file_path)
