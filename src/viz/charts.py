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
    """创建人生K线图（0-90岁），K线形态与运势评级匹配"""
    from .kline_generator import generate_kline_data

    # 使用专门的K线生成器确保评级与形态匹配
    klines = generate_kline_data(fortunes)

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
        hovertemplate='%{text}<br>运势: %{close:.0f}<extra></extra>'
    ))

    # 添加10年均线
    import pandas as pd
    scores = [k.score for k in klines]
    ma10 = pd.Series(scores).rolling(window=10, min_periods=1).mean()
    fig.add_trace(go.Scatter(
        x=years, y=ma10, mode='lines',
        name='10年均线', line=dict(color='#f59e0b', width=2)
    ))

    fig.update_layout(
        title=dict(text="人生运势K线图（0-90岁）", x=0.5),
        xaxis_title="年份（年龄）", yaxis_title="运势指数",
        yaxis=dict(range=[20, 100]),
        xaxis=dict(rangeslider=dict(visible=True, thickness=0.05)),
        height=500, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
    )
    return fig


def create_year_fortune_line(fortunes: list[YearFortune]) -> go.Figure:
    """创建流年运势趋势图（0-90岁），增强hover详细信息"""
    years = [f.year for f in fortunes]
    scores = [f.score for f in fortunes]

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
    fig.add_trace(go.Scatter(
        x=years, y=scores, mode='lines',
        name='流年运势', line=dict(color='#8b5cf6', width=2),
        fill='tozeroy', fillcolor='rgba(139, 92, 246, 0.2)',
        text=hover_texts, hovertemplate='%{text}<br>运势: %{y:.0f}<extra></extra>'
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
        height=400, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
    )
    return fig

