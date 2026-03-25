import logging

from src.config import (
    US_TICKERS,
    KR_TICKERS,
    SLACK_WEBHOOK_URL,
    DISCORD_WEBHOOK_URL,
    REPORT_URL,
)
from src.repository import init_db
from src.crawler import (
    fetch_us_stocks,
    fetch_kr_stocks,
    fetch_us_index,
    fetch_kr_index,
    fetch_usd_krw,
    fetch_us_market_news,
    fetch_kr_market_news,
)
from src.service import (
    generate_report,
    send_slack_message,
    send_discord_message,
    save_stocks,
    transform_us_data,
    transform_kr_data,
)

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


def main() -> None:
    # 1. DB 초기화
    try:
        init_db()
    except Exception as e:
        logger.error(f"DB 초기화 실패: {e}")
        return

    # 2. 데이터 수집
    logger.info("데이터 수집 중...")
    us_results = fetch_us_stocks(US_TICKERS)
    kr_results = fetch_kr_stocks(KR_TICKERS)

    # 2. 지수 데이터 수집
    logger.info("지수 데이터 수집 중...")
    us_index = fetch_us_index()
    kr_index = fetch_kr_index()
    usd_krw = fetch_usd_krw()

    # 3. 시장 뉴스 수집
    logger.info("시장 뉴스 수집 중...")
    us_market_news = fetch_us_market_news()
    kr_market_news = fetch_kr_market_news()

    # 4. DB 저장
    logger.info("DB 저장 중...")
    save_stocks(us_results, kr_results)

    # 5. 데이터 변환
    logger.info("데이터 변환 중...")
    us_market, us_stocks = transform_us_data(us_results, us_index)
    kr_market, kr_stocks = transform_kr_data(kr_results, kr_index)

    # 6. HTML 리포트 생성
    _generate_report(us_market, kr_market, us_stocks, kr_stocks, 
                     us_market_news, kr_market_news, usd_krw)

    # 7. 알림 전송
    _send_notifications(us_results, kr_results, us_market, kr_market, usd_krw)


def _generate_report(
    us_market, kr_market, us_stocks, kr_stocks,
    us_market_news, kr_market_news, usd_krw
) -> None:
    """HTML 리포트 생성"""
    logger.info("리포트 생성 중...")
    try:
        filename = generate_report(
            us_market=us_market,
            kr_market=kr_market,
            us_stocks=us_stocks,
            kr_stocks=kr_stocks,
            us_market_news=us_market_news,
            kr_market_news=kr_market_news,
            usd_krw=usd_krw,
            ai_comment=None
        )
        logger.info(f"리포트 저장 완료: {filename}")
    except Exception as e:
        logger.error(f"리포트 생성 실패: {e}")


def _send_notifications(
    us_results, kr_results, us_market, kr_market, usd_krw
) -> None:
    """Slack/Discord 알림 전송"""
    # Slack
    logger.info("Slack 전송 중...")
    try:
        if send_slack_message(
            SLACK_WEBHOOK_URL,
            us_results,
            kr_results,
            us_market=us_market,
            kr_market=kr_market,
            usd_krw=usd_krw,
            report_url=REPORT_URL
        ):
            logger.info("Slack 전송 완료!")
        else:
            logger.warning("Slack 전송 실패")
    except Exception as e:
        logger.error(f"Slack 전송 실패: {e}")

    # Discord
    if DISCORD_WEBHOOK_URL:
        logger.info("Discord 전송 중...")
        try:
            if send_discord_message(
                DISCORD_WEBHOOK_URL,
                us_results,
                kr_results,
                us_market=us_market,
                kr_market=kr_market,
                usd_krw=usd_krw,
                report_url=REPORT_URL
            ):
                logger.info("Discord 전송 완료!")
            else:
                logger.warning("Discord 전송 실패")
        except Exception as e:
            logger.error(f"Discord 전송 실패: {e}")


if __name__ == "__main__":
    main()
