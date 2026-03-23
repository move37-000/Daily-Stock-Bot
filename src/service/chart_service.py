import matplotlib.pyplot as plt
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


def generate_chart_base64(symbol, history):
    """
    주간 차트를 base64 문자열로 반환 (HTML 임베드용)

    Args:
        symbol: 종목 심볼 (로깅용)
        history: [{'date': '2025-01-15', 'close': 228.44}, ...] 형태

    Returns:
        base64 인코딩된 PNG 이미지 문자열, 데이터 부족 시 None
    """
    if len(history) < 2:
        return None

    dates = [h['date'] for h in reversed(history)]
    prices = [h['close'] for h in reversed(history)]

    fig, ax = plt.subplots(figsize=(6, 3))

    x = range(len(dates))
    ax.plot(x, prices, marker='o', linewidth=2, markersize=4, color='#2563eb')

    if prices[-1] >= prices[0]:
        ax.fill_between(x, prices, prices[0], alpha=0.3, color='#22c55e')
    else:
        ax.fill_between(x, prices, prices[0], alpha=0.3, color='#ef4444')

    ax.set_xticks(x)
    ax.set_xticklabels([d[5:] for d in dates], fontsize=8)
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