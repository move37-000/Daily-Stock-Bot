import requests


def send_slack_message(webhook_url, us_results, kr_results, us_market=None, kr_market=None, usd_krw=None,
                       report_url=None):
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
    lines = [f"📊 *일일 주식 리포트* | {today}", ""]

    lines.append("")
    lines.append("")

    # 지수 정보
    if us_market and kr_market:
        lines.append("*시장 지수*")

        lines.append("")

        sp500 = us_market.get('sp500', {})
        sp500_emoji = "🔴" if sp500.get('change', 0) < 0 else "🟢"
        sp500_sign = "+" if sp500.get('change', 0) >= 0 else "-"
        lines.append(f"{sp500_emoji} S&P 500  {sp500.get('price', '-')} ({sp500_sign}{sp500.get('change_pct', '-')}%)")

        nasdaq = us_market.get('nasdaq', {})
        nasdaq_emoji = "🔴" if nasdaq.get('change', 0) < 0 else "🟢"
        nasdaq_sign = "+" if nasdaq.get('change', 0) >= 0 else "-"
        lines.append(
            f"{nasdaq_emoji} NASDAQ  {nasdaq.get('price', '-')} ({nasdaq_sign}{nasdaq.get('change_pct', '-')}%)")

        kospi = kr_market.get('kospi', {})
        kospi_emoji = "🔴" if kospi.get('change', 0) < 0 else "🟢"
        kospi_sign = "+" if kospi.get('change', 0) >= 0 else "-"
        lines.append(f"{kospi_emoji} KOSPI  {kospi.get('price', '-')} ({kospi_sign}{kospi.get('change_pct', '-')}%)")

        kosdaq = kr_market.get('kosdaq', {})
        kosdaq_emoji = "🔴" if kosdaq.get('change', 0) < 0 else "🟢"
        kosdaq_sign = "+" if kosdaq.get('change', 0) >= 0 else "-"
        lines.append(
            f"{kosdaq_emoji} KOSDAQ  {kosdaq.get('price', '-')} ({kosdaq_sign}{kosdaq.get('change_pct', '-')}%)")

        lines.append("")
        lines.append("")

    # 환율 정보
    if usd_krw and usd_krw.get('price') != '-':
        usd_emoji = "🔴" if usd_krw.get('change', 0) < 0 else "🟢"
        usd_sign = "+" if usd_krw.get('change', 0) >= 0 else "-"
        lines.append(f"💵 *USD/KRW*  {usd_krw.get('price', '-')} ({usd_sign}{usd_krw.get('change_pct', '-')}%)")

        lines.append("")
        lines.append("")

    # 요약
    lines.append("*오늘의 요약*")
    lines.append("")
    lines.append(f"🇺🇸 미국 {us_up}↑ {us_down}↓ | 🇰🇷 한국 {kr_up}↑ {kr_down}↓")
    lines.append(f"📈 {top_gainer['name']} {top_gainer['pct']:+.2f}% | 📉 {top_loser['name']} {top_loser['pct']:+.2f}%")

    lines.append("")

    message = "\n".join(lines)

    # Block Kit
    blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": message
            }
        }
    ]

    # 리포트 버튼
    if report_url:
        blocks.append({"type": "divider"})
        blocks.append({
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "📊 전체 리포트 보기",
                        "emoji": True
                    },
                    "url": report_url,
                    "style": "primary"
                }
            ]
        })

    payload = {
        "text": message,
        "blocks": blocks
    }

    response = requests.post(webhook_url, json=payload)

    return response.status_code == 200


def send_discord_message(webhook_url, us_results, kr_results, us_market=None, kr_market=None, usd_krw=None,
                         report_url=None):
    """Discord로 주식 리포트 전송"""
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

    # 지수 텍스트 구성
    lines = []

    if us_market:
        sp500 = us_market.get('sp500', {})
        sp500_emoji = "🔴" if sp500.get('change', 0) < 0 else "🟢"
        sp500_sign = "+" if sp500.get('change', 0) >= 0 else ""

        nasdaq = us_market.get('nasdaq', {})
        nasdaq_emoji = "🔴" if nasdaq.get('change', 0) < 0 else "🟢"
        nasdaq_sign = "+" if nasdaq.get('change', 0) >= 0 else ""

        lines.append("**🇺🇸 US Market**")
        lines.append(f"{sp500_emoji} S&P 500 `{sp500.get('price', '-')}` ({sp500_sign}{sp500.get('change_pct', '-')}%)")
        lines.append(
            f"{nasdaq_emoji} NASDAQ `{nasdaq.get('price', '-')}` ({nasdaq_sign}{nasdaq.get('change_pct', '-')}%)")
        lines.append("")

    if kr_market:
        kospi = kr_market.get('kospi', {})
        kospi_emoji = "🔴" if kospi.get('change', 0) < 0 else "🟢"
        kospi_sign = "+" if kospi.get('change', 0) >= 0 else ""

        kosdaq = kr_market.get('kosdaq', {})
        kosdaq_emoji = "🔴" if kosdaq.get('change', 0) < 0 else "🟢"
        kosdaq_sign = "+" if kosdaq.get('change', 0) >= 0 else ""

        lines.append("**🇰🇷 KR Market**")
        lines.append(f"{kospi_emoji} KOSPI `{kospi.get('price', '-')}` ({kospi_sign}{kospi.get('change_pct', '-')}%)")
        lines.append(
            f"{kosdaq_emoji} KOSDAQ `{kosdaq.get('price', '-')}` ({kosdaq_sign}{kosdaq.get('change_pct', '-')}%)")
        lines.append("")

    if usd_krw and usd_krw.get('price') != '-':
        usd_emoji = "🔴" if usd_krw.get('change', 0) < 0 else "🟢"
        usd_sign = "+" if usd_krw.get('change', 0) >= 0 else ""
        lines.append("**💵 USD/KRW**")
        lines.append(f"{usd_emoji} `{usd_krw.get('price', '-')}` ({usd_sign}{usd_krw.get('change_pct', '-')}%)")
        lines.append("")

    lines.append("**📊 오늘의 요약**")
    lines.append(f"🇺🇸 {us_up}↑ {us_down}↓ │ 🇰🇷 {kr_up}↑ {kr_down}↓")
    lines.append(
        f"📈 {top_gainer['name']} `{top_gainer['pct']:+.2f}%` │ 📉 {top_loser['name']} `{top_loser['pct']:+.2f}%`")

    if report_url:
        lines.append("")
        lines.append(f"[📊 **전체 리포트 보기**]({report_url})")

    description = "\n".join(lines)

    # Embed 구성
    embed = {
        "title": "📈 일일 주식 리포트",
        "description": description,
        "color": 0x5865F2,
        "footer": {
            "text": f"Daily Stock Bot • {today}"
        }
    }

    payload = {
        "embeds": [embed]
    }

    response = requests.post(webhook_url, json=payload)

    return response.status_code == 204