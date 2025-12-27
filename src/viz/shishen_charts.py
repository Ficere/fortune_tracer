"""十神可视化图表"""
import plotly.graph_objects as go
from src.models.bazi_models import ShiShenAnalysis


# 十神颜色（按类别）
SHISHEN_COLORS = {
    "比肩": "#6366f1",  # 紫色系 - 同我
    "劫财": "#8b5cf6",
    "偏印": "#22c55e",  # 绿色系 - 生我
    "正印": "#16a34a",
    "食神": "#f59e0b",  # 黄色系 - 我生
    "伤官": "#eab308",
    "七杀": "#ef4444",  # 红色系 - 克我
    "正官": "#dc2626",
    "偏财": "#3b82f6",  # 蓝色系 - 我克
    "正财": "#2563eb",
    "日主": "#1e293b",  # 黑色
}

# 十神类别
SHISHEN_CATEGORIES = {
    "比劫": ["比肩", "劫财"],
    "印星": ["偏印", "正印"],
    "食伤": ["食神", "伤官"],
    "官杀": ["七杀", "正官"],
    "财星": ["偏财", "正财"],
}


def create_shishen_radar(shishen: ShiShenAnalysis) -> go.Figure:
    """创建十神雷达图"""
    # 按类别统计
    category_counts = {}
    for cat, items in SHISHEN_CATEGORIES.items():
        total = sum(shishen.shishen_count.get(item, 0) for item in items)
        category_counts[cat] = total
    
    categories = list(category_counts.keys())
    values = list(category_counts.values())
    
    # 闭合图形
    categories.append(categories[0])
    values.append(values[0])
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='十神分布',
        line_color='#8b5cf6',
        fillcolor='rgba(139, 92, 246, 0.3)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, max(values) * 1.2 + 1]),
            bgcolor='rgba(0,0,0,0)'
        ),
        showlegend=False,
        title=dict(text="十神能量分布", x=0.5),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=350
    )
    
    return fig


def create_shishen_bar(shishen: ShiShenAnalysis) -> go.Figure:
    """创建十神柱状图"""
    # 过滤掉日主
    items = [
        (name, count) for name, count in shishen.shishen_count.items()
        if name != "日主" and count > 0
    ]
    
    if not items:
        items = [("无", 0)]
    
    items.sort(key=lambda x: x[1], reverse=True)
    names, counts = zip(*items)
    colors = [SHISHEN_COLORS.get(n, "#6366f1") for n in names]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=names,
        y=counts,
        marker_color=colors,
        text=[f"{c:.1f}" for c in counts],
        textposition='auto',
        hovertemplate="<b>%{x}</b><br>力量: %{y:.1f}<extra></extra>"
    ))
    
    fig.update_layout(
        title=dict(text="十神力量分布", x=0.5),
        xaxis_title="",
        yaxis_title="力量值",
        height=300,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig


def create_shishen_sunburst(shishen: ShiShenAnalysis) -> go.Figure:
    """创建十神旭日图"""
    labels = ["十神"]
    parents = [""]
    values = [1]
    colors = ["#f1f5f9"]
    
    # 添加类别
    for cat, items in SHISHEN_CATEGORIES.items():
        cat_total = sum(shishen.shishen_count.get(item, 0) for item in items)
        if cat_total > 0:
            labels.append(cat)
            parents.append("十神")
            values.append(cat_total)
            colors.append("#e2e8f0")
            
            # 添加具体十神
            for item in items:
                count = shishen.shishen_count.get(item, 0)
                if count > 0:
                    labels.append(item)
                    parents.append(cat)
                    values.append(count)
                    colors.append(SHISHEN_COLORS.get(item, "#6366f1"))
    
    fig = go.Figure(go.Sunburst(
        labels=labels,
        parents=parents,
        values=values,
        marker=dict(colors=colors),
        branchvalues="total",
        hovertemplate="<b>%{label}</b><br>力量: %{value:.1f}<extra></extra>"
    ))
    
    fig.update_layout(
        title=dict(text=f"十神结构 - {shishen.pattern}", x=0.5),
        height=400,
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig
