from datetime import datetime
import os


def generate_report(us_results, kr_results, charts=None):
    """마크다운 리포트 생성"""
    today = datetime.now().strftime("%Y-%m-%d")

    lines = [
        f"# 일일 주식 리포트 ({today})",
        "",
        "## 📊 요약",
        ""
    ]

    # 상승/하락 카운트
    us_up = sum(1 for s in us_results if s['change'] >= 0)
    us_down = len(us_results) - us_up
    kr_up = sum(1 for s in kr_results if s['change'] >= 0)
    kr_down = len(kr_results) - kr_up

    lines.append(f"- 🇺🇸 미국: {us_up}상승 {us_down}하락")
    lines.append(f"- 🇰🇷 한국: {kr_up}상승 {kr_down}하락")
    lines.append("")

    # 미국 주식
    lines.append("## 🇺🇸 미국 주식")
    lines.append("")

    for stock in us_results:
        emoji = "🟢" if stock['change'] >= 0 else "🔴"
        lines.append(f"### {emoji} {stock['symbol']}")
        lines.append(f"- 종가: ${stock['close']:.2f}")
        lines.append(f"- 변동: ${stock['change']:+.2f} ({stock['change_pct']:+.2f}%)")

        # 차트 이미지 추가
        if charts:
            chart = next((c for c in charts if c['symbol'] == stock['symbol']), None)
            if chart:
                lines.append("")
                lines.append(f"![{stock['symbol']} 차트](charts/{stock['symbol']}_weekly.png)")

        if stock.get('news'):
            lines.append("")
            lines.append("**관련 뉴스:**")
            for news in stock['news']:
                lines.append(f"- [{news['title']}]({news['link']})")

        lines.append("")

    # 한국 주식
    lines.append("## 🇰🇷 한국 주식")
    lines.append("")

    for stock in kr_results:
        emoji = "🟢" if stock['change'] >= 0 else "🔴"
        lines.append(f"### {emoji} {stock['name']} ({stock['code']})")
        lines.append(f"- 종가: {stock['close']:,}원")
        lines.append(f"- 변동: {stock['change']:+,}원 ({stock['change_pct']:+.2f}%)")

        # 차트 이미지 추가 (name으로 매칭)
        if charts:
            chart = next((c for c in charts if c['symbol'] == stock['name']), None)
            if chart:
                lines.append("")
                lines.append(f"![{stock['name']} 차트](charts/{stock['name']}_weekly.png)")

        if stock.get('news'):
            lines.append("")
            lines.append("**관련 뉴스:**")
            for news in stock['news']:
                lines.append(f"- [{news['title']}]({news['link']})")

        lines.append("")

    return "\n".join(lines)


def save_report(content, filename=None):
    """리포트를 파일로 저장"""
    os.makedirs("reports", exist_ok=True)

    if filename is None:
        today = datetime.now().strftime("%Y%m%d")
        filename = f"reports/report_{today}.md"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

    return filename