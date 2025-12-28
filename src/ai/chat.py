"""LLM对话模块 - 处理带上下文的对话"""
import os
from openai import OpenAI
from .session import Session


def chat_with_llm(
    session: Session,
    user_message: str,
    api_key: str | None = None,
    feature: str = "general"
) -> str:
    """与LLM对话，保持上下文
    
    Args:
        session: 会话对象
        user_message: 用户消息
        api_key: OpenAI API Key
        feature: 功能类型（bazi/compatibility/date_selection/bonefate）
    
    Returns:
        LLM回复
    """
    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        return "请提供OpenAI API Key以启用AI对话功能。"
    
    # 添加用户消息
    session.add_message("user", user_message)
    
    # 构建消息列表
    system_prompt = session.build_system_prompt(feature)
    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(session.get_messages_for_api())
    
    try:
        client = OpenAI(api_key=key)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.7,
            max_tokens=1000
        )
        reply = response.choices[0].message.content
        session.add_message("assistant", reply)
        return reply
    except Exception as e:
        error_msg = f"对话出错: {str(e)}"
        session.messages.pop()  # 移除失败的用户消息
        return error_msg


def interpret_result(
    context_data: dict,
    api_key: str | None = None,
    feature: str = "bazi"
) -> str:
    """对分析结果进行LLM解读
    
    Args:
        context_data: 分析结果数据
        api_key: OpenAI API Key
        feature: 功能类型
    
    Returns:
        LLM解读结果
    """
    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        return _get_default_interpretation(feature)
    
    prompt = _build_interpret_prompt(context_data, feature)
    
    try:
        client = OpenAI(api_key=key)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "你是命理学专家，请用通俗易懂的语言进行解读。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=800
        )
        return response.choices[0].message.content
    except Exception:
        return _get_default_interpretation(feature)


def _build_interpret_prompt(data: dict, feature: str) -> str:
    """构建解读提示词"""
    prompts = {
        "bazi": "请解读以下八字分析结果，给出综合建议：\n",
        "compatibility": "请解读以下配对分析结果，给出关系建议：\n",
        "date_selection": "请解读以下择日分析结果，给出选择建议：\n",
        "bonefate": "请解读以下称骨算命结果，给出人生建议：\n"
    }
    base = prompts.get(feature, "请解读以下分析结果：\n")
    
    content_parts = []
    for key, value in data.items():
        if isinstance(value, str):
            content_parts.append(f"{key}: {value}")
        elif isinstance(value, (int, float)):
            content_parts.append(f"{key}: {value}")
    
    return base + "\n".join(content_parts)


def _get_default_interpretation(feature: str) -> str:
    """默认解读（无API时）"""
    defaults = {
        "bazi": "八字分析已完成。如需AI深度解读，请提供OpenAI API Key。",
        "compatibility": "配对分析已完成。如需AI深度解读，请提供OpenAI API Key。",
        "date_selection": "择日分析已完成。如需AI深度解读，请提供OpenAI API Key。",
        "bonefate": "称骨分析已完成。如需AI深度解读，请提供OpenAI API Key。"
    }
    return defaults.get(feature, "分析已完成。如需AI解读，请提供OpenAI API Key。")

