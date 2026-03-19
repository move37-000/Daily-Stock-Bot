import requests


def send_slack_message(webhook_url, us_results, kr_results):
    """Slack으로 주식 리포트 전송"""

    lines = ["*📈 일일 주식 리포트*", ""]

    lines.append("*🇺🇸 미국 주식*")
    for stock in us_results:
        emoji = "🔴" if stock['change'] < 0 else "🟢"
        lines.append(f"{emoji} *{stock['symbol']}*: ${stock['close']:.2f} ({stock['change_pct']:+.2f}%)")

    lines.append("")
    lines.append("*🇰🇷 한국 주식*")
    for stock in kr_results:
        emoji = "🔴" if stock['change'] < 0 else "🟢"
        lines.append(f"{emoji} *{stock['name']}*: {stock['close']:,}원 ({stock['change_pct']:+.2f}%)")

    message = "\n".join(lines)

    payload = {"text": message}
    response = requests.post(webhook_url, json=payload)

    return response.status_code == 200