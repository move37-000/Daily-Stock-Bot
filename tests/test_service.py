from src.service import generate_report


def test_generate_report_returns_string():
    """리포트가 문자열로 반환되는지 확인"""
    us_results = [{
        'symbol': 'AAPL',
        'close': 150.0,
        'change': 2.0,
        'change_pct': 1.35,
        'news': []
    }]
    kr_results = [{
        'code': '005930',
        'name': '삼성전자',
        'close': 70000,
        'change': 1000,
        'change_pct': 1.45,
        'news': []
    }]

    result = generate_report(us_results, kr_results)

    assert isinstance(result, str)
    assert "AAPL" in result
    assert "삼성전자" in result


def test_generate_report_contains_header():
    """리포트에 헤더가 포함되는지 확인"""
    result = generate_report([], [])

    assert "일일 주식 리포트" in result