import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import platform
import base64
from io import BytesIO

# 한글 폰트 설정
if platform.system() == 'Windows':
    plt.rcParams['font.family'] = 'Malgun Gothic'
elif platform.system() == 'Darwin':
    plt.rcParams['font.family'] = 'AppleGothic'
else:
    plt.rcParams['font.family'] = 'NanumGothic'

plt.rcParams['axes.unicode_minus'] = False

def _format_price(value, pos):
    """Y축 금액 포맷터 (천 단위 콤마)"""
    if value >= 1000:
        return f'{value:,.0f}'
    else:
        return f'{value:.2f}'


def generate_chart_base64(symbol, history):
    """
    주간 차트를 base64 문자열로 반환 (HTML 임베드용)

    Args:
        symbol: 종목 심볼 (로깅용)
        history: [{'date': '2025-01-15', 'close': 228.44}, ...] 형태
                 날짜 오름차순 (오래된 날짜 → 최신 날짜)

    Returns:
        base64 인코딩된 PNG 이미지 문자열, 데이터 부족 시 None
    """
    if len(history) < 2:
        return None

    # 날짜 오름차순 정렬 (왼쪽=과거, 오른쪽=최신)
    sorted_history = sorted(history, key=lambda h: h['date'])

    dates = [h['date'] for h in sorted_history]
    prices = [h['close'] for h in sorted_history]

    fig, ax = plt.subplots(figsize=(6, 3))

    x = range(len(dates))
    ax.plot(x, prices, marker='o', linewidth=2, markersize=4, color='#2563eb')

    # 시작 대비 상승/하락 색상
    if prices[-1] >= prices[0]:
        ax.fill_between(x, prices, prices[0], alpha=0.3, color='#22c55e')
    else:
        ax.fill_between(x, prices, prices[0], alpha=0.3, color='#ef4444')

    # X축: 날짜 (MM-DD 형식)
    ax.set_xticks(x)
    ax.set_xticklabels([d[5:] for d in dates], fontsize=8)

    # Y축: 천 단위 콤마 포맷
    ax.yaxis.set_major_formatter(FuncFormatter(_format_price))
    ax.tick_params(axis='y', labelsize=8)

    ax.set_xlabel("")
    ax.set_ylabel("")

    plt.tight_layout()

    # 메모리 버퍼에 저장 → base64 변환
    buffer = BytesIO()
    plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
    plt.close()

    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()

    return image_base64