import os
import logging
from ftplib import print_line

from google import genai

from src.config import GEMINI_MODELS

logger = logging.getLogger(__name__)


def generate_market_comment(
        us_market: dict,
        kr_market: dict,
        us_stocks: list,
        kr_stocks: list
) -> str | None:
    """AI 시황 분석 생성 (fallback 지원)"""

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        logger.warning("GEMINI_API_KEY가 설정되지 않음")
        return None

    client = genai.Client(api_key=api_key)
    prompt = _build_prompt(us_market, kr_market, us_stocks, kr_stocks)

    # for model in GEMINI_MODELS:
    #     try:
    #         logger.info(f"AI 모델 시도: {model}")
    #         response = client.models.generate_content(
    #             model=model,
    #             contents=prompt
    #         )
    #         logger.info(f"AI 분석 성공: {model}")
    #         return response.text.strip()
    #
    #     except Exception as e:
    #         logger.warning(f"{model} 실패: {e}")
    #         continue

    logger.error("모든 AI 모델 실패")
    return None


def _build_prompt(
        us_market: dict,
        kr_market: dict,
        us_stocks: list,
        kr_stocks: list
) -> str:
    """프롬포트 생성"""

    # 미국 지수 정보
    sp500 = us_market.get("sp500", {})
    nasdaq = us_market.get("nasdaq", {})

    # 한국 지수 정보
    kospi = kr_market.get("kospi", {})
    kosdaq = kr_market.get("kosdaq", {})

    # 종목 정보 요약
    us_summary = ", ".join([
        f"{s.get('symbol', '')} {s.get('change_pct', 0)}%"
        for s in us_stocks[:3]
    ])

    kr_summary = ", ".join([
        f"{s.get('symbol', '')} {s.get('change_pct', 0)}%"
        for s in kr_stocks[:3]
    ])

    prompt = f"""당신은 개인 투자자를 위한 세계 제일의 유능하고 전문적인 주식 애널리스트 입니다.

    아래 데이터를 바탕으로 오늘 한국장 개장 전 시황 브리핑을 작성해주세요.

    ## 데이터

    **미국장 (오늘 새벽 마감)**
    - S&P 500: {sp500.get('price', '-')} ({sp500.get('change_pct', '-')}%)
    - NASDAQ: {nasdaq.get('price', '-')} ({nasdaq.get('change_pct', '-')}%)
    - 주요 종목: {us_summary}

    **한국장 (어제 마감)**
    - KOSPI: {kospi.get('price', '-')} ({kospi.get('change_pct', '-')}%)
    - KOSDAQ: {kosdaq.get('price', '-')} ({kosdaq.get('change_pct', '-')}%)
    - 주요 종목: {kr_summary}

    ## 작성 규칙
    1. 7 - 8 문장으로 간결하게
    2. 어제 한국장 → 미국장 영향 → 오늘 한국장 전망 순서
    3. 세계적인 정세 또는 뉴스를 최대한 참고하면서 설명도
    3. 반말로 친근하게 ("~했어", "~될 것 같아")
    4. 숫자는 이미 위에 있으니 반복하지 말고 흐름 위주로(중요한건 표현해도 됨)
    5. 투자 권유가 아닌 정보 제공 목적임을 인지

    브리핑을 작성해줘."""

    return prompt
