"""紫微斗数分析页面"""
import streamlit as st
from datetime import datetime
from src.core.ziwei import calculate_ziwei_chart, generate_ziwei_analysis
from src.viz.ziwei_charts import create_ziwei_chart, create_palace_summary_chart


def render_ziwei_page():
    """渲染紫微斗数页面"""
    st.header("🌟 紫微斗数排盘")
    st.markdown("*根据出生时间排布紫微星盘，分析命理格局*")
    
    # 输入区域
    col1, col2, col3 = st.columns(3)
    
    with col1:
        birth_date = st.date_input(
            "出生日期",
            value=datetime(1990, 1, 1),
            min_value=datetime(1900, 1, 1),
            max_value=datetime.now(),
            key="ziwei_birth_date"
        )
    
    with col2:
        birth_time = st.time_input(
            "出生时间",
            value=datetime(2000, 1, 1, 12, 0).time(),
            key="ziwei_birth_time"
        )
    
    with col3:
        gender = st.selectbox("性别", ["男", "女"], key="ziwei_gender")
    
    birth_place = st.text_input(
        "出生地点（可选）",
        placeholder="如：北京、上海",
        key="ziwei_birth_place"
    )
    
    if st.button("排盘分析", type="primary", key="ziwei_analyze"):
        birth_datetime = datetime.combine(birth_date, birth_time)
        
        with st.spinner("正在排盘..."):
            try:
                chart = calculate_ziwei_chart(
                    birth_datetime, gender, birth_place or None
                )
                analysis = generate_ziwei_analysis(chart)
                
                # 存储到session
                st.session_state["ziwei_chart"] = chart
                st.session_state["ziwei_analysis"] = analysis
                
            except Exception as e:
                st.error(f"排盘失败：{str(e)}")
                return
    
    # 显示结果
    if "ziwei_chart" in st.session_state:
        _display_ziwei_result()


def _display_ziwei_result():
    """显示紫微分析结果"""
    chart = st.session_state["ziwei_chart"]
    analysis = st.session_state["ziwei_analysis"]
    
    # 星盘图
    st.subheader("📊 紫微星盘")
    fig = create_ziwei_chart(chart)
    st.plotly_chart(fig, use_container_width=True)
    
    # 基本信息
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("五行局", chart.wuxing_ju.value)
    with col2:
        ming_palace = next((p for p in chart.palaces if p.palace.value == "命宫"), None)
        ming_zhi = ming_palace.dizhi if ming_palace else "-"
        st.metric("命宫", ming_zhi)
    with col3:
        shen_zhi = chart.palaces[chart.shen_gong_pos].dizhi if chart.palaces else "-"
        st.metric("身宫", shen_zhi)
    with col4:
        lunar_info = f"{chart.lunar_month}月{chart.lunar_day}日"
        st.metric("农历", lunar_info)
    
    # 四化显示
    if chart.sihua_stars:
        st.subheader("✨ 四化飞星")
        sihua_cols = st.columns(4)
        for i, (hua_name, star_info) in enumerate(chart.sihua_stars.items()):
            with sihua_cols[i % 4]:
                st.info(f"**{hua_name}**\n\n{star_info}")
    
    # 分析结果
    st.subheader("📝 命盘解读")
    
    tabs = st.tabs(["性格特点", "事业运势", "财运分析", "感情姻缘", "健康提示"])
    
    with tabs[0]:
        st.markdown(f"**性格分析：**\n\n{analysis.personality}")
    
    with tabs[1]:
        st.markdown(f"**事业分析：**\n\n{analysis.career}")
    
    with tabs[2]:
        st.markdown(f"**财运分析：**\n\n{analysis.wealth}")
    
    with tabs[3]:
        st.markdown(f"**感情分析：**\n\n{analysis.love}")
    
    with tabs[4]:
        st.markdown(f"**健康提示：**\n\n{analysis.health}")
    
    # 宫位雷达图
    st.subheader("📈 宫位评分")
    radar_fig = create_palace_summary_chart(chart)
    st.plotly_chart(radar_fig, use_container_width=True)
    
    # 综合评价
    st.subheader("🎯 综合评价")
    st.success(analysis.summary)
    
    # 十二宫详情
    with st.expander("查看十二宫详情", expanded=False):
        _display_all_palaces(chart)


def _display_all_palaces(chart):
    """显示所有宫位详情"""
    for palace in chart.palaces:
        main_stars = ", ".join([s.name + s.sihua for s in palace.main_stars]) or "无"
        aux_stars = ", ".join([s.name for s in palace.aux_stars]) or "无"
        sha_stars = ", ".join([s.name for s in palace.sha_stars]) or "无"
        
        st.markdown(f"""
        **{palace.tiangan}{palace.dizhi} {palace.palace.value}**
        - 主星：{main_stars}
        - 辅星：{aux_stars}
        - 煞星：{sha_stars}
        ---
        """)

