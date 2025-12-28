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
.feature-card { padding: 15px; border-radius: 10px; background: #f8fafc; margin: 5px 0; }
</style>
""", unsafe_allow_html=True)

# 初始化session state
if "api_key" not in st.session_state:
    st.session_state.api_key = ""
if "current_mode" not in st.session_state:
    st.session_state.current_mode = "🔮 个人八字"
if "analyzed" not in st.session_state:
    st.session_state.analyzed = False

# 左侧边栏 - 功能选择
with st.sidebar:
    st.markdown("## 🔮 Fortune Tracer")
    st.caption("生辰八字 AI 智能解读")
    st.divider()

    # 功能选择
    st.markdown("### 功能选择")
    mode = st.radio(
        "选择功能",
        ["🔮 个人八字", "💑 配对分析", "📅 择日", "⚖️ 称骨算命"],
        label_visibility="collapsed"
    )
    st.session_state.current_mode = mode

    st.divider()

    # 全局设置
    st.markdown("### ⚙️ 设置")
    api_key = st.text_input(
        "OpenAI API Key",
        value=st.session_state.api_key,
        type="password",
        help="用于AI解读和对话功能"
    )
    st.session_state.api_key = api_key

    st.divider()
    st.caption("💡 填写信息后点击分析按钮")

# 主内容区 - 输入表单和结果展示
st.markdown("<h1 class='main-title'>🔮 Fortune Tracer</h1>", unsafe_allow_html=True)

# 根据功能渲染不同的输入表单
from src.ui.forms import render_form
render_form(mode, api_key)

