"""
date_utils 모듈 테스트
"""
import pytest

from src.utils.date_utils import (
    format_us_news_time,
    format_kr_news_time,
    _format_korean_time,
)
from datetime import datetime


class TestFormatUsNewsTime:
    """format_us_news_time 함수 테스트"""

    def test_빈_문자열(self):
        """빈 문자열 입력 시 빈 문자열 반환"""
        result = format_us_news_time("")
        assert result == ""

    def test_정상_변환_오전(self):
        """오전 시간 변환"""
        result = format_us_news_time("2024-03-18T09:30:00Z")
        assert "3월 18일" in result
        assert "오전" in result
        assert "9시 30분" in result

    def test_정상_변환_오후(self):
        """오후 시간 변환"""
        result = format_us_news_time("2024-03-18T14:30:00Z")
        assert "3월 18일" in result
        assert "오후" in result
        assert "2시 30분" in result

    def test_자정(self):
        """자정(00시)은 오전 12시로 표시"""
        result = format_us_news_time("2024-03-18T00:00:00Z")
        assert "오전" in result
        assert "12시" in result

    def test_정오(self):
        """정오(12시)는 오후 12시로 표시"""
        result = format_us_news_time("2024-03-18T12:00:00Z")
        assert "오후" in result
        assert "12시" in result

    def test_잘못된_포맷(self):
        """잘못된 포맷은 빈 문자열 반환"""
        result = format_us_news_time("invalid-date")
        assert result == ""


class TestFormatKrNewsTime:
    """format_kr_news_time 함수 테스트"""

    def test_빈_문자열(self):
        """빈 문자열 입력 시 빈 문자열 반환"""
        result = format_kr_news_time("")
        assert result == ""

    def test_짧은_문자열(self):
        """12자 미만 문자열은 빈 문자열 반환"""
        result = format_kr_news_time("20240318")
        assert result == ""

    def test_정상_변환_오전(self):
        """오전 시간 변환"""
        result = format_kr_news_time("202403180930")
        assert "3월 18일" in result
        assert "오전" in result
        assert "9시 30분" in result

    def test_정상_변환_오후(self):
        """오후 시간 변환"""
        result = format_kr_news_time("202403181430")
        assert "3월 18일" in result
        assert "오후" in result
        assert "2시 30분" in result


class TestFormatKoreanTime:
    """_format_korean_time 함수 테스트"""

    def test_오전(self):
        """오전 시간"""
        dt = datetime(2024, 3, 18, 9, 30)
        result = _format_korean_time(dt)
        assert result == "3월 18일 오전 9시 30분"

    def test_오후(self):
        """오후 시간"""
        dt = datetime(2024, 3, 18, 15, 45)
        result = _format_korean_time(dt)
        assert result == "3월 18일 오후 3시 45분"

    def test_자정(self):
        """자정은 오전 12시"""
        dt = datetime(2024, 3, 18, 0, 0)
        result = _format_korean_time(dt)
        assert result == "3월 18일 오전 12시 0분"

    def test_정오(self):
        """정오는 오후 12시"""
        dt = datetime(2024, 3, 18, 12, 0)
        result = _format_korean_time(dt)
        assert result == "3월 18일 오후 12시 0분"
