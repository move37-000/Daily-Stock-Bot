"""
알림 서비스 모듈

Slack, Discord 등 외부 서비스로 리포트 알림을 전송합니다.
"""
import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Any

import requests

logger = logging.getLogger(__name__)


@dataclass
class NotificationData:
    """알림용 데이터 구조"""
    today: str
    us_up: int
    us_down: int
    kr_up: int
    kr_down: int
    top_gainer: dict[str, Any]
    top_loser: dict[str, Any]


def send_slack_message(
    webhook_url: str,
    us_results: list[dict[str, Any]],
    kr_results: list[dict[str, Any]],
    us_market: dict[str, Any] | None = None,
    kr_market: dict[str, Any] | None = None,
    usd_krw: dict[str, Any] | None = None,
    report_url: str | None = None
) -> bool:
    """
    Slack으로 주식 리포트 전송

    Returns:
        전송 성공 여부
    """
    data = _prepare_notification_data(us_results, kr_results)
    message = _build_slack_message(data, us_market, kr_market, usd_krw)
    blocks = _build_slack_blocks(message, report_url)

    payload = {
        "text": message,
        "blocks": blocks
    }

    try:
        response = requests.post(webhook_url, json=payload)
        return response.status_code == 200
    except Exception as e:
        logger.error(f"Slack 전송 실패: {e}")
        return False


def send_discord_message(
    webhook_url: str,
    us_results: list[dict[str, Any]],
    kr_results: list[dict[str, Any]],
    us_market: dict[str, Any] | None = None,
    kr_market: dict[str, Any] | None = None,
    usd_krw: dict[str, Any] | None = None,
    report_url: str | None = None
) -> bool:
    """
    Discord로 주식 리포트 전송

    Returns:
        전송 성공 여부
    """
    data = _prepare_notification_data(us_results, kr_results)
    description = _build_discord_description(data, us_market, kr_market, usd_krw, report_url)

    embed = {
        "title": "📈 일일 주식 리포트",
        "description": description,
        "color": 0x5865F2,
        "footer": {
            "text": f"Daily Stock Bot • {data.today}"
        }
    }

    payload = {"embeds": [embed]}

    try:
        response = requests.post(webhook_url, json=payload)
        return response.status_code == 204
    except Exception as e:
        logger.error(f"Discord 전송 실패: {e}")
        return False


# =============================================================================
# Private Helper Functions
# =============================================================================

def _prepare_notification_data(
    us_results: list[dict[str, Any]],
    kr_results: list[dict[str, Any]]
) -> NotificationData:
    """알림용 공통 데이터 준비"""
    today = datetime.now().strftime("%Y-%m-%d")

    # 상승/하락 카운트
    us_up = sum(1 for s in us_results if s['change'] >= 0)
    us_down = len(us_results) - us_up
    kr_up = sum(1 for s in kr_results if s['change'] >= 0)
    kr_down = len(kr_results) - kr_up

    # Top 상승/하락 찾기
    all_stocks = [
        {'name': s['symbol'], 'pct': s['change_pct']} for s in us_results
    ] + [
        {'name': s['name'], 'pct': s['change_pct']} for s in kr_results
    ]

    top_gainer = max(all_stocks, key=lambda x: x['pct'])
    top_loser = min(all_stocks, key=lambda x: x['pct'])

    return NotificationData(
        today=today,
        us_up=us_up,
        us_down=us_down,
        kr_up=kr_up,
        kr_down=kr_down,
        top_gainer=top_gainer,
        top_loser=top_loser
    )


def _format_index_line(
    index_data: dict[str, Any],
    name: str,
    use_backticks: bool = False
) -> str:
    """지수 한 줄 포맷팅"""
    emoji = "🔴" if index_data.get('change', 0) < 0 else "🟢"
    sign = "+" if index_data.get('change', 0) >= 0 else "-"
    price = index_data.get('price', '-')
    pct = index_data.get('change_pct', '-')

    if use_backticks:
        return f"{emoji} {name} `{price}` ({sign}{pct}%)"
    return f"{emoji} {name}  {price} ({sign}{pct}%)"


def _build_slack_message(
    data: NotificationData,
    us_market: dict[str, Any] | None,
    kr_market: dict[str, Any] | None,
    usd_krw: dict[str, Any] | None
) -> str:
    """Slack 메시지 텍스트 생성"""
    lines = [f"📊 *일일 주식 리포트* | {data.today}", "", ""]

    # 지수 정보
    if us_market and kr_market:
        lines.append("*시장 지수*")
        lines.append("")
        lines.append(_format_index_line(us_market.get('sp500', {}), "S&P 500"))
        lines.append(_format_index_line(us_market.get('nasdaq', {}), "NASDAQ"))
        lines.append(_format_index_line(kr_market.get('kospi', {}), "KOSPI"))
        lines.append(_format_index_line(kr_market.get('kosdaq', {}), "KOSDAQ"))
        lines.extend(["", ""])

    # 환율 정보
    if usd_krw and usd_krw.get('price') != '-':
        emoji = "🔴" if usd_krw.get('change', 0) < 0 else "🟢"
        sign = "+" if usd_krw.get('change', 0) >= 0 else "-"
        lines.append(f"💵 *USD/KRW*  {usd_krw.get('price', '-')} ({sign}{usd_krw.get('change_pct', '-')}%)")
        lines.extend(["", ""])

    # 요약
    lines.append("*오늘의 요약*")
    lines.append("")
    lines.append(f"🇺🇸 미국 {data.us_up}↑ {data.us_down}↓ | 🇰🇷 한국 {data.kr_up}↑ {data.kr_down}↓")
    lines.append(f"📈 {data.top_gainer['name']} {data.top_gainer['pct']:+.2f}% | 📉 {data.top_loser['name']} {data.top_loser['pct']:+.2f}%")
    lines.append("")

    return "\n".join(lines)


def _build_slack_blocks(message: str, report_url: str | None) -> list[dict[str, Any]]:
    """Slack Block Kit 구성"""
    blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": message
            }
        }
    ]

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

    return blocks


def _build_discord_description(
    data: NotificationData,
    us_market: dict[str, Any] | None,
    kr_market: dict[str, Any] | None,
    usd_krw: dict[str, Any] | None,
    report_url: str | None
) -> str:
    """Discord Embed description 생성"""
    lines = []

    if us_market:
        lines.append("**🇺🇸 US Market**")
        lines.append(_format_index_line(us_market.get('sp500', {}), "S&P 500", use_backticks=True))
        lines.append(_format_index_line(us_market.get('nasdaq', {}), "NASDAQ", use_backticks=True))
        lines.append("")

    if kr_market:
        lines.append("**🇰🇷 KR Market**")
        lines.append(_format_index_line(kr_market.get('kospi', {}), "KOSPI", use_backticks=True))
        lines.append(_format_index_line(kr_market.get('kosdaq', {}), "KOSDAQ", use_backticks=True))
        lines.append("")

    if usd_krw and usd_krw.get('price') != '-':
        emoji = "🔴" if usd_krw.get('change', 0) < 0 else "🟢"
        sign = "+" if usd_krw.get('change', 0) >= 0 else ""
        lines.append("**💵 USD/KRW**")
        lines.append(f"{emoji} `{usd_krw.get('price', '-')}` ({sign}{usd_krw.get('change_pct', '-')}%)")
        lines.append("")

    lines.append("**📊 오늘의 요약**")
    lines.append(f"🇺🇸 {data.us_up}↑ {data.us_down}↓ │ 🇰🇷 {data.kr_up}↑ {data.kr_down}↓")
    lines.append(f"📈 {data.top_gainer['name']} `{data.top_gainer['pct']:+.2f}%` │ 📉 {data.top_loser['name']} `{data.top_loser['pct']:+.2f}%`")

    if report_url:
        lines.append("")
        lines.append(f"[📊 **전체 리포트 보기**]({report_url})")

    return "\n".join(lines)
