"""每日运势完整版UI组件"""
import streamlit as st
from src.models.daily_fortune_models import DailyFortuneReport, DimensionScore


def render_full_daily_fortune(report: DailyFortuneReport):
    """渲染完整每日运势报告"""
    st.markdown("### 📅 今日运势详解")
    
    # 总体运势区
    _render_total_section(report)
    
    # 七维度详情
    _render_dimensions_section(report)
    
    # 吉时推荐 + 行动指南
    col1, col2 = st.columns([1, 1])
    with col1:
        _render_lucky_hours(report)
    with col2:
        _render_action_guide(report)
    
    # 增运建议
    _render_enhancement_section(report)


def _render_total_section(report: DailyFortuneReport):
    """渲染总体运势区域"""
    bg = _get_level_gradient(report.total_level)
    
    st.markdown(f"""
    <div style='background:{bg};padding:16px;border-radius:12px;margin-bottom:16px'>
        <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:12px'>
            <span style='font-size:14px;color:#64748b'>
                {report.target_date.strftime('%Y年%m月%d日')} | {report.day_ganzhi}日 | 五行属{report.day_wuxing}
            </span>
        </div>
        <div style='display:flex;align-items:center;gap:16px'>
            <div style='font-size:48px'>{report.total_emoji}</div>
            <div>
                <div style='font-size:32px;font-weight:bold;color:#1e293b'>
                    {report.total_score:.0f}分
                </div>
                <div style='font-size:18px;font-weight:bold;color:#475569'>
                    {report.total_level}
                </div>
            </div>
            <div style='flex:1;font-size:14px;color:#475569;padding-left:16px'>
                {report.total_summary}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def _render_dimensions_section(report: DailyFortuneReport):
    """渲染七维度评分区域"""
    st.markdown("#### 📊 分项运势")
    
    dims = [
        ("career", report.career, "💼"),
        ("wealth", report.wealth, "💰"),
        ("love", report.love, "💕"),
        ("health", report.health, "🏥"),
        ("emotion", report.emotion, "🧠"),
        ("family", report.family, "🏠"),
        ("opportunity", report.opportunity, "🌟"),
    ]
    
    # 找出最高和最低
    sorted_dims = sorted(dims, key=lambda x: x[1].score, reverse=True)
    best_key = sorted_dims[0][0]
    worst_key = sorted_dims[-1][0]
    
    # 分两行展示
    for row_dims in [dims[:4], dims[3:]]:
        cols = st.columns(len(row_dims))
        for col, (key, dim, icon) in zip(cols, row_dims):
            with col:
                _render_dimension_card(dim, icon, key == best_key, key == worst_key)


def _render_dimension_card(dim: DimensionScore, icon: str, is_best: bool, is_worst: bool):
    """渲染单个维度卡片"""
    border = "2px solid #10b981" if is_best else ("2px solid #f59e0b" if is_worst else "1px solid #e2e8f0")
    badge = "🔥" if is_best else ("⚠️" if is_worst else "")
    
    st.markdown(f"""
    <div style='background:#f8fafc;padding:10px;border-radius:8px;border:{border};text-align:center'>
        <div style='font-size:10px;color:#64748b'>{badge} {dim.name}</div>
        <div style='font-size:20px'>{icon}</div>
        <div style='font-size:18px;font-weight:bold;color:#1e293b'>{int(dim.score)}分</div>
        <div style='font-size:11px;color:#64748b'>{dim.level}</div>
    </div>
    """, unsafe_allow_html=True)
    
    with st.expander("详情", expanded=False):
        if dim.factors:
            st.caption("**成因:**")
            for f in dim.factors[:2]:
                st.caption(f"• {f}")
        st.caption("**建议:**")
        for a in dim.advice[:2]:
            st.caption(f"• {a}")


def _render_lucky_hours(report: DailyFortuneReport):
    """渲染吉时推荐"""
    st.markdown("#### 🕐 吉时推荐")
    for h in report.lucky_hours:
        st.markdown(f"""
        <div style='background:#ecfdf5;padding:8px;border-radius:6px;margin-bottom:6px'>
            <span style='font-weight:bold'>{h.hour_name}</span>
            <span style='color:#64748b;font-size:12px'>({h.time_range})</span>
            <span style='float:right;font-weight:bold;color:#059669'>{h.score:.0f}分</span>
            <div style='font-size:11px;color:#475569'>适宜: {', '.join(h.suitable[:3])}</div>
        </div>
        """, unsafe_allow_html=True)


def _render_action_guide(report: DailyFortuneReport):
    """渲染行动指南"""
    st.markdown("#### 📋 今日指南")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**✅ 宜**")
        for item in report.suitable_actions[:4]:
            st.caption(f"• {item}")
    with col2:
        st.markdown("**❌ 忌**")
        for item in report.unsuitable_actions[:4]:
            st.caption(f"• {item}")


def _render_enhancement_section(report: DailyFortuneReport):
    """渲染增运建议"""
    st.markdown("#### ✨ 增运贴士")
    cols = st.columns(4)
    info = [
        ("🧭 吉方", report.lucky_direction),
        ("🎨 幸运色", report.lucky_color),
        ("🔢 幸运数", report.lucky_number),
        ("💡 建议", report.enhancement_tips[0][:10] + "..." if report.enhancement_tips else "保持乐观"),
    ]
    for col, (label, value) in zip(cols, info):
        with col:
            st.metric(label, value)


def _get_level_gradient(level: str) -> str:
    """获取等级渐变背景"""
    gradients = {
        "大吉主动": "linear-gradient(135deg, #dcfce7, #bbf7d0)",
        "良好推进": "linear-gradient(135deg, #d1fae5, #a7f3d0)",
        "平稳保守": "linear-gradient(135deg, #fefce8, #fef9c3)",
        "谨慎观望": "linear-gradient(135deg, #fff7ed, #fed7aa)",
        "小心应对": "linear-gradient(135deg, #fef2f2, #fecaca)",
        "暂避锋芒": "linear-gradient(135deg, #fee2e2, #fca5a5)",
    }
    return gradients.get(level, "#f8fafc")

