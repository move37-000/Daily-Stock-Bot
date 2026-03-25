"""
stock_service 모듈 테스트
"""
import pytest

from src.service.stock_service import _calculate_daily_change


class TestCalculateDailyChange:
    """_calculate_daily_change 함수 테스트"""

    def test_첫번째_인덱스(self):
        """첫 번째 인덱스는 변동 0"""
        history = [
            {"close": 100},
            {"close": 110},
        ]

        change, change_pct = _calculate_daily_change(history, 0)

        assert change == 0
        assert change_pct == 0

    def test_상승(self):
        """가격 상승 시 양수 반환"""
        history = [
            {"close": 100},
            {"close": 110},
        ]

        change, change_pct = _calculate_daily_change(history, 1)

        assert change == 10
        assert change_pct == 10.0

    def test_하락(self):
        """가격 하락 시 음수 반환"""
        history = [
            {"close": 100},
            {"close": 90},
        ]

        change, change_pct = _calculate_daily_change(history, 1)

        assert change == -10
        assert change_pct == -10.0

    def test_변동_없음(self):
        """가격 변동 없으면 0"""
        history = [
            {"close": 100},
            {"close": 100},
        ]

        change, change_pct = _calculate_daily_change(history, 1)

        assert change == 0
        assert change_pct == 0
