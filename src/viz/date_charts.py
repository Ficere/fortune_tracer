"""择日可视化图表"""
import plotly.graph_objects as go
from src.models.date_selection_models import DateRecommendation, DayQuality


# 质量对应颜色
QUALITY_COLORS = {
    DayQuality.EXCELLENT: "#22c55e",
    DayQuality.GOOD: "#86efac",
    DayQuality.NEUTRAL: "#fbbf24",
    DayQuality.BAD: "#f87171",
    DayQuality.TERRIBLE: "#dc2626",
}


def create_date_calendar(result: DateRecommendation) -> go.Figure:
    """创建日期日历热力图"""
    all_days = result.recommended_dates + result.avoid_dates
    all_days.sort(key=lambda x: x.date)
    
    if not all_days:
        fig = go.Figure()
        fig.add_annotation(text="暂无数据", x=0.5, y=0.5, showarrow=False)
        return fig
    
    dates = [d.date.strftime("%m/%d") for d in all_days]
    scores = [d.score for d in all_days]
    ganzhis = [d.ganzhi for d in all_days]
    qualities = [d.quality.value for d in all_days]
    colors = [QUALITY_COLORS[d.quality] for d in all_days]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=dates,
        y=scores,
        marker_color=colors,
        text=[f"{gz}<br>{q}" for gz, q in zip(ganzhis, qualities)],
        textposition='outside',
        hovertemplate='%{x}<br>得分: %{y}<br>%{text}<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(text=f"{result.event_type.value} 吉日分布", x=0.5),
        xaxis_title="日期",
        yaxis_title="吉凶得分",
        yaxis=dict(range=[0, 100]),
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    # 添加基准线
    fig.add_hline(y=70, line_dash="dash", line_color="#22c55e",
                  annotation_text="吉日线")
    fig.add_hline(y=50, line_dash="dash", line_color="#fbbf24",
                  annotation_text="平日线")
    
    return fig


def create_date_timeline(result: DateRecommendation) -> go.Figure:
    """创建推荐日期时间线"""
    recommended = result.recommended_dates[:8]
    
    if not recommended:
        fig = go.Figure()
        fig.add_annotation(text="暂无推荐日期", x=0.5, y=0.5, showarrow=False)
        return fig
    
    fig = go.Figure()
    
    for i, day in enumerate(recommended):
        color = QUALITY_COLORS[day.quality]
        fig.add_trace(go.Scatter(
            x=[day.date],
            y=[day.score],
            mode='markers+text',
            marker=dict(size=30, color=color, symbol='diamond'),
            text=[f"{day.ganzhi}<br>{day.quality.value}"],
            textposition='top center',
            name=day.date.strftime("%m/%d"),
            hovertemplate=(
                f"日期: {day.date.strftime('%Y-%m-%d')}<br>"
                f"干支: {day.ganzhi}<br>"
                f"得分: {day.score}<br>"
                f"宜: {', '.join(day.suitable[:3])}<br>"
                f"忌: {', '.join(day.avoid[:2])}<extra></extra>"
            )
        ))
    
    fig.update_layout(
        title=dict(text="推荐吉日", x=0.5),
        xaxis_title="日期",
        yaxis_title="吉凶得分",
        yaxis=dict(range=[50, 100]),
        showlegend=False,
        height=350,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

