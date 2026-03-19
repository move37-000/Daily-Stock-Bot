from src.config import US_TICKERS, KR_TICKERS


def test_us_tickers_not_empty():
    """미국 종목 리스트가 비어있지 않은지 확인"""
    assert len(US_TICKERS) > 0


def test_kr_tickers_not_empty():
    """한국 종목 리스트가 비어있지 않은지 확인"""
    assert len(KR_TICKERS) > 0


def test_us_tickers_are_strings():
    """미국 종목 코드가 문자열인지 확인"""
    for ticker in US_TICKERS:
        assert isinstance(ticker, str)


def test_kr_tickers_have_name():
    """한국 종목이 코드와 이름을 가지는지 확인"""
    for code, name in KR_TICKERS.items():
        assert isinstance(code, str)
        assert isinstance(name, str)