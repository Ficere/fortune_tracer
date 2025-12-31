"""紫微斗数可视化图表"""
import plotly.graph_objects as go
from src.models.ziwei_models import ZiweiChart, PalaceInfo


# 十二宫位布局坐标（4x4方格，中间空）
# 布局：    巳  午  未  申
#          辰  --  --  酉
#          卯  --  --  戌
#          寅  丑  子  亥
PALACE_LAYOUT = {
    0: (3, 0),   # 子
    1: (2, 0),   # 丑
    2: (0, 0),   # 寅
    3: (0, 1),   # 卯
    4: (0, 2),   # 辰
    5: (0, 3),   # 巳
    6: (1, 3),   # 午
    7: (2, 3),   # 未
    8: (3, 3),   # 申
    9: (3, 2),   # 酉
    10: (3, 1),  # 戌
    11: (1, 0),  # 亥
}


def create_ziwei_chart(chart: ZiweiChart, show_detail: bool = True) -> go.Figure:
    """创建紫微星盘图
    
    Args:
        chart: 紫微星盘数据
        show_detail: 是否显示详细星曜
    """
    fig = go.Figure()
    
    # 绘制宫位格子
    for palace in chart.palaces:
        pos = palace.position
        x, y = PALACE_LAYOUT.get(pos, (0, 0))
        _draw_palace_box(fig, palace, x, y, chart.ming_gong_pos, show_detail)
    
    # 绘制中央信息
    _draw_center_info(fig, chart)
    
    # 设置布局
    fig.update_layout(
        title=dict(
            text="紫微斗数命盘",
            x=0.5,
            font=dict(size=20)
        ),
        showlegend=False,
        width=700,
        height=700,
        xaxis=dict(range=[-0.5, 4.5], showgrid=False, zeroline=False, visible=False),
        yaxis=dict(range=[-0.5, 4.5], showgrid=False, zeroline=False, visible=False),
        plot_bgcolor="white",
        margin=dict(l=20, r=20, t=60, b=20),
    )
    
    return fig


def _draw_palace_box(
    fig: go.Figure, palace: PalaceInfo, x: int, y: int, 
    ming_pos: int, show_detail: bool
):
    """绘制单个宫位格子"""
    # 命宫用特殊颜色
    is_ming = palace.position == ming_pos
    fill_color = "rgba(255, 215, 0, 0.2)" if is_ming else "rgba(200, 200, 200, 0.1)"
    border_color = "gold" if is_ming else "gray"
    
    # 绘制方框
    fig.add_shape(
        type="rect",
        x0=x, y0=y, x1=x+1, y1=y+1,
        line=dict(color=border_color, width=2),
        fillcolor=fill_color,
    )
    
    # 宫位名称和地支
    header = f"{palace.tiangan}{palace.dizhi} {palace.palace.value}"
    fig.add_annotation(
        x=x+0.5, y=y+0.9,
        text=header,
        showarrow=False,
        font=dict(size=10, color="darkblue"),
    )
    
    if show_detail:
        # 主星
        main_names = [f"<b>{s.name}</b>{s.sihua}" for s in palace.main_stars]
        if main_names:
            fig.add_annotation(
                x=x+0.5, y=y+0.65,
                text=" ".join(main_names),
                showarrow=False,
                font=dict(size=9, color="darkred"),
            )
        
        # 辅星
        aux_names = [s.name for s in palace.aux_stars]
        if aux_names:
            fig.add_annotation(
                x=x+0.5, y=y+0.4,
                text=" ".join(aux_names[:3]),
                showarrow=False,
                font=dict(size=8, color="darkgreen"),
            )
        
        # 煞星
        sha_names = [s.name for s in palace.sha_stars]
        if sha_names:
            fig.add_annotation(
                x=x+0.5, y=y+0.2,
                text=" ".join(sha_names),
                showarrow=False,
                font=dict(size=8, color="purple"),
            )


def _draw_center_info(fig: go.Figure, chart: ZiweiChart):
    """绘制中央命盘信息"""
    # 中央区域
    fig.add_shape(
        type="rect",
        x0=1, y0=1, x1=3, y1=3,
        line=dict(color="black", width=1),
        fillcolor="rgba(255,255,255,0.9)",
    )
    
    # 命盘基本信息
    info_lines = [
        f"农历 {chart.lunar_year}年{chart.lunar_month}月{chart.lunar_day}日",
        f"时辰：{chart.hour_zhi}时",
        f"性别：{chart.gender}",
        f"五行局：{chart.wuxing_ju.value}",
    ]
    
    # 四化信息
    if chart.sihua_stars:
        sihua_text = "  ".join([f"{k}:{v}" for k, v in chart.sihua_stars.items()])
        info_lines.append(f"四化：{sihua_text}")
    
    for i, line in enumerate(info_lines):
        fig.add_annotation(
            x=2, y=2.5 - i * 0.35,
            text=line,
            showarrow=False,
            font=dict(size=10),
        )


def create_palace_summary_chart(chart: ZiweiChart) -> go.Figure:
    """创建宫位摘要雷达图"""
    # 计算每个宫位的星曜得分
    palace_names = [p.palace.value for p in chart.palaces]
    scores = []
    
    for palace in chart.palaces:
        score = 60  # 基础分
        score += len(palace.main_stars) * 10
        score += len(palace.aux_stars) * 5
        score -= len(palace.sha_stars) * 8
        scores.append(max(30, min(100, score)))
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=scores + [scores[0]],
        theta=palace_names + [palace_names[0]],
        fill="toself",
        name="宫位评分",
        fillcolor="rgba(138, 43, 226, 0.3)",
        line=dict(color="purple"),
    ))
    
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=False,
        title="十二宫位评分",
        height=400,
    )
    
    return fig

