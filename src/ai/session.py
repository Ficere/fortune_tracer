"""会话管理模块 - 管理对话记忆和分析结果"""
import uuid
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Message:
    """对话消息"""
    role: str  # "user" or "assistant"
    content: str


@dataclass
class Session:
    """会话workspace，保存对话记忆和分析结果"""
    session_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    messages: list[Message] = field(default_factory=list)
    analysis_context: dict[str, Any] = field(default_factory=dict)
    
    def add_message(self, role: str, content: str):
        """添加消息到对话历史"""
        self.messages.append(Message(role=role, content=content))
    
    def get_messages_for_api(self) -> list[dict]:
        """获取API格式的消息列表"""
        return [{"role": m.role, "content": m.content} for m in self.messages]
    
    def set_context(self, key: str, value: Any):
        """设置分析上下文"""
        self.analysis_context[key] = value
    
    def get_context(self, key: str) -> Any | None:
        """获取分析上下文"""
        return self.analysis_context.get(key)
    
    def build_system_prompt(self, feature: str) -> str:
        """根据功能和上下文构建系统提示"""
        base = "你是一位资深的命理学专家，擅长生辰八字分析。请用通俗易懂的语言解答用户问题。"
        
        context_parts = []
        if self.analysis_context:
            context_parts.append("\n当前分析结果：")
            for key, value in self.analysis_context.items():
                if isinstance(value, str):
                    context_parts.append(f"- {key}: {value}")
                elif hasattr(value, '__dict__'):
                    context_parts.append(f"- {key}: {_format_obj(value)}")
        
        return base + "".join(context_parts)
    
    def clear(self):
        """清空会话"""
        self.messages.clear()
        self.analysis_context.clear()


def _format_obj(obj: Any) -> str:
    """格式化对象为字符串"""
    if hasattr(obj, 'display'):
        return str(obj.display)
    if hasattr(obj, 'value'):
        return str(obj.value)
    return str(obj)[:100]


def get_or_create_session(st_session_state, feature: str) -> Session:
    """从streamlit session_state获取或创建Session"""
    key = f"session_{feature}"
    if key not in st_session_state:
        st_session_state[key] = Session()
    return st_session_state[key]

