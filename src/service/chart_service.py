import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import platform
import base64
from io import BytesIO
import numpy as np

# 한글 폰트 설정
if platform.system() == 'Windows':
    plt.rcParams['font.family'] = 'Malgun Gothic'
elif platform.system() == 'Darwin':
    plt.rcParams['font.family'] = 'AppleGothic'
else:
    plt.rcParams['font.family'] = 'NanumGothic'

plt.rcParams['axes.unicode_minus'] = False


def _format_price(value, pos):
    """Y축 금액 포맷터"""
    if value >= 1000:
        return f'{value:,.0f}'
    else:
        return f'{value:.2f}'


def generate_chart_base64(symbol, history):
    """
    주간 차트를 base64 문자열로 반환
    """
    if len(history) < 2:
        return None

    # 날짜 오름차순 정렬
    sorted_history = sorted(history, key=lambda h: h['date'])

    dates = [h['date'] for h in sorted_history]
    prices = [h['close'] for h in sorted_history]

    # 스타일 설정
    fig, ax = plt.subplots(figsize=(7, 3))
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')

    x = np.arange(len(dates))
    y = np.array(prices)

    # 색상 결정 (상승: 초록, 하락: 빨강)
    if prices[-1] >= prices[0]:
        line_color = '#34C759'
        fill_color = '#34C759'
    else:
        line_color = '#FF3B30'
        fill_color = '#FF3B30'

    # 곡선 보간 (Cubic spline 느낌)
    if len(x) >= 3:
        from scipy.interpolate import PchipInterpolator
        x_smooth = np.linspace(x.min(), x.max(), 200)
        pchip = PchipInterpolator(x, y)
        y_smooth = pchip(x_smooth)
    else:
        x_smooth = x
        y_smooth = y

    # Y축 범위 계산
    y_min = min(prices)
    y_max = max(prices)
    y_padding = (y_max - y_min) * 0.15 if y_max != y_min else y_max * 0.1
    baseline = y_min - y_padding

    # 그라데이션 영역 채우기
    ax.fill_between(x_smooth, y_smooth, baseline, alpha=0.15, color=fill_color)

    # 부드러운 곡선 그리기
    ax.plot(x_smooth, y_smooth, color=line_color, linewidth=2.5, solid_capstyle='round')

    # 마지막 포인트에 점 표시
    ax.scatter([x[-1]], [prices[-1]], color=line_color, s=40, zorder=5)

    # 테두리 제거
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

    # X축 설정 (실제 데이터 포인트 위치에만 라벨)
    ax.set_xticks(x)
    ax.set_xticklabels([d[5:] for d in dates], fontsize=9, color='#8E8E93')
    ax.tick_params(axis='x', length=0, pad=8)

    # Y축 설정
    ax.set_ylim(baseline, y_max + y_padding)
    ax.yaxis.set_major_formatter(FuncFormatter(_format_price))
    ax.tick_params(axis='y', length=0, labelsize=9, colors='#8E8E93', pad=8)

    # Y축 그리드 제거 (깔끔하게)
    ax.yaxis.grid(False)
    ax.xaxis.grid(False)

    # 여백 조정
    plt.tight_layout()
    plt.subplots_adjust(left=0.12, right=0.95, top=0.95, bottom=0.15)

    # base64 변환
    buffer = BytesIO()
    plt.savefig(buffer, format='png', dpi=120, facecolor='white', edgecolor='none')
    plt.close()

    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()

    return image_base64