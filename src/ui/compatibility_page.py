"""配对分析页面"""
import streamlit as st
from datetime import datetime
from src.core import (
    calculate_bazi, analyze_wuxing, calculate_compatibility,
    analyze_shishen, convert_to_true_solar_time
)
from src.models.bazi_models import Gender
from src.viz import (
    create_compatibility_gauge,
    create_wuxing_comparison,
    create_relations_sunburst
)
from src.ai import get_or_create_session
from .common import render_pillar_display
from .chat_component import render_chat_section


def render_compatibility_analysis(info1: dict, info2: dict, api_key: str | None = None):
    """渲染配对分析结果"""
    # 计算双方八字（支持真太阳时）
    dt1 = datetime.combine(info1["date"], info1["time"])
    dt2 = datetime.combine(info2["date"], info2["time"])
    
    place1, place2 = info1["place"] or None, info2["place"] or None
    if place1:
        dt1 = convert_to_true_solar_time(dt1, place1)
    if place2:
        dt2 = convert_to_true_solar_time(dt2, place2)
    
    gender1 = Gender.MALE if info1["gender"] == "男" else Gender.FEMALE
    gender2 = Gender.MALE if info2["gender"] == "男" else Gender.FEMALE
    
    with st.spinner("正在分析配对..."):
        bazi1 = calculate_bazi(dt1, gender1, place1)
        bazi2 = calculate_bazi(dt2, gender2, place2)
        wuxing1 = analyze_wuxing(bazi1)
        wuxing2 = analyze_wuxing(bazi2)
        shishen1 = analyze_shishen(bazi1)
        shishen2 = analyze_shishen(bazi2)
        result = calculate_compatibility(bazi1, bazi2, wuxing1, wuxing2)
    
    # 配对得分
    st.subheader("💑 配对结果")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.plotly_chart(
            create_compatibility_gauge(result.total_score, result.grade),
            width="stretch"
        )
    
    # 双方八字对比
    st.subheader("📜 八字对比")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("##### 本人八字")
        pillars1 = [bazi1.year_pillar, bazi1.month_pillar, bazi1.day_pillar, bazi1.hour_pillar]
        _render_mini_pillars(pillars1)
        st.caption(f"格局: **{shishen1.pattern}** | 日主: {wuxing1.day_master.value}({wuxing1.day_master_strength})")
    with col2:
        st.markdown("##### 对方八字")
        pillars2 = [bazi2.year_pillar, bazi2.month_pillar, bazi2.day_pillar, bazi2.hour_pillar]
        _render_mini_pillars(pillars2)
        st.caption(f"格局: **{shishen2.pattern}** | 日主: {wuxing2.day_master.value}({wuxing2.day_master_strength})")
    
    # 五行对比
    st.subheader("🌟 五行互补分析")
    col1, col2 = st.columns([1.2, 0.8])
    with col1:
        st.plotly_chart(
            create_wuxing_comparison(wuxing1, wuxing2),
            width="stretch"
        )
    with col2:
        wx = result.wuxing_compat
        st.metric("平衡得分", f"{wx.balance_score}分")
        if wx.complementary:
            st.success("✅ 互补项: " + ", ".join(wx.complementary))
        if wx.conflicting:
            st.warning("⚠️ 冲突项: " + ", ".join(wx.conflicting))
        st.info(wx.analysis)
    
    # 干支关系
    st.subheader("🔗 干支关系分析")
    col1, col2 = st.columns([1, 1])
    with col1:
        st.plotly_chart(create_relations_sunburst(result), width="stretch")
    with col2:
        gz = result.ganzhi_relations
        if gz.tiangan_he:
            st.success(f"💕 天干合: {_format_relations(gz.tiangan_he)}")
        if gz.dizhi_he:
            st.success(f"💕 地支合: {_format_relations(gz.dizhi_he)}")
        if gz.dizhi_chong:
            st.error(f"⚡ 地支冲: {_format_relations(gz.dizhi_chong)}")
        if gz.dizhi_xing:
            st.warning(f"⚠️ 地支刑: {_format_relations(gz.dizhi_xing)}")
        if not any([gz.tiangan_he, gz.dizhi_he, gz.dizhi_chong, gz.dizhi_xing]):
            st.info("关系平和，无明显合冲")
    
    # 建议
    st.subheader("💡 配对建议")
    adv = result.advice
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("##### ✨ 优势方面")
        for s in adv.strengths:
            st.markdown(f"- {s}")
        st.markdown("##### 💪 相处建议")
        for s in adv.suggestions:
            st.markdown(f"- {s}")
    with col2:
        st.markdown("##### ⚠️ 挑战方面")
        for c in adv.challenges:
            st.markdown(f"- {c}")
        st.markdown("##### 🚨 注意事项")
        for c in adv.cautions:
            st.markdown(f"- {c}")
    
    # 下载报告
    st.download_button(
        "📥 下载配对报告 (JSON)",
        result.to_json(),
        file_name=f"compatibility_{info1['date']}_{info2['date']}.json",
        mime="application/json"
    )

    # LLM对话区域
    st.divider()
    session = get_or_create_session(st.session_state, "compatibility")
    session.set_context("配对得分", f"{result.total_score}分 ({result.grade})")
    session.set_context("五行平衡", result.wuxing_compat.analysis)
    session.set_context("主要建议", "; ".join(result.advice.suggestions[:2]))
    render_chat_section(session, api_key, "compatibility", "🤖 配对问答")


def _render_mini_pillars(pillars: list):
    """渲染迷你四柱"""
    cols = st.columns(4)
    for col, pillar, name in zip(cols, pillars, ["年", "月", "日", "时"]):
        with col:
            st.markdown(f"""
            <div style='background:#6366f1;padding:8px;border-radius:8px;
                text-align:center;color:white;font-size:14px'>
                <div>{name}</div>
                <div style='font-size:18px'>{pillar.tiangan.value}</div>
                <div style='font-size:18px'>{pillar.dizhi.value}</div>
            </div>
            """, unsafe_allow_html=True)


def _format_relations(relations: list) -> str:
    """格式化关系列表"""
    return ", ".join(f"{r.elements[0]}{r.elements[1]}({r.description})" for r in relations)

