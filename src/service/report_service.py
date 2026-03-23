from jinja2 import Environment, FileSystemLoader
from pathlib import Path
from datetime import datetime


class ReportService:
    """HTML 리포트 생성 서비스"""

    def __init__(self):
        # 프로젝트 루트 경로 계산
        self._project_root = Path(__file__).parent.parent.parent

        # Jinja2 환경 설정
        self._env = Environment(
            loader=FileSystemLoader(self._project_root / "templates"),
            autoescape=True
        )

    def generate_report(
            self,
            us_market: dict,
            kr_market: dict,
            us_stocks: list,
            kr_stocks: list,
            news_list: list,
            ai_comment: str = None
    ) -> str:
        """
        HTML 리포트 생성

        Args:
            us_market: 미국 시장 지수 데이터
            kr_market: 한국 시장 지수 데이터
            us_stocks: 미국 종목 리스트
            kr_stocks: 한국 종목 리스트
            news_list: 뉴스 헤드라인 리스트
            ai_comment: AI 시황 분석 (선택)

        Returns:
            생성된 HTML 파일 경로
        """
        # 템플릿 로드
        template = self._env.get_template("report.html")

        # 현재 시간
        now = datetime.now()

        # 데이터 바인딩
        html_content = template.render(
            report_date=now.strftime("%Y-%m-%d"),
            generated_at=now.strftime("%Y-%m-%d %H:%M KST"),
            us_market=us_market,
            kr_market=kr_market,
            us_stocks=us_stocks,
            kr_stocks=kr_stocks,
            news_list=news_list,
            ai_comment=ai_comment
        )

        # 파일 저장
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