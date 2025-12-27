"""八字分析页面"""
import streamlit as st
from datetime import datetime
from src.core import calculate_bazi, analyze_wuxing
from src.ai.interpreter import interpret_bazi, calculate_year_fortunes
from src.viz import (
    create_wuxing_radar, create_fortune_kline,
    create_year_fortune_line, create_palace_chart
)
from src.models import FortuneReport
from src.models.bazi_models import Gender
from .common import render_pillar_display


def render_bazi_analysis(birth_info: dict, api_key: str | None = None):
    """渲染八字分析结果"""
    birth_dt = datetime.combine(birth_info["date"], birth_info["time"])
    gender_enum = Gender.MALE if birth_info["gender"] == "男" else Gender.FEMALE
    
    with st.spinner("正在计算八字..."):
        bazi = calculate_bazi(birth_dt, gender_enum, birth_info["place"] or None)
        wuxing = analyze_wuxing(bazi)
        fortunes = calculate_year_fortunes(bazi, wuxing, years=10)
    
    # 八字展示
    st.subheader("📜 您的生辰八字")
    pillars = [bazi.year_pillar, bazi.month_pillar, bazi.day_pillar, bazi.hour_pillar]
    names = ["年柱", "月柱", "日柱", "时柱"]
    render_pillar_display(pillars, names)
    
    # 五行分析
    st.subheader("🌟 五行分析")
    col1, col2 = st.columns([1, 1])
    with col1:
        st.plotly_chart(create_wuxing_radar(wuxing), use_container_width=True)
    with col2:
        st.markdown(f"**日主**: {wuxing.day_master.value} ({wuxing.day_master_strength})")
        st.markdown(f"**喜用神**: {', '.join(w.value for w in wuxing.favorable)}")
        st.markdown(f"**忌神**: {', '.join(w.value for w in wuxing.unfavorable)}")
        counts = wuxing.counts.to_dict()
        for wx, count in counts.items():
            st.progress(min(count / 5, 1.0), text=f"{wx}: {count}")
    
    # 宫位图
    st.subheader("🏛️ 八字宫位")
    st.plotly_chart(create_palace_chart(bazi, wuxing), use_container_width=True)
    
    # 运势图表
    st.subheader("📈 运势预测")
    tab1, tab2 = st.tabs(["人生K线图", "流年趋势"])
    with tab1:
        st.plotly_chart(create_fortune_kline(fortunes), use_container_width=True)
    with tab2:
        st.plotly_chart(create_year_fortune_line(fortunes), use_container_width=True)
    
    # AI解读
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
    
    # 数据导出
    report = FortuneReport(
        bazi=bazi, wuxing=wuxing,
        interpretation=interpretation, year_fortunes=fortunes
    )
    st.download_button(
        "📥 下载完整报告 (JSON)",
        report.to_json(),
        file_name=f"fortune_report_{birth_info['date']}.json",
        mime="application/json"
    )

