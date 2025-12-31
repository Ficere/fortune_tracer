"""图表可视化模块"""
import plotly.graph_objects as go
from src.models import WuxingAnalysis
from src.models.bazi_models import YearFortune


def create_wuxing_radar(wuxing: WuxingAnalysis) -> go.Figure:
    """创建五行雷达图"""
    counts = wuxing.counts.to_dict()
    categories = list(counts.keys())
    values = list(counts.values())
    values.append(values[0])  # 闭合图形
    categories.append(categories[0])
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='五行分布',
        line_color='#6366f1',
        fillcolor='rgba(99, 102, 241, 0.3)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, max(values) * 1.2]),
            bgcolor='rgba(0,0,0,0)'
        ),
        showlegend=False,
        title=dict(text="五行能量分布", x=0.5),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=400
    )
    
    return fig


def create_fortune_kline(fortunes: list[YearFortune]) -> go.Figure:
    """创建人生K线图（0-90岁），使用乘法模式产生自然复利波动"""
    from .kline_multiplier import generate_multiplier_klines
    import pandas as pd

    # 使用乘法模式K线生成器
    klines = generate_multiplier_klines(fortunes, base_price=100.0)

    years = [k.year for k in klines]
    opens = [k.open for k in klines]
    highs = [k.high for k in klines]
    lows = [k.low for k in klines]
    closes = [k.close for k in klines]
    hover_texts = [k.hover_text for k in klines]

    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=years, open=opens, high=highs, low=lows, close=closes,
        increasing_line_color='#22c55e', decreasing_line_color='#ef4444',
        name='运势K线', text=hover_texts,
        hovertemplate='%{text}<br>运势指数: %{close:.1f}<extra></extra>'
    ))

    # 添加10年均线
    ma10 = pd.Series(closes).rolling(window=10, min_periods=1).mean()
    fig.add_trace(go.Scatter(
        x=years, y=ma10, mode='lines',
        name='10年均线', line=dict(color='#f59e0b', width=2)
    ))

    # 添加基准线（起点100）
    fig.add_hline(y=100, line_dash="dot", line_color="#94a3b8",
                  annotation_text="基准线 100")

    fig.update_layout(
        title=dict(text="人生运势K线图（0-90岁）", x=0.5),
        xaxis_title="年份（年龄）", yaxis_title="运势指数",
        xaxis=dict(rangeslider=dict(visible=True, thickness=0.05)),
        height=500, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
    )
    return fig


def create_year_fortune_line(fortunes: list[YearFortune]) -> go.Figure:
    """创建流年运势柱状图（0-90岁），hover交互更精准"""
    years = [f.year for f in fortunes]
    scores = [f.score for f in fortunes]

    # 根据分数设置颜色
    colors = [_get_bar_color(s) for s in scores]

    # 构建详细hover文本
    hover_texts = []
    for f in fortunes:
        text = f"{f.description}"
        if f.detail:
            text += f"<br>{f.detail.emoji} {f.detail.level}"
            text += f"<br>事业: {f.detail.career}"
            text += f"<br>感情: {f.detail.love}"
        hover_texts.append(text)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=years, y=scores,
        name='流年运势',
        marker_color=colors,
        text=hover_texts,
        hovertemplate='%{text}<br>运势: %{y:.0f}<extra></extra>'
    ))

    # 添加平均线
    avg = sum(scores) / len(scores) if scores else 50
    fig.add_hline(y=avg, line_dash="dash", line_color="#94a3b8",
                  annotation_text=f"平均: {avg:.0f}")

    fig.update_layout(
        title=dict(text="流年运势趋势（0-90岁）", x=0.5),
        xaxis_title="年份（年龄）", yaxis_title="运势指数",
        yaxis=dict(range=[30, 100]),
        xaxis=dict(rangeslider=dict(visible=True, thickness=0.05)),
        height=400, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        bargap=0.1
    )
    return fig


def _get_bar_color(score: float) -> str:
    """根据分数获取柱状图颜色"""
    if score >= 80:
        return '#22c55e'  # 绿色 - 大吉/吉
    elif score >= 65:
        return '#84cc16'  # 浅绿 - 小吉
    elif score >= 55:
        return '#eab308'  # 黄色 - 平
    elif score >= 45:
        return '#f97316'  # 橙色 - 小凶
    else:
        return '#ef4444'  # 红色 - 凶/大凶

