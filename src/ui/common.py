"""通用UI组件"""
import streamlit as st
from datetime import datetime, time


def render_birth_input(prefix: str = "", default_year: int = 1990) -> dict:
    """渲染出生信息输入表单"""
    label_suffix = f" ({prefix})" if prefix else ""
    
    birth_date = st.date_input(
        f"出生日期{label_suffix}",
        value=datetime(default_year, 1, 1),
        min_value=datetime(1900, 1, 1),
        max_value=datetime.now(),
        key=f"date_{prefix}"
    )
    
    birth_time = st.time_input(
        f"出生时间{label_suffix}",
        value=time(12, 0),
        key=f"time_{prefix}"
    )
    
    gender = st.selectbox(
        f"性别{label_suffix}",
        ["男", "女"],
        key=f"gender_{prefix}"
    )
    
    birth_place = st.text_input(
        f"出生地点{label_suffix}（可选）",
        placeholder="如：北京",
        key=f"place_{prefix}"
    )
    
    return {
        "date": birth_date,
        "time": birth_time,
        "gender": gender,
        "place": birth_place
    }


def render_pillar_display(pillars: list, names: list):
    """渲染四柱展示"""
    cols = st.columns(4)
    for col, name, pillar in zip(cols, names, pillars):
        with col:
            st.markdown(f"""
            <div style='background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);
                padding:20px;border-radius:10px;text-align:center;color:white;margin:5px'>
                <div style='font-size:12px;opacity:0.8'>{name}</div>
                <div style='font-size:32px;font-weight:bold'>{pillar.tiangan.value}</div>
                <div style='font-size:32px;font-weight:bold'>{pillar.dizhi.value}</div>
            </div>
            """, unsafe_allow_html=True)

