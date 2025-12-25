"""配对分析可视化图表"""
import plotly.graph_objects as go
from src.models import WuxingAnalysis
from src.models.compatibility_models import CompatibilityResult


def create_compatibility_gauge(score: int, grade: str) -> go.Figure:
    """创建配对得分仪表盘"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={"text": f"配对指数<br><span style='font-size:0.8em'>{grade}</span>"},
        gauge={
            "axis": {"range": [0, 100], "tickwidth": 1},
            "bar": {"color": "#8b5cf6"},
            "bgcolor": "white",
            "steps": [
                {"range": [0, 50], "color": "#fecaca"},
                {"range": [50, 70], "color": "#fef08a"},
                {"range": [70, 85], "color": "#bbf7d0"},
                {"range": [85, 100], "color": "#86efac"},
            ],
            "threshold": {
                "line": {"color": "#ef4444", "width": 4},
                "thickness": 0.75,
                "value": 60
            }
        }
    ))
    
    fig.update_layout(
        height=280,
        paper_bgcolor='rgba(0,0,0,0)',
        font={"color": "#334155", "size": 14}
    )
    return fig


def create_wuxing_comparison(wx1: WuxingAnalysis, wx2: WuxingAnalysis) -> go.Figure:
    """创建双人五行对比雷达图"""
    categories = ["木", "火", "土", "金", "水", "木"]
    
    c1 = wx1.counts.to_dict()
    c2 = wx2.counts.to_dict()
    values1 = [c1["木"], c1["火"], c1["土"], c1["金"], c1["水"], c1["木"]]
    values2 = [c2["木"], c2["火"], c2["土"], c2["金"], c2["水"], c2["木"]]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values1, theta=categories, fill='toself',
        name='本人', line_color='#6366f1',
        fillcolor='rgba(99, 102, 241, 0.3)'
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=values2, theta=categories, fill='toself',
        name='对方', line_color='#ec4899',
        fillcolor='rgba(236, 72, 153, 0.3)'
    ))
    
    max_val = max(max(values1), max(values2))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, max_val * 1.2])),
        showlegend=True,
        title=dict(text="五行能量对比", x=0.5),
        height=380,
        paper_bgcolor='rgba(0,0,0,0)'
    )
    return fig


def create_relations_sunburst(result: CompatibilityResult) -> go.Figure:
    """创建干支关系旭日图"""
    labels = ["关系总览"]
    parents = [""]
    values = [1]
    colors = ["#f1f5f9"]
    
    gz = result.ganzhi_relations
    
    # 添加正面关系
    if gz.tiangan_he or gz.dizhi_he:
        labels.append("相合")
        parents.append("关系总览")
        values.append(len(gz.tiangan_he) + len(gz.dizhi_he))
        colors.append("#22c55e")
        
        for rel in gz.tiangan_he:
            labels.append(f"{rel.elements[0]}合{rel.elements[1]}")
            parents.append("相合")
            values.append(1)
            colors.append("#86efac")
        
        for rel in gz.dizhi_he:
            labels.append(f"{rel.elements[0]}合{rel.elements[1]}")
            parents.append("相合")
            values.append(1)
            colors.append("#86efac")
    
    # 添加负面关系
    if gz.tiangan_chong or gz.dizhi_chong or gz.dizhi_xing:
        labels.append("相冲刑")
        parents.append("关系总览")
        values.append(len(gz.tiangan_chong) + len(gz.dizhi_chong) + len(gz.dizhi_xing))
        colors.append("#ef4444")
        
        for rel in gz.dizhi_chong:
            labels.append(f"{rel.elements[0]}冲{rel.elements[1]}")
            parents.append("相冲刑")
            values.append(1)
            colors.append("#fca5a5")
    
    if len(labels) == 1:
        labels.extend(["平和", "无明显关系"])
        parents.extend(["关系总览", "平和"])
        values.extend([1, 1])
        colors.extend(["#94a3b8", "#cbd5e1"])
    
    fig = go.Figure(go.Sunburst(
        labels=labels, parents=parents, values=values,
        marker=dict(colors=colors),
        branchvalues="total"
    ))
    
    fig.update_layout(
        title=dict(text="干支关系图", x=0.5),
        height=350,
        paper_bgcolor='rgba(0,0,0,0)'
    )
    return fig

