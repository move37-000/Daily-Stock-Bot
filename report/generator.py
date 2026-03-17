from datetime import datetime
import os


def generate_report(us_results, kr_results):
    """마크다운 리포트 생성"""
    today = datetime.now().strftime("%Y-%m-%d")

    lines = [
        f"# 일일 주식 리포트 ({today})",
        "",
        "## 미국 주식",
        ""
    ]

    for stock in us_results:
        lines.append(f"### {stock['symbol']}")
        lines.append(f"- 종가: ${stock['close']:.2f}")
        lines.append(f"- 변동: ${stock['change']:+.2f} ({stock['change_pct']:+.2f}%)")
        lines.append("")

        # 뉴스 추가
        if stock.get('news'):
            lines.append("")
            lines.append("**관련 뉴스:**")
            for news in stock['news']:
                lines.append(f"- [{news['title']}]({news['link']}) - {news['publisher']}")

        lines.append("")

    lines.append("## 한국 주식")
    lines.append("")

    for stock in kr_results:
        lines.append(f"### {stock['name']} ({stock['code']})")
        lines.append(f"- 종가: {stock['close']:,}원")
        lines.append(f"- 변동: {stock['change']:+,}원 ({stock['change_pct']:+.2f}%)")

        # 뉴스 추가
        if stock.get('news'):
            lines.append("")
            lines.append("**관련 뉴스:**")
            for news in stock['news']:
                lines.append(f"- [{news['title']}]({news['link']})")

    return "\n".join(lines)


def save_report(content, filename=None):
    """리포트를 파일로 저장"""
    # reports 폴더 없으면 생성
    os.makedirs("reports", exist_ok=True)

    if filename is None:
        today = datetime.now().strftime("%Y%m%d")
        filename = f"reports/report_{today}.md"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

    return filename