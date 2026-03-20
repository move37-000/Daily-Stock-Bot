import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import os
import platform

# 한글 폰트 설정
if platform.system() == 'Windows':
    plt.rcParams['font.family'] = 'Malgun Gothic'
elif platform.system() == 'Darwin':
    plt.rcParams['font.family'] = 'AppleGothic'
else:
    plt.rcParams['font.family'] = 'NanumGothic'

plt.rcParams['axes.unicode_minus'] = False


def generate_weekly_chart(symbol, history, save_dir="reports/charts"):
    """주간 차트 이미지 생성"""
    os.makedirs(save_dir, exist_ok=True)

    # 데이터 준비 (날짜순 정렬)
    dates = [h['date'] for h in reversed(history)]  # 문자열로 유지
    prices = [h['close'] for h in reversed(history)]

    # 그래프 생성
    fig, ax = plt.subplots(figsize=(8, 4))

    # x축을 인덱스로 사용 (날짜 간격 무시)
    x = range(len(dates))
    ax.plot(x, prices, marker='o', linewidth=2, markersize=6, color='#2563eb')

    # 시작점 대비 상승/하락 색상 영역
    if prices[-1] >= prices[0]:
        ax.fill_between(x, prices, prices[0], alpha=0.3, color='#22c55e')
    else:
        ax.fill_between(x, prices, prices[0], alpha=0.3, color='#ef4444')

    # 레이블
    ax.set_title(f"{symbol} 주간 추이", fontsize=14, fontweight='bold')
    ax.set_xlabel("")
    ax.set_ylabel("종가", fontsize=10)

    # x축 라벨을 날짜 문자열로 설정
    ax.set_xticks(x)
    ax.set_xticklabels([d[5:] for d in dates])  # "2026-03-17" → "03-17"

    # 가격 표시
    for i, price in enumerate(prices):
        ax.annotate(f'{price:,.0f}', (i, price), textcoords="offset points",
                    xytext=(0, 10), ha='center', fontsize=8)

    plt.tight_layout()

    # 저장
    filepath = f"{save_dir}/{symbol}_weekly.png"
    plt.savefig(filepath, dpi=100, bbox_inches='tight')
    plt.close()

    return filepath