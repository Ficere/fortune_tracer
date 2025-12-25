"""八字宫位图模块"""
import plotly.graph_objects as go
from src.models import BaziChart, WuxingAnalysis
from src.core.constants import TIANGAN_WUXING, DIZHI_WUXING


# 五行颜色映射
WUXING_COLORS = {
    "木": "#22c55e",  # 绿色
    "火": "#ef4444",  # 红色
    "土": "#f59e0b",  # 黄色
    "金": "#f1f5f9",  # 白色
    "水": "#3b82f6",  # 蓝色
}


def create_palace_chart(bazi: BaziChart, wuxing: WuxingAnalysis) -> go.Figure:
    """创建八字宫位图"""
    pillars = [
        ("时柱", bazi.hour_pillar),
        ("日柱", bazi.day_pillar),
        ("月柱", bazi.month_pillar),
        ("年柱", bazi.year_pillar),
    ]
    
    fig = go.Figure()
    
    # 绘制四柱
    for i, (name, pillar) in enumerate(pillars):
        x_center = i * 1.5 + 0.75
        
        gan = pillar.tiangan.value
        zhi = pillar.dizhi.value
        gan_wx = TIANGAN_WUXING[gan]
        zhi_wx = DIZHI_WUXING[zhi]
        
        # 天干方框
        fig.add_shape(
            type="rect",
            x0=x_center - 0.4, y0=1.5, x1=x_center + 0.4, y1=2.3,
            fillcolor=WUXING_COLORS[gan_wx],
            line=dict(color="#334155", width=2),
            opacity=0.8
        )
        
        # 地支方框
        fig.add_shape(
            type="rect",
            x0=x_center - 0.4, y0=0.5, x1=x_center + 0.4, y1=1.3,
            fillcolor=WUXING_COLORS[zhi_wx],
            line=dict(color="#334155", width=2),
            opacity=0.8
        )
        
        # 天干文字
        text_color = "#1e293b" if gan_wx in ["金", "土"] else "#f8fafc"
        fig.add_annotation(
            x=x_center, y=1.9,
            text=f"<b>{gan}</b>",
            font=dict(size=28, color=text_color),
            showarrow=False
        )
        
        # 地支文字
        text_color = "#1e293b" if zhi_wx in ["金", "土"] else "#f8fafc"
        fig.add_annotation(
            x=x_center, y=0.9,
            text=f"<b>{zhi}</b>",
            font=dict(size=28, color=text_color),
            showarrow=False
        )
        
        # 柱名标签
        fig.add_annotation(
            x=x_center, y=2.6,
            text=name,
            font=dict(size=14, color="#64748b"),
            showarrow=False
        )
    
    # 添加日主标记
    fig.add_annotation(
        x=1 * 1.5 + 0.75, y=2.9,
        text="★ 日主",
        font=dict(size=12, color="#8b5cf6"),
        showarrow=False
    )
    
    # 五行图例
    for i, (wx, color) in enumerate(WUXING_COLORS.items()):
        fig.add_shape(
            type="rect",
            x0=i * 0.8 + 1.5, y0=-0.3, x1=i * 0.8 + 1.9, y1=-0.1,
            fillcolor=color,
            line=dict(color="#334155", width=1)
        )
        fig.add_annotation(
            x=i * 0.8 + 1.7, y=-0.5,
            text=wx,
            font=dict(size=10, color="#64748b"),
            showarrow=False
        )
    
    fig.update_layout(
        title=dict(text="八字宫位图", x=0.5),
        xaxis=dict(visible=False, range=[-0.2, 6.5]),
        yaxis=dict(visible=False, range=[-0.8, 3.2]),
        height=380,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=50, b=20)
    )
    
    return fig

