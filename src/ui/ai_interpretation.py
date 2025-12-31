"""AI解读渲染组件"""
import os
import streamlit as st
from src.ai.interpreter import interpret_bazi_full
from src.ai import get_or_create_session
from src.models import FortuneReport
from .chat_component import render_chat_section


def render_ai_interpretation(
    bazi, wuxing, api_key, birth_info, fortunes, all_analysis: dict | None = None
):
    """渲染AI解读和报告下载

    Args:
        all_analysis: 包含 shishen, dayun, shensha, nayin, auxiliary, bonefate 的字典
    """
    st.subheader("🤖 AI命理解读")

    # API Key缺失提示
    has_api_key = api_key or os.getenv("OPENAI_API_KEY")
    if not has_api_key:
        st.warning("⚠️ 未检测到OpenAI API Key，当前使用**离线规则库**进行解读。"
                   "如需AI智能解读，请在左侧设置中填写API Key。")

    with st.spinner("正在分析您的命盘..."):
        interpretation = interpret_bazi_full(bazi, wuxing, api_key, all_analysis)

    _render_interpretation_cards(interpretation)
    _render_download_button(bazi, wuxing, interpretation, fortunes, birth_info)
    _render_chat_area(bazi, wuxing, interpretation, api_key, all_analysis)


def _render_interpretation_cards(interpretation):
    """渲染解读卡片"""
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


def _render_download_button(bazi, wuxing, interpretation, fortunes, birth_info):
    """渲染下载按钮"""
    report = FortuneReport(
        bazi=bazi, wuxing=wuxing,
        interpretation=interpretation, year_fortunes=fortunes
    )
    st.download_button(
        "📥 下载完整报告 (JSON)", report.to_json(),
        file_name=f"fortune_report_{birth_info['date']}.json",
        mime="application/json"
    )


def _render_chat_area(bazi, wuxing, interpretation, api_key, all_analysis=None):
    """渲染LLM对话区域"""
    st.divider()
    session = get_or_create_session(st.session_state, "bazi")
    bazi_display = (f"{bazi.year_pillar.display} {bazi.month_pillar.display} "
                    f"{bazi.day_pillar.display} {bazi.hour_pillar.display}")
    session.set_context("八字", bazi_display)
    session.set_context("日主", f"{wuxing.day_master.value}({wuxing.day_master_strength})")
    session.set_context("喜用神", ", ".join(w.value for w in wuxing.favorable))
    session.set_context("性格特点", interpretation.personality[:50])

    # 添加更多上下文
    if all_analysis:
        if all_analysis.get("shishen"):
            session.set_context("格局", all_analysis["shishen"].pattern)
        if all_analysis.get("bonefate"):
            session.set_context("称骨", f"{all_analysis['bonefate'].weight}两")

    render_chat_section(session, api_key, "bazi", "🤖 八字问答")

