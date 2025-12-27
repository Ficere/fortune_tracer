"""择日页面"""
import streamlit as st
from datetime import datetime, date
from src.core import (
    calculate_bazi, analyze_wuxing, select_dates,
    convert_to_true_solar_time
)
from src.models import EventType
from src.models.bazi_models import Gender
from src.models.date_selection_models import DayQuality
from src.viz import create_date_calendar, create_date_timeline


# 质量对应样式
QUALITY_STYLES = {
    DayQuality.EXCELLENT: ("🌟", "#22c55e", "大吉之日"),
    DayQuality.GOOD: ("✨", "#86efac", "吉利之日"),
    DayQuality.NEUTRAL: ("⚪", "#fbbf24", "平常之日"),
    DayQuality.BAD: ("⚠️", "#f87171", "不宜之日"),
    DayQuality.TERRIBLE: ("❌", "#dc2626", "大凶之日"),
}


def render_date_selection(birth_info: dict, event_type: str, search_days: int):
    """渲染择日结果"""
    # 计算八字（支持真太阳时）
    birth_dt = datetime.combine(birth_info["date"], birth_info["time"])
    gender_enum = Gender.MALE if birth_info["gender"] == "男" else Gender.FEMALE
    place = birth_info["place"] or None
    
    if place:
        birth_dt = convert_to_true_solar_time(birth_dt, place)
    
    with st.spinner("正在择日..."):
        bazi = calculate_bazi(birth_dt, gender_enum, place)
        wuxing = analyze_wuxing(bazi)
        
        event_map = {
            "结婚": EventType.WEDDING,
            "开业": EventType.BUSINESS,
            "搬家": EventType.MOVING,
            "出行": EventType.TRAVEL,
            "签约": EventType.SIGNING,
        }
        event = event_map.get(event_type, EventType.WEDDING)
        
        result = select_dates(bazi, wuxing, event, date.today(), search_days)
    
    # 显示您的八字信息
    st.subheader("📜 您的八字")
    cols = st.columns(4)
    for col, pillar, name in zip(
        cols,
        [bazi.year_pillar, bazi.month_pillar, bazi.day_pillar, bazi.hour_pillar],
        ["年", "月", "日", "时"]
    ):
        with col:
            st.markdown(f"""
            <div style='background:#6366f1;padding:8px;border-radius:8px;
                text-align:center;color:white'>
                <div>{name}</div>
                <div style='font-size:20px'>{pillar.display}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown(f"**喜用神**: {', '.join(w.value for w in wuxing.favorable)} | "
                f"**忌神**: {', '.join(w.value for w in wuxing.unfavorable)}")
    
    # 择日结果概览
    st.subheader(f"📅 {event_type}择日结果")
    st.info(result.summary)
    
    # 可视化
    col1, col2 = st.columns([1.2, 0.8])
    with col1:
        st.plotly_chart(create_date_calendar(result), use_container_width=True)
    with col2:
        st.plotly_chart(create_date_timeline(result), use_container_width=True)
    
    # 推荐吉日详情
    st.subheader("🌟 推荐吉日")
    if result.recommended_dates:
        for day in result.recommended_dates[:6]:
            icon, color, desc = QUALITY_STYLES[day.quality]
            with st.expander(
                f"{icon} {day.date.strftime('%Y-%m-%d')} {day.ganzhi} - {day.quality.value} (得分:{day.score})"
            ):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**✅ 宜**: {', '.join(day.suitable)}")
                with col2:
                    st.markdown(f"**❌ 忌**: {', '.join(day.avoid)}")
                if day.clash_zodiac:
                    st.warning(f"⚠️ 冲 {day.clash_zodiac}")
                st.caption(day.analysis)
    else:
        st.warning("未找到推荐的吉日，建议扩大搜索范围")
    
    # 需避开的日期
    if result.avoid_dates:
        st.subheader("⚠️ 需避开的日期")
        avoid_text = ", ".join(
            f"{d.date.strftime('%m/%d')}({d.ganzhi})"
            for d in result.avoid_dates[:5]
        )
        st.error(avoid_text)
    
    # 下载报告
    st.download_button(
        "📥 下载择日报告 (JSON)",
        result.to_json(),
        file_name=f"date_selection_{event_type}_{date.today()}.json",
        mime="application/json"
    )

