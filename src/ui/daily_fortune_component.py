"""每日运势UI组件"""
import streamlit as st
from datetime import date
from src.core.fortune.daily_fortune import DailyFortune


def render_daily_fortune_panel(fortunes: list[DailyFortune]):
    """渲染每日运势面板（今日、明日、后日）"""
    if not fortunes:
        return
    
    st.markdown("### 📅 每日运势")
    
    # 三天运势卡片
    cols = st.columns(3)
    day_labels = ["今日", "明日", "后日"]
    
    for idx, (col, fortune) in enumerate(zip(cols, fortunes[:3])):
        with col:
            _render_day_card(fortune, day_labels[idx])


def _render_day_card(fortune: DailyFortune, label: str):
    """渲染单日运势卡片"""
    bg_color = _get_bg_color(fortune.level)
    
    st.markdown(f"""
    <div style='background:{bg_color};padding:12px;border-radius:10px;
        border:1px solid #e2e8f0;margin-bottom:10px'>
        <div style='display:flex;justify-content:space-between;align-items:center'>
            <span style='font-weight:bold;font-size:14px'>{label}</span>
            <span style='font-size:12px;color:#64748b'>
                {fortune.date.strftime('%m/%d')} {fortune.ganzhi}
            </span>
        </div>
        <div style='text-align:center;margin:8px 0'>
            <span style='font-size:32px'>{fortune.emoji}</span>
            <div style='font-size:18px;font-weight:bold;margin-top:4px'>
                {fortune.level}
            </div>
            <div style='font-size:24px;color:#6366f1;font-weight:bold'>
                {fortune.score:.0f}分
            </div>
        </div>
        <div style='font-size:12px;color:#475569;text-align:center;margin-bottom:8px'>
            {fortune.summary}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 宜忌和建议
    with st.expander("查看详情", expanded=(label == "今日")):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**✅ 宜**")
            for item in fortune.suitable[:3]:
                st.caption(f"• {item}")
        with col2:
            st.markdown("**❌ 忌**")
            for item in fortune.unsuitable[:3]:
                st.caption(f"• {item}")
        
        st.markdown("**💡 增运建议**")
        for tip in fortune.tips[:2]:
            st.caption(f"• {tip}")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.caption(f"🧭 吉方: {fortune.lucky_direction}")
        with col2:
            st.caption(f"🎨 幸运色: {fortune.lucky_color}")
        with col3:
            st.caption(f"🏥 {fortune.health_tip[:8]}...")


def _get_bg_color(level: str) -> str:
    """获取背景色"""
    colors = {
        "大吉": "linear-gradient(135deg, #dcfce7, #bbf7d0)",
        "吉": "linear-gradient(135deg, #d1fae5, #a7f3d0)",
        "小吉": "linear-gradient(135deg, #ecfdf5, #d1fae5)",
        "平": "linear-gradient(135deg, #fefce8, #fef9c3)",
        "小凶": "linear-gradient(135deg, #fff7ed, #fed7aa)",
        "凶": "linear-gradient(135deg, #fef2f2, #fecaca)",
        "大凶": "linear-gradient(135deg, #fee2e2, #fca5a5)"
    }
    return colors.get(level, "#f8fafc")


def render_daily_fortune_mini(fortune: DailyFortune):
    """渲染迷你版今日运势（侧边栏用）"""
    st.markdown(f"""
    <div style='background:#f1f5f9;padding:8px;border-radius:8px;text-align:center'>
        <div style='font-size:10px;color:#64748b'>今日运势 {fortune.ganzhi}</div>
        <div style='font-size:24px'>{fortune.emoji}</div>
        <div style='font-size:14px;font-weight:bold'>{fortune.level} {fortune.score:.0f}分</div>
        <div style='font-size:10px;color:#475569'>{fortune.summary[:15]}...</div>
    </div>
    """, unsafe_allow_html=True)

