"""
날짜/시간 유틸리티 모듈

뉴스 시간 포맷 변환 등 날짜 관련 공통 함수를 제공합니다.
"""
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


def format_us_news_time(pub_date: str) -> str:
    """
    미국 뉴스 시간 포맷 변환 (ISO 8601 → 한글)

    Args:
        pub_date: ISO 8601 형식의 시간 문자열 (예: "2024-03-24T14:30:00Z")

    Returns:
        한글 형식의 시간 문자열 (예: "3월 24일 오후 2시 30분")
        파싱 실패 시 빈 문자열 반환
    """
    if not pub_date:
        return ""

    try:
        dt = datetime.strptime(pub_date, "%Y-%m-%dT%H:%M:%SZ")
        return _format_korean_time(dt)
    except ValueError as e:
        logger.debug(f"미국 뉴스 시간 파싱 실패: {pub_date}, {e}")
        return ""


def format_kr_news_time(datetime_str: str) -> str:
    """
    한국 뉴스 시간 포맷 변환 (네이버 형식 → 한글)

    Args:
        datetime_str: 네이버 형식의 시간 문자열 (예: "202403241430")

    Returns:
        한글 형식의 시간 문자열 (예: "3월 24일 오후 2시 30분")
        파싱 실패 시 빈 문자열 반환
    """
    if not datetime_str or len(datetime_str) < 12:
        return ""

    try:
        month = int(datetime_str[4:6])
        day = int(datetime_str[6:8])
        hour = int(datetime_str[8:10])
        minute = int(datetime_str[10:12])

        dt = datetime(2000, month, day, hour, minute)  # 연도는 포맷팅에 사용 안 함
        return _format_korean_time(dt)
    except (ValueError, IndexError) as e:
        logger.debug(f"한국 뉴스 시간 파싱 실패: {datetime_str}, {e}")
        return ""


def _format_korean_time(dt: datetime) -> str:
    """
    datetime 객체를 한글 시간 포맷으로 변환

    Args:
        dt: datetime 객체

    Returns:
        한글 형식의 시간 문자열 (예: "3월 24일 오후 2시 30분")
    """
    hour = dt.hour
    minute = dt.minute

    if hour < 12:
        ampm = "오전"
        display_hour = hour if hour != 0 else 12
    else:
        ampm = "오후"
        display_hour = hour - 12 if hour != 12 else 12

    return f"{dt.month}월 {dt.day}일 {ampm} {display_hour}시 {minute}분"
