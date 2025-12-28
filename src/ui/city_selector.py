"""城市选择器组件 - 提供智能城市搜索和选择功能"""
import streamlit as st
from src.core.city_search import (
    search_cities, get_all_city_options, parse_city_option
)


def render_city_selector(
    label: str = "出生地点（可选）",
    key: str = "city",
    help_text: str = "支持拼音和模糊搜索"
) -> str:
    """
    渲染城市选择器
    
    使用 selectbox 配合搜索功能，让用户选择存在于数据库中的城市
    
    Args:
        label: 标签文字
        key: 组件唯一标识
        help_text: 帮助文字
    
    Returns:
        选中的城市名（不含省份后缀），未选择返回空字符串
    """
    # 初始化 session state
    search_key = f"{key}_search"
    if search_key not in st.session_state:
        st.session_state[search_key] = ""
    
    # 搜索输入
    search_input = st.text_input(
        label,
        key=search_key,
        placeholder="输入城市名或拼音搜索...",
        help=help_text
    )
    
    if not search_input:
        # 未输入时显示提示
        st.caption("💡 输入城市名后将显示匹配结果")
        return ""
    
    # 搜索匹配的城市
    matched_cities = search_cities(search_input, limit=10)
    
    if not matched_cities:
        st.warning(f"未找到匹配 '{search_input}' 的城市")
        return ""
    
    # 构建选项列表
    options = [f"{c.name} ({c.province})" for c in matched_cities]
    
    # 下拉选择
    selected = st.selectbox(
        "选择城市",
        options=options,
        key=f"{key}_select",
        label_visibility="collapsed"
    )
    
    if selected:
        city_name = parse_city_option(selected)
        st.caption(f"✅ 已选择: {selected}")
        return city_name
    
    return ""


def render_city_selectbox(
    label: str = "出生地点（可选）",
    key: str = "city_box",
    include_empty: bool = True
) -> str:
    """
    渲染简化版城市选择框（直接下拉选择所有城市）
    
    适用于不需要搜索功能的场景
    
    Args:
        label: 标签文字
        key: 组件唯一标识
        include_empty: 是否包含空选项
    
    Returns:
        选中的城市名，未选择返回空字符串
    """
    options = get_all_city_options()
    if include_empty:
        options = ["（不选择）"] + options
    
    selected = st.selectbox(label, options=options, key=key)
    
    if selected and selected != "（不选择）":
        return parse_city_option(selected)
    return ""

