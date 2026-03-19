import requests


def send_slack_message(webhook_url, us_results, kr_results):
    """Slack으로 주식 리포트 전송"""
    from datetime import datetime
    today = datetime.now().strftime("%Y-%m-%d")

    # 상승/하락 카운트
    us_up = sum(1 for s in us_results if s['change'] >= 0)
    us_down = len(us_results) - us_up
    kr_up = sum(1 for s in kr_results if s['change'] >= 0)
    kr_down = len(kr_results) - kr_up

    # Top 상승/하락 찾기
    all_stocks = []
    for s in us_results:
        all_stocks.append({'name': s['symbol'], 'pct': s['change_pct']})
    for s in kr_results:
        all_stocks.append({'name': s['name'], 'pct': s['change_pct']})

    top_gainer = max(all_stocks, key=lambda x: x['pct'])
    top_loser = min(all_stocks, key=lambda x: x['pct'])

    # 메시지 구성
    lines = [
        f"*📊 일일 주식 리포트 ({today})*",
        "",
        "━━━ *오늘의 요약* ━━━",
        f"🇺🇸 미국: {us_up}상승 {us_down}하락 | 🇰🇷 한국: {kr_up}상승 {kr_down}하락",
        "",
        f"📈 Top 상승: {top_gainer['name']} {top_gainer['pct']:+.2f}%",
        f"📉 Top 하락: {top_loser['name']} {top_loser['pct']:+.2f}%",
        "",
        "━━━ *미국 주식* ━━━"
    ]

    for stock in us_results:
        emoji = "🔴" if stock['change'] < 0 else "🟢"
        lines.append(f"{emoji} {stock['symbol']:6} ${stock['close']:<8.2f} {stock['change_pct']:+.2f}%")

    lines.append("")
    lines.append("━━━ *한국 주식* ━━━")

    for stock in kr_results:
        emoji = "🔴" if stock['change'] < 0 else "🟢"
        lines.append(f"{emoji} {stock['name']:6} {stock['close']:>8,}원 {stock['change_pct']:+.2f}%")

    message = "\n".join(lines)

    payload = {"text": message}
    response = requests.post(webhook_url, json=payload)

    return response.status_code == 200