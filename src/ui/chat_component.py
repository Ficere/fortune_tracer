"""聊天组件 - 用于各功能页面的LLM对话"""
import os
import streamlit as st
from src.ai import Session, chat_with_llm


def render_chat_section(
    session: Session,
    api_key: str | None,
    feature: str,
    title: str = "🤖 AI对话"
):
    """渲染聊天区域

    Args:
        session: 会话对象
        api_key: OpenAI API Key
        feature: 功能类型
        title: 区域标题
    """
    st.subheader(title)

    # API Key缺失提示
    has_api_key = api_key or os.getenv("OPENAI_API_KEY")
    if not has_api_key:
        st.caption("💡 填写OpenAI API Key后可与AI对话，深入探讨分析结果")

    # 显示对话历史
    chat_container = st.container(height=300)
    with chat_container:
        if not session.messages:
            st.caption("💡 您可以询问关于分析结果的任何问题")
        else:
            for msg in session.messages:
                if msg.role == "user":
                    st.markdown(f"**🧑 您**: {msg.content}")
                else:
                    st.markdown(f"**🤖 AI**: {msg.content}")
    
    # 输入区域
    col1, col2 = st.columns([4, 1])
    with col1:
        user_input = st.text_input(
            "输入问题",
            key=f"chat_input_{feature}",
            placeholder="例如：我的八字有什么特点？",
            label_visibility="collapsed"
        )
    with col2:
        send_btn = st.button("发送", key=f"send_{feature}", use_container_width=True)
    
    # 发送消息
    if send_btn and user_input:
        if not api_key:
            st.warning("请先填写OpenAI API Key")
        else:
            with st.spinner("AI思考中..."):
                reply = chat_with_llm(session, user_input, api_key, feature)
            st.rerun()
    
    # 清空对话按钮
    if session.messages:
        if st.button("🗑️ 清空对话", key=f"clear_{feature}"):
            session.messages.clear()
            st.rerun()


def render_llm_interpretation(
    interpretation: str,
    title: str = "🔮 AI解读"
):
    """渲染LLM解读结果
    
    Args:
        interpretation: 解读文本
        title: 标题
    """
    st.subheader(title)
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        padding: 20px; border-radius: 12px; border-left: 4px solid #0ea5e9;'>
        {interpretation}
    </div>
    """, unsafe_allow_html=True)

