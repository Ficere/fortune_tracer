"""大运可视化图表"""
import plotly.graph_objects as go
from src.models.bazi_models import DaYunInfo, WuxingAnalysis


# 五行颜色
WUXING_COLORS = {
    "木": "#22c55e",
    "火": "#ef4444",
    "土": "#f59e0b",
    "金": "#94a3b8",
    "水": "#3b82f6",
}


def create_dayun_timeline(dayun_info: DaYunInfo, current_age: int = 0) -> go.Figure:
    """创建大运时间线图"""
    fig = go.Figure()
    
    for i, dy in enumerate(dayun_info.dayun_list):
        color = WUXING_COLORS.get(dy.wuxing, "#6366f1")
        is_current = dy.start_age <= current_age <= dy.end_age
        
        # 大运条
        fig.add_trace(go.Bar(
            x=[10],
            y=[dy.ganzhi],
            orientation='h',
            marker=dict(
                color=color,
                opacity=1.0 if is_current else 0.6,
                line=dict(color='#1e293b', width=2 if is_current else 0)
            ),
            text=f"{dy.start_age}-{dy.end_age}岁 ({dy.start_year}-{dy.end_year})",
            textposition='inside',
            textfont=dict(color='white', size=12),
            hovertemplate=(
                f"<b>{dy.ganzhi}</b><br>"
                f"五行: {dy.wuxing}<br>"
                f"年龄: {dy.start_age}-{dy.end_age}岁<br>"
                f"年份: {dy.start_year}-{dy.end_year}<extra></extra>"
            ),
            showlegend=False
        ))
    
    fig.update_layout(
        title=dict(
            text=f"大运排盘 ({dayun_info.direction})",
            x=0.5
        ),
        xaxis=dict(visible=False),
        yaxis=dict(
            title="",
            autorange="reversed"
        ),
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=60, r=20, t=50, b=20)
    )
    
    return fig


def create_dayun_fortune_chart(
    dayun_info: DaYunInfo,
    wuxing: WuxingAnalysis
) -> go.Figure:
    """创建大运运势走势图"""
    ages = []
    scores = []
    labels = []
    colors = []
    
    favorable_wx = [w.value for w in wuxing.favorable]
    
    for dy in dayun_info.dayun_list:
        mid_age = (dy.start_age + dy.end_age) // 2
        ages.append(mid_age)
        
        # 根据大运五行与喜用神关系计算分数
        base_score = 70
        if dy.wuxing in favorable_wx:
            base_score += 15
        else:
            base_score -= 10
        
        # 添加一些变化
        base_score += (hash(dy.ganzhi) % 15) - 7
        scores.append(max(40, min(95, base_score)))
        labels.append(dy.ganzhi)
        colors.append(WUXING_COLORS.get(dy.wuxing, "#6366f1"))
    
    fig = go.Figure()
    
    # 运势折线
    fig.add_trace(go.Scatter(
        x=ages,
        y=scores,
        mode='lines+markers+text',
        line=dict(color='#8b5cf6', width=3),
        marker=dict(size=12, color=colors, line=dict(color='white', width=2)),
        text=labels,
        textposition='top center',
        textfont=dict(size=10),
        hovertemplate="<b>%{text}</b><br>年龄: %{x}岁<br>运势: %{y}<extra></extra>"
    ))
    
    # 平均线
    avg_score = sum(scores) / len(scores)
    fig.add_hline(
        y=avg_score, line_dash="dash", line_color="#94a3b8",
        annotation_text=f"平均: {avg_score:.0f}"
    )
    
    fig.update_layout(
        title=dict(text="大运运势走势", x=0.5),
        xaxis_title="年龄",
        yaxis_title="运势指数",
        yaxis=dict(range=[30, 100]),
        height=350,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig
