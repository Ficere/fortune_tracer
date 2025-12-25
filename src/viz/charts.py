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
    """创建人生K线图"""
    years = [f.year for f in fortunes]
    scores = [f.score for f in fortunes]
    
    # 生成K线数据（开盘、最高、最低、收盘）
    opens = []
    highs = []
    lows = []
    closes = []
    colors = []
    
    prev_score = scores[0] if scores else 50
    for score in scores:
        open_val = prev_score
        close_val = score
        high_val = max(open_val, close_val) + (hash(str(score)) % 10)
        low_val = min(open_val, close_val) - (hash(str(score * 2)) % 8)
        
        opens.append(open_val)
        closes.append(close_val)
        highs.append(min(high_val, 100))
        lows.append(max(low_val, 20))
        colors.append('#22c55e' if close_val >= open_val else '#ef4444')
        prev_score = score
    
    fig = go.Figure()
    
    fig.add_trace(go.Candlestick(
        x=years,
        open=opens,
        high=highs,
        low=lows,
        close=closes,
        increasing_line_color='#22c55e',
        decreasing_line_color='#ef4444',
        name='运势K线'
    ))
    
    # 添加均线
    import pandas as pd
    df = pd.DataFrame({'score': scores})
    ma3 = df['score'].rolling(window=3, min_periods=1).mean()
    
    fig.add_trace(go.Scatter(
        x=years, y=ma3, mode='lines',
        name='3年均线', line=dict(color='#f59e0b', width=2)
    ))
    
    fig.update_layout(
        title=dict(text="人生运势K线图", x=0.5),
        xaxis_title="年份",
        yaxis_title="运势指数",
        yaxis=dict(range=[20, 100]),
        xaxis_rangeslider_visible=False,
        height=450,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig


def create_year_fortune_line(fortunes: list[YearFortune]) -> go.Figure:
    """创建流年运势趋势图"""
    years = [f.year for f in fortunes]
    scores = [f.score for f in fortunes]
    descriptions = [f.description for f in fortunes]
    
    fig = go.Figure()
    
    # 添加面积图
    fig.add_trace(go.Scatter(
        x=years, y=scores,
        mode='lines+markers',
        name='流年运势',
        line=dict(color='#8b5cf6', width=3),
        marker=dict(size=10, color='#8b5cf6'),
        fill='tozeroy',
        fillcolor='rgba(139, 92, 246, 0.2)',
        text=descriptions,
        hovertemplate='%{text}<br>运势: %{y:.0f}<extra></extra>'
    ))
    
    # 添加平均线
    avg = sum(scores) / len(scores) if scores else 50
    fig.add_hline(y=avg, line_dash="dash", line_color="#94a3b8",
                  annotation_text=f"平均: {avg:.0f}")
    
    fig.update_layout(
        title=dict(text="流年运势趋势", x=0.5),
        xaxis_title="年份",
        yaxis_title="运势指数",
        yaxis=dict(range=[30, 100]),
        height=350,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

