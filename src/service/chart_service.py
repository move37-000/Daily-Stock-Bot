import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import os
import platform

# 한글 폰트 설정 (import 직후, 함수 밖에서 설정)
if platform.system() == 'Windows':
    plt.rcParams['font.family'] = 'Malgun Gothic'
elif platform.system() == 'Darwin':  # Mac
    plt.rcParams['font.family'] = 'AppleGothic'
else:  # Linux
    plt.rcParams['font.family'] = 'NanumGothic'

plt.rcParams['axes.unicode_minus'] = False


def generate_weekly_chart(symbol, history, save_dir="reports/charts"):
    """주간 차트 이미지 생성"""
    os.makedirs(save_dir, exist_ok=True)

    # 데이터 준비
    dates = [datetime.strptime(h['date'], "%Y-%m-%d") for h in reversed(history)]
    prices = [h['close'] for h in reversed(history)]

    # 그래프 생성
    fig, ax = plt.subplots(figsize=(8, 4))

    # 라인 차트
    ax.plot(dates, prices, marker='o', linewidth=2, markersize=6, color='#2563eb')

    # 시작점 대비 상승/하락 색상 영역
    if prices[-1] >= prices[0]:
        ax.fill_between(dates, prices, prices[0], alpha=0.3, color='#22c55e')
    else:
        ax.fill_between(dates, prices, prices[0], alpha=0.3, color='#ef4444')

    # 레이블
    ax.set_title(f"{symbol} 주간 추이", fontsize=14, fontweight='bold')
    ax.set_xlabel("")
    ax.set_ylabel("종가", fontsize=10)

    # x축 날짜 포맷
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
    ax.xaxis.set_major_locator(mdates.DayLocator())

    # 가격 표시
    for i, (date, price) in enumerate(zip(dates, prices)):
        ax.annotate(f'{price:,.0f}', (date, price), textcoords="offset points",
                    xytext=(0, 10), ha='center', fontsize=8)

    plt.tight_layout()

    # 저장
    filepath = f"{save_dir}/{symbol}_weekly.png"
    plt.savefig(filepath, dpi=100, bbox_inches='tight')
    plt.close()

    return filepath