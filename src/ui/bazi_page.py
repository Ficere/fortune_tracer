"""八字分析页面"""
import streamlit as st
from datetime import datetime
from src.core import (
    calculate_bazi, analyze_wuxing, calculate_dayun,
    analyze_shishen, convert_to_true_solar_time,
    calculate_shensha, calculate_nayin, calculate_auxiliary_from_bazi
)
from src.ai.interpreter import interpret_bazi, calculate_year_fortunes
from src.viz import (
    create_wuxing_radar, create_fortune_kline,
    create_year_fortune_line, create_palace_chart
)
from src.models import FortuneReport
from src.models.bazi_models import Gender
from .common import render_pillar_display
from .bazi_components import (
    render_auxiliary_info, render_nayin_info, render_shensha_info
)


def render_bazi_analysis(birth_info: dict, api_key: str | None = None):
    """渲染八字分析结果"""
    birth_dt = datetime.combine(birth_info["date"], birth_info["time"])
    gender_enum = Gender.MALE if birth_info["gender"] == "男" else Gender.FEMALE
    place = birth_info["place"] or None
    
    # 真太阳时转换
    true_solar_dt = convert_to_true_solar_time(birth_dt, place) if place else birth_dt
    
    with st.spinner("正在计算八字..."):
        bazi = calculate_bazi(true_solar_dt, gender_enum, place)
        wuxing = analyze_wuxing(bazi)
        shishen = analyze_shishen(bazi)
        dayun_info = calculate_dayun(bazi)
        shensha = calculate_shensha(bazi)
        nayin_list = calculate_nayin(bazi)
        auxiliary = calculate_auxiliary_from_bazi(bazi)
        fortunes = calculate_year_fortunes(bazi, wuxing, years=10)
    
    # 八字展示
    st.subheader("📜 您的生辰八字")
    if place and true_solar_dt != birth_dt:
        st.caption(f"📍 已转换为{place}真太阳时")
    pillars = [bazi.year_pillar, bazi.month_pillar, bazi.day_pillar, bazi.hour_pillar]
    render_pillar_display(pillars, ["年柱", "月柱", "日柱", "时柱"])
    st.caption(f"格局: **{shishen.pattern}** | {shishen.analysis}")
    
    # 辅助宫位
    st.subheader("🏯 辅助宫位")
    render_auxiliary_info(auxiliary)
    
    # 纳音五行
    st.subheader("🎵 纳音五行")
    render_nayin_info(nayin_list)
    
    # 五行分析
    st.subheader("🌟 五行分析")
    _render_wuxing_section(wuxing)
    
    # 神煞分析
    st.subheader("⚔️ 神煞分析")
    render_shensha_info(shensha)
    
    # 十神 & 大运
    tab_ss, tab_dy = st.tabs(["🔮 十神分析", "🛤️ 大运排盘"])
    with tab_ss:
        _render_shishen_table(shishen)
    with tab_dy:
        _render_dayun(dayun_info)
    
    # 宫位图 & 运势图
    st.subheader("📈 运势分析")
    tab1, tab2, tab3 = st.tabs(["宫位图", "人生K线", "流年趋势"])
    with tab1:
        st.plotly_chart(create_palace_chart(bazi, wuxing), use_container_width=True)
    with tab2:
        st.plotly_chart(create_fortune_kline(fortunes), use_container_width=True)
    with tab3:
        st.plotly_chart(create_year_fortune_line(fortunes), use_container_width=True)
    
    # AI解读
    _render_ai_interpretation(bazi, wuxing, api_key, birth_info, fortunes)


def _render_wuxing_section(wuxing):
    """渲染五行分析部分"""
    col1, col2 = st.columns([1, 1])
    with col1:
        st.plotly_chart(create_wuxing_radar(wuxing), use_container_width=True)
    with col2:
        st.markdown(f"**日主**: {wuxing.day_master.value} ({wuxing.day_master_strength})")
        st.markdown(f"**喜用神**: {', '.join(w.value for w in wuxing.favorable)}")
        st.markdown(f"**忌神**: {', '.join(w.value for w in wuxing.unfavorable)}")
        for wx, count in wuxing.counts.to_dict().items():
            st.progress(min(count / 5, 1.0), text=f"{wx}: {count:.1f}")


def _render_shishen_table(shishen):
    """渲染十神表格"""
    cols = st.columns(4)
    for col, info in zip(cols, shishen.shishen_list):
        with col:
            st.markdown(f"""
            <div style='background:#f8fafc;padding:10px;border-radius:8px;
                text-align:center;border:1px solid #e2e8f0'>
                <div style='font-size:12px;color:#64748b'>{info.pillar_name}</div>
                <div style='font-size:16px;font-weight:bold;color:#334155'>
                    {info.tiangan} <span style='color:#6366f1'>({info.tiangan_shishen})</span>
                </div>
                <div style='font-size:16px;font-weight:bold;color:#334155'>{info.dizhi}</div>
                <div style='font-size:10px;color:#94a3b8'>
                    藏: {', '.join(info.dizhi_shishen) or '-'}
                </div>
            </div>
            """, unsafe_allow_html=True)


def _render_dayun(dayun_info):
    """渲染大运"""
    st.caption(
        f"起运: **{dayun_info.start_age}岁{dayun_info.extra_months}个月** | "
        f"方向: **{dayun_info.direction}**"
    )
    cols = st.columns(len(dayun_info.dayun_list))
    for col, dy in zip(cols, dayun_info.dayun_list):
        with col:
            st.markdown(f"""
            <div style='background:linear-gradient(135deg,#6366f1,#8b5cf6);
                padding:8px;border-radius:8px;text-align:center;color:white'>
                <div style='font-size:16px;font-weight:bold'>{dy.ganzhi}</div>
                <div style='font-size:12px'>{dy.start_age}-{dy.end_age}岁</div>
                <div style='font-size:11px;opacity:0.8'>{dy.start_year}-{dy.end_year}</div>
            </div>
            """, unsafe_allow_html=True)


def _render_ai_interpretation(bazi, wuxing, api_key, birth_info, fortunes):
    """渲染AI解读和报告下载"""
    from src.ai.interpreter import interpret_bazi
    
    st.subheader("🤖 AI命理解读")
    with st.spinner("AI正在分析您的命盘..."):
        interpretation = interpret_bazi(bazi, wuxing, api_key)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 💫 性格特点")
        st.info(interpretation.personality)
        st.markdown("#### 💼 事业运势")
        st.info(interpretation.career)
        st.markdown("#### 💰 财运分析")
        st.info(interpretation.wealth)
    with col2:
        st.markdown("#### 💕 感情运势")
        st.info(interpretation.love)
        st.markdown("#### 🏥 健康建议")
        st.info(interpretation.health)
        st.markdown("#### 📋 综合评价")
        st.success(interpretation.summary)
    
    report = FortuneReport(
        bazi=bazi, wuxing=wuxing,
        interpretation=interpretation, year_fortunes=fortunes
    )
    st.download_button(
        "📥 下载完整报告 (JSON)", report.to_json(),
        file_name=f"fortune_report_{birth_info['date']}.json",
        mime="application/json"
    )

