"""称骨算命页面 - 袁天罡八字称骨算命"""

import streamlit as st
from datetime import datetime
from src.core import analyze_bonefate
from src.models import BoneFateResult


def render_bonefate_analysis(birth_info: dict, is_lunar: bool = False):
    """渲染称骨算命分析结果
    
    Args:
        birth_info: 包含 date, time 的字典
        is_lunar: 是否为农历日期
    """
    birth_dt = datetime.combine(birth_info["date"], birth_info["time"])
    
    with st.spinner("正在计算骨重..."):
        result_dict = analyze_bonefate(birth_dt, is_lunar)
        result = BoneFateResult.from_dict(result_dict)
    
    # 骨重展示
    st.subheader("⚖️ 您的骨重")
    _render_weight_display(result)
    
    # 日期信息
    st.subheader("📅 出生信息")
    _render_date_info(result)
    
    # 命格分析
    st.subheader("📜 命格分析")
    _render_fate_analysis(result)
    
    # 命运诗词
    st.subheader("📖 命运诗词")
    _render_poem(result)
    
    # 下载报告
    st.download_button(
        "📥 下载称骨报告 (JSON)",
        result.to_json(),
        file_name=f"bonefate_report_{birth_info['date']}.json",
        mime="application/json",
    )


def _render_weight_display(result: BoneFateResult):
    """渲染骨重显示"""
    # 骨重仪表盘
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # 骨重主显示
        weight_percent = min((result.weight - 2.0) / 5.2 * 100, 100)
        
        st.markdown(f"""
        <div style='text-align: center; padding: 30px; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 20px; color: white; margin: 10px 0;'>
            <div style='font-size: 48px; font-weight: bold;'>{result.weight_display}</div>
            <div style='font-size: 20px; margin-top: 10px;'>骨重等级: {result.level}</div>
            <div style='font-size: 14px; margin-top: 5px; opacity: 0.9;'>{result.level_desc}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # 骨重进度条
        st.progress(weight_percent / 100, text=f"骨重范围: 2.1两 ~ 7.2两")


def _render_date_info(result: BoneFateResult):
    """渲染日期信息"""
    col1, col2 = st.columns(2)
    
    with col1:
        lunar = result.lunar_date
        st.markdown(f"""
        <div style='background: #fef3c7; padding: 15px; border-radius: 10px;
            border-left: 4px solid #f59e0b;'>
            <div style='font-weight: bold; color: #92400e;'>🌙 农历</div>
            <div style='font-size: 18px; color: #78350f; margin-top: 8px;'>
                {lunar.year}年 {lunar.month}月 {lunar.day}日 {lunar.hour}时
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        solar = result.solar_date
        st.markdown(f"""
        <div style='background: #dbeafe; padding: 15px; border-radius: 10px;
            border-left: 4px solid #3b82f6;'>
            <div style='font-weight: bold; color: #1e40af;'>☀️ 阳历</div>
            <div style='font-size: 18px; color: #1e3a8a; margin-top: 8px;'>
                {solar.year}年 {solar.month}月 {solar.day}日 {solar.hour}:00
            </div>
        </div>
        """, unsafe_allow_html=True)


def _render_fate_analysis(result: BoneFateResult):
    """渲染命格分析"""
    # 命格标题卡片
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        padding: 20px; border-radius: 15px; margin: 10px 0;'>
        <div style='font-size: 24px; font-weight: bold; color: #92400e; text-align: center;'>
            「{result.title}」
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 等级详情
    _render_level_explanation(result.level)


def _render_level_explanation(level: str):
    """渲染等级说明"""
    level_info = {
        "下下": {"color": "#dc2626", "emoji": "😢", "desc": "命途多舛，需以勤勉自持，逆境中求发展"},
        "下": {"color": "#ea580c", "emoji": "😔", "desc": "早年困苦较多，但晚年可渐入佳境"},
        "中下": {"color": "#d97706", "emoji": "😐", "desc": "平凡辛劳之命，守成持重为上策"},
        "中": {"color": "#65a30d", "emoji": "😊", "desc": "中等福禄，一生平稳，知足常乐"},
        "中上": {"color": "#16a34a", "emoji": "😄", "desc": "福禄不缺，先苦后甜，晚景渐隆"},
        "上": {"color": "#0891b2", "emoji": "😁", "desc": "福寿双全，衣禄无忧，平安顺遂"},
        "上上": {"color": "#7c3aed", "emoji": "🤩", "desc": "富贵荣华，名利双收，贵人相助"},
        "极上": {"color": "#c026d3", "emoji": "🌟", "desc": "贵人天相，逍遥快乐，声名远播"},
        "至尊": {"color": "#e11d48", "emoji": "👑", "desc": "帝王将相之格，万古流芳之命"},
    }
    
    info = level_info.get(level, level_info["中"])
    
    st.markdown(f"""
    <div style='display: flex; align-items: center; padding: 15px;
        background: #f8fafc; border-radius: 10px; margin-top: 10px;'>
        <span style='font-size: 40px; margin-right: 15px;'>{info['emoji']}</span>
        <div>
            <div style='font-weight: bold; color: {info['color']}; font-size: 18px;'>
                等级评价: {level}
            </div>
            <div style='color: #64748b; margin-top: 5px;'>{info['desc']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def _render_poem(result: BoneFateResult):
    """渲染命运诗词"""
    # 将诗词按换行符分割
    lines = result.poem.split('\n')
    
    st.markdown("""
    <div style='background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        padding: 30px; border-radius: 15px; color: #f1f5f9;'>
    """, unsafe_allow_html=True)
    
    for line in lines:
        if line.strip():
            st.markdown(f"""
            <p style='font-size: 16px; line-height: 2; margin: 10px 0;
                text-align: center; letter-spacing: 2px;'>
                {line.strip()}
            </p>
            """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # 提示说明
    st.caption("""
    💡 **温馨提示**：称骨算命是民间流传的传统命理方法，仅供参考和娱乐。
    命运掌握在自己手中，努力和态度才是决定人生的关键因素。
    """)
