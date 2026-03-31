from datetime import datetime
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader

_PROJECT_ROOT = Path(__file__).parent.parent.parent
_ENV = Environment(
    loader=FileSystemLoader(_PROJECT_ROOT / "templates"),
    autoescape=True
)


def generate_report(
    us_market: dict[str, Any],
    kr_market: dict[str, Any],
    us_stocks: list[dict[str, Any]],
    kr_stocks: list[dict[str, Any]],
    us_market_news: list[dict[str, Any]],
    kr_market_news: list[dict[str, Any]],
    usd_krw: dict[str, Any] | None = None,
    ai_comment: str | None = None
) -> str:
    template = _ENV.get_template("report.html")
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

    return _save_report(html_content, now)


def _save_report(content: str, timestamp: datetime) -> str:
    reports_dir = _PROJECT_ROOT / "reports"
    reports_dir.mkdir(exist_ok=True)

    filename = f"report_{timestamp.strftime('%Y%m%d_%H%M%S')}.html"
    file_path = reports_dir / filename

    file_path.write_text(content, encoding="utf-8")
    return str(file_path)
