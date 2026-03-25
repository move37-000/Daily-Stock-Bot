"""
transformer 모듈 테스트
"""
import pytest

from src.service.transformer import (
    transform_us_data,
    transform_kr_data,
    _get_us_logo_url,
    _get_kr_logo_url,
    _sort_and_format_history,
)


class TestTransformUsData:
    """transform_us_data 함수 테스트"""

    def test_빈_데이터(self):
        """빈 리스트 입력 시 빈 결과 반환"""
        us_market, us_stocks = transform_us_data([], {})

        assert us_stocks == []
        assert us_market["sp500"]["price"] == "-"
        assert us_market["nasdaq"]["price"] == "-"

    def test_정상_변환(self):
        """정상 데이터 변환"""
        us_results = [{
            "symbol": "AAPL",
            "close": 178.50,
            "change": 2.30,
            "change_pct": 1.31,
            "history": [
                {"date": "2024-03-18", "close": 176.20},
                {"date": "2024-03-19", "close": 178.50},
            ],
            "news": []
        }]
        us_index = {
            "sp500": {"price": "5,200.00", "change": 20, "change_pct": "0.39"}
        }

        us_market, us_stocks = transform_us_data(us_results, us_index)

        assert len(us_stocks) == 1
        assert us_stocks[0]["symbol"] == "AAPL"
        assert us_stocks[0]["name"] == "Apple Inc."
        assert us_stocks[0]["price"] == "178.50"
        assert us_stocks[0]["change_pct"] == "1.31"
        assert us_market["sp500"]["price"] == "5,200.00"

    def test_히스토리_정렬(self):
        """히스토리가 날짜순으로 정렬되는지 확인"""
        us_results = [{
            "symbol": "AAPL",
            "close": 180.00,
            "change": 1.00,
            "change_pct": 0.56,
            "history": [
                {"date": "2024-03-20", "close": 180.00},
                {"date": "2024-03-18", "close": 176.00},
                {"date": "2024-03-19", "close": 178.00},
            ],
            "news": []
        }]

        _, us_stocks = transform_us_data(us_results, {})

        history = us_stocks[0]["history"]
        assert history[0]["date"] == "2024-03-18"
        assert history[1]["date"] == "2024-03-19"
        assert history[2]["date"] == "2024-03-20"


class TestTransformKrData:
    """transform_kr_data 함수 테스트"""

    def test_빈_데이터(self):
        """빈 리스트 입력 시 빈 결과 반환"""
        kr_market, kr_stocks = transform_kr_data([], {})

        assert kr_stocks == []
        assert kr_market["kospi"]["price"] == "-"
        assert kr_market["kosdaq"]["price"] == "-"

    def test_정상_변환(self):
        """정상 데이터 변환"""
        kr_results = [{
            "code": "005930",
            "name": "삼성전자",
            "close": 71500,
            "change": -500,
            "change_pct": -0.69,
            "history": [],
            "news": []
        }]
        kr_index = {
            "kospi": {"price": "2,650.00", "change": 15, "change_pct": "0.57"}
        }

        kr_market, kr_stocks = transform_kr_data(kr_results, kr_index)

        assert len(kr_stocks) == 1
        assert kr_stocks[0]["symbol"] == "삼성전자"
        assert kr_stocks[0]["name"] == "005930"
        assert kr_stocks[0]["price"] == "71,500"
        assert kr_stocks[0]["change_pct"] == "0.69"  # abs() 적용됨
        assert kr_market["kospi"]["price"] == "2,650.00"


class TestGetLogoUrl:
    """로고 URL 생성 테스트"""

    def test_미국_알려진_종목(self):
        """알려진 미국 종목은 매핑된 도메인 사용"""
        url = _get_us_logo_url("AAPL")
        assert "apple.com" in url

    def test_미국_모르는_종목(self):
        """모르는 종목은 심볼.com 사용"""
        url = _get_us_logo_url("XYZ")
        assert "xyz.com" in url

    def test_한국_종목(self):
        """한국 종목은 토스 URL 사용"""
        url = _get_kr_logo_url("005930")
        assert "005930" in url
        assert "tossinvest" in url


class TestSortAndFormatHistory:
    """_sort_and_format_history 함수 테스트"""

    def test_빈_히스토리(self):
        """빈 리스트 입력"""
        result = _sort_and_format_history([])
        assert result == []

    def test_정렬_및_포맷(self):
        """날짜순 정렬 + price 키로 변환"""
        history = [
            {"date": "2024-03-20", "close": 180},
            {"date": "2024-03-18", "close": 176},
        ]

        result = _sort_and_format_history(history)

        assert result[0]["date"] == "2024-03-18"
        assert result[0]["price"] == 176
        assert result[1]["date"] == "2024-03-20"
        assert result[1]["price"] == 180
