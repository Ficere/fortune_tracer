"""生辰八字AI解读Web应用 - 主入口"""
import streamlit as st
from datetime import datetime, time

st.set_page_config(
    page_title="Fortune Tracer - 生辰八字AI解读",
    page_icon="🔮",
    layout="wide"
)

# 样式
st.markdown("""
<style>
.main-title { text-align: center; color: #6366f1; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>🔮 Fortune Tracer</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center;color:#64748b'>生辰八字 AI 智能解读</h3>", unsafe_allow_html=True)

# 侧边栏 - 功能选择与输入
with st.sidebar:
    mode = st.radio("功能选择", ["🔮 个人八字", "💑 配对分析", "📅 择日", "⚖️ 称骨算命"], horizontal=True)
    st.divider()

    if mode == "🔮 个人八字":
        st.header("📝 出生信息")
        birth_date = st.date_input(
            "出生日期", value=datetime(1990, 1, 1),
            min_value=datetime(1900, 1, 1), max_value=datetime.now()
        )
        birth_time = st.time_input("出生时间", value=time(12, 0))
        gender = st.selectbox("性别", ["男", "女"])
        birth_place = st.text_input("出生地点（可选）", placeholder="如：北京")
        api_key = st.text_input("OpenAI API Key（可选）", type="password")
        analyze_btn = st.button("🔮 开始解读", type="primary", use_container_width=True)
    elif mode == "💑 配对分析":
        st.header("📝 本人信息")
        date1 = st.date_input("出生日期", value=datetime(1990, 1, 1), key="d1")
        time1 = st.time_input("出生时间", value=time(12, 0), key="t1")
        gender1 = st.selectbox("性别", ["男", "女"], key="g1")
        place1 = st.text_input("出生地点（可选）", key="p1")
        st.divider()
        st.header("💕 对方信息")
        date2 = st.date_input("出生日期", value=datetime(1992, 1, 1), key="d2")
        time2 = st.time_input("出生时间", value=time(12, 0), key="t2")
        gender2 = st.selectbox("性别", ["女", "男"], key="g2")
        place2 = st.text_input("出生地点（可选）", key="p2")
        analyze_btn = st.button("💑 开始配对", type="primary", use_container_width=True)
    elif mode == "📅 择日":
        st.header("📝 您的出生信息")
        zr_date = st.date_input("出生日期", value=datetime(1990, 1, 1), key="zd")
        zr_time = st.time_input("出生时间", value=time(12, 0), key="zt")
        zr_gender = st.selectbox("性别", ["男", "女"], key="zg")
        zr_place = st.text_input("出生地点（可选）", key="zp")
        st.divider()
        st.header("📅 择日设置")
        event_type = st.selectbox("事件类型", ["结婚", "开业", "搬家", "出行", "签约"])
        search_days = st.slider("搜索天数", 15, 90, 30)
        analyze_btn = st.button("📅 开始择日", type="primary", use_container_width=True)
    else:  # 称骨算命
        st.header("📝 出生信息")
        st.caption("袁天罡八字称骨算命")
        bf_date = st.date_input("出生日期", value=datetime(1990, 1, 1), key="bf_d")
        bf_time = st.time_input("出生时间", value=time(12, 0), key="bf_t")
        bf_lunar = st.checkbox("输入日期为农历", key="bf_lunar")
        analyze_btn = st.button("⚖️ 开始称骨", type="primary", use_container_width=True)

# 主内容区
if analyze_btn:
    if mode == "🔮 个人八字":
        from src.ui import render_bazi_analysis
        birth_info = {"date": birth_date, "time": birth_time, "gender": gender, "place": birth_place}
        render_bazi_analysis(birth_info, api_key or None)
    elif mode == "💑 配对分析":
        from src.ui import render_compatibility_analysis
        info1 = {"date": date1, "time": time1, "gender": gender1, "place": place1}
        info2 = {"date": date2, "time": time2, "gender": gender2, "place": place2}
        render_compatibility_analysis(info1, info2)
    elif mode == "📅 择日":
        from src.ui import render_date_selection
        zr_info = {"date": zr_date, "time": zr_time, "gender": zr_gender, "place": zr_place}
        render_date_selection(zr_info, event_type, search_days)
    else:  # 称骨算命
        from src.ui import render_bonefate_analysis
        bf_info = {"date": bf_date, "time": bf_time}
        render_bonefate_analysis(bf_info, bf_lunar)
else:
    st.info("👈 请在左侧选择功能并填写信息，然后点击按钮开始分析")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        ### 🔮 个人八字
        - 精准四柱计算
        - 五行雷达图
        - 人生K线图
        - AI命理解读
        """)
    with col2:
        st.markdown("""
        ### 💑 配对分析
        - 双人八字对比
        - 五行互补分析
        - 干支相合相冲
        - 配对得分评级
        """)
    with col3:
        st.markdown("""
        ### 📅 择日功能
        - 结婚/开业吉日
        - 搬家/出行吉日
        - 每日宜忌事项
        - 冲煞生肖提醒
        """)
    with col4:
        st.markdown("""
        ### ⚖️ 称骨算命
        - 袁天罡称骨法
        - 计算命运骨重
        - 命格等级评定
        - 古诗词命书
        """)

