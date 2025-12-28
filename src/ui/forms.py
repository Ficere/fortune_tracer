"""输入表单模块 - 各功能的输入区域"""
import streamlit as st
from datetime import datetime, time
from src.ui.city_selector import render_city_selector


def render_form(mode: str, api_key: str | None):
    """根据功能类型渲染输入表单"""
    if mode == "🔮 个人八字":
        _render_bazi_form(api_key)
    elif mode == "💑 配对分析":
        _render_compatibility_form(api_key)
    elif mode == "📅 择日":
        _render_date_selection_form(api_key)
    else:
        _render_bonefate_form(api_key)


def _render_bazi_form(api_key: str | None):
    """个人八字输入表单"""
    st.subheader("📝 出生信息")

    col1, col2 = st.columns(2)
    with col1:
        birth_date = st.date_input(
            "出生日期",
            value=datetime(1990, 1, 1),
            min_value=datetime(1900, 1, 1),
            max_value=datetime.now()
        )
        gender = st.selectbox("性别", ["男", "女"])
    with col2:
        birth_time = st.time_input("出生时间", value=time(12, 0))
        birth_place = render_city_selector(key="bazi_city")

    analyze_btn = st.button("🔮 开始解读", type="primary", use_container_width=True)

    if analyze_btn:
        from src.ui import render_bazi_analysis
        birth_info = {"date": birth_date, "time": birth_time, "gender": gender, "place": birth_place}
        st.divider()
        render_bazi_analysis(birth_info, api_key)


def _render_compatibility_form(api_key: str | None):
    """配对分析输入表单"""
    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("📝 本人信息")
        date1 = st.date_input("出生日期", value=datetime(1990, 1, 1), key="d1")
        time1 = st.time_input("出生时间", value=time(12, 0), key="t1")
        gender1 = st.selectbox("性别", ["男", "女"], key="g1")
        place1 = render_city_selector(key="compat_city1")

    with col_b:
        st.subheader("💕 对方信息")
        date2 = st.date_input("出生日期", value=datetime(1992, 1, 1), key="d2")
        time2 = st.time_input("出生时间", value=time(12, 0), key="t2")
        gender2 = st.selectbox("性别", ["女", "男"], key="g2")
        place2 = render_city_selector(key="compat_city2")

    analyze_btn = st.button("💑 开始配对", type="primary", use_container_width=True)

    if analyze_btn:
        from src.ui import render_compatibility_analysis
        info1 = {"date": date1, "time": time1, "gender": gender1, "place": place1}
        info2 = {"date": date2, "time": time2, "gender": gender2, "place": place2}
        st.divider()
        render_compatibility_analysis(info1, info2, api_key)


def _render_date_selection_form(api_key: str | None):
    """择日输入表单"""
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📝 您的出生信息")
        zr_date = st.date_input("出生日期", value=datetime(1990, 1, 1), key="zd")
        zr_time = st.time_input("出生时间", value=time(12, 0), key="zt")
        zr_gender = st.selectbox("性别", ["男", "女"], key="zg")
        zr_place = render_city_selector(key="date_city")

    with col2:
        st.subheader("📅 择日设置")
        event_type = st.selectbox("事件类型", ["结婚", "开业", "搬家", "出行", "签约"])
        search_days = st.slider("搜索天数", 15, 90, 30)

    analyze_btn = st.button("📅 开始择日", type="primary", use_container_width=True)

    if analyze_btn:
        from src.ui import render_date_selection
        zr_info = {"date": zr_date, "time": zr_time, "gender": zr_gender, "place": zr_place}
        st.divider()
        render_date_selection(zr_info, event_type, search_days, api_key)


def _render_bonefate_form(api_key: str | None):
    """称骨算命输入表单"""
    st.subheader("📝 出生信息")
    st.caption("袁天罡八字称骨算命")
    
    col1, col2 = st.columns(2)
    with col1:
        bf_date = st.date_input("出生日期", value=datetime(1990, 1, 1), key="bf_d")
        bf_lunar = st.checkbox("输入日期为农历", key="bf_lunar")
    with col2:
        bf_time = st.time_input("出生时间", value=time(12, 0), key="bf_t")
    
    analyze_btn = st.button("⚖️ 开始称骨", type="primary", use_container_width=True)
    
    if analyze_btn:
        from src.ui import render_bonefate_analysis
        bf_info = {"date": bf_date, "time": bf_time}
        st.divider()
        render_bonefate_analysis(bf_info, bf_lunar, api_key)

