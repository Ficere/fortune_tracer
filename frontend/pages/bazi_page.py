"""八字分析页面 - 调用后端API"""
import streamlit as st
from datetime import datetime
import json
from frontend.api_client import analyze_bazi, APIError
from src.models import FortuneReport, BaziChart, WuxingAnalysis, AIInterpretation
from src.models.bazi_models import YearFortune
from src.viz import (
    create_wuxing_radar, create_fortune_kline,
    create_year_fortune_line, create_palace_chart
)


def _parse_response(data: dict) -> FortuneReport:
    """解析API响应为数据模型"""
    return FortuneReport.model_validate(data)


def render_bazi_analysis(birth_info: dict, api_key: str | None = None):
    """渲染八字分析结果（调用API）"""
    birth_dt = datetime.combine(birth_info["date"], birth_info["time"])
    
    try:
        with st.spinner("正在分析八字..."):
            response = analyze_bazi(
                birth_dt, birth_info["gender"],
                birth_info["place"] or None, api_key
            )
            report = _parse_response(response)
    except APIError as e:
        st.error(f"❌ API错误: {e.message}")
        return
    
    bazi, wuxing = report.bazi, report.wuxing
    fortunes, interpretation = report.year_fortunes, report.interpretation
    
    # 八字展示
    st.subheader("📜 您的生辰八字")
    _render_pillars(bazi)
    
    # 五行分析
    st.subheader("🌟 五行分析")
    col1, col2 = st.columns([1, 1])
    with col1:
        st.plotly_chart(create_wuxing_radar(wuxing), width="stretch")
    with col2:
        st.markdown(f"**日主**: {wuxing.day_master.value} ({wuxing.day_master_strength})")
        st.markdown(f"**喜用神**: {', '.join(w.value for w in wuxing.favorable)}")
        st.markdown(f"**忌神**: {', '.join(w.value for w in wuxing.unfavorable)}")
        for wx, count in wuxing.counts.to_dict().items():
            st.progress(min(count / 5, 1.0), text=f"{wx}: {count}")

    # 宫位图
    st.subheader("🏛️ 八字宫位")
    st.plotly_chart(create_palace_chart(bazi, wuxing), width="stretch")

    # 运势图表
    st.subheader("📈 运势预测")
    tab1, tab2 = st.tabs(["人生K线图", "流年趋势"])
    with tab1:
        st.plotly_chart(create_fortune_kline(fortunes), width="stretch")
    with tab2:
        st.plotly_chart(create_year_fortune_line(fortunes), width="stretch")
    
    # AI解读
    if interpretation:
        st.subheader("🤖 AI命理解读")
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
    
    # 下载报告
    st.download_button(
        "📥 下载完整报告 (JSON)",
        report.to_json(),
        file_name=f"fortune_report_{birth_info['date']}.json",
        mime="application/json"
    )


def _render_pillars(bazi: BaziChart):
    """渲染四柱"""
    cols = st.columns(4)
    pillars = [bazi.year_pillar, bazi.month_pillar, bazi.day_pillar, bazi.hour_pillar]
    names = ["年柱", "月柱", "日柱", "时柱"]
    for col, pillar, name in zip(cols, pillars, names):
        with col:
            st.markdown(f"""
            <div style='background:linear-gradient(135deg,#667eea,#764ba2);
                padding:20px;border-radius:10px;text-align:center;color:white'>
                <div style='font-size:12px;opacity:0.8'>{name}</div>
                <div style='font-size:28px;font-weight:bold'>{pillar.tiangan.value}</div>
                <div style='font-size:28px;font-weight:bold'>{pillar.dizhi.value}</div>
            </div>
            """, unsafe_allow_html=True)

