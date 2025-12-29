"""AI分析配置管理模块"""
import os
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class AIConfig:
    """AI分析配置"""
    # API设置
    api_key: Optional[str] = None
    base_url: Optional[str] = None  # 支持兼容接口
    model: str = "gpt-4o-mini"
    
    # 请求设置
    timeout: int = 30
    max_retries: int = 2
    temperature: float = 0.7
    max_tokens: int = 2000
    
    # 功能开关
    enabled: bool = True
    use_json_mode: bool = True
    
    @classmethod
    def from_env(cls) -> "AIConfig":
        """从环境变量加载配置"""
        return cls(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_BASE_URL"),
            model=os.getenv("AI_MODEL", "gpt-4o-mini"),
            timeout=int(os.getenv("AI_TIMEOUT", "30")),
            max_retries=int(os.getenv("AI_MAX_RETRIES", "2")),
            temperature=float(os.getenv("AI_TEMPERATURE", "0.7")),
            max_tokens=int(os.getenv("AI_MAX_TOKENS", "2000")),
            enabled=os.getenv("AI_ENABLED", "true").lower() == "true",
            use_json_mode=os.getenv("AI_JSON_MODE", "true").lower() == "true",
        )
    
    def with_api_key(self, api_key: str) -> "AIConfig":
        """创建带有指定API Key的新配置"""
        return AIConfig(
            api_key=api_key,
            base_url=self.base_url,
            model=self.model,
            timeout=self.timeout,
            max_retries=self.max_retries,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            enabled=self.enabled,
            use_json_mode=self.use_json_mode,
        )
    
    def is_valid(self) -> bool:
        """检查配置是否有效"""
        return bool(self.api_key) and self.enabled


# 全局默认配置（延迟加载）
_default_config: Optional[AIConfig] = None


def get_ai_config() -> AIConfig:
    """获取全局AI配置"""
    global _default_config
    if _default_config is None:
        _default_config = AIConfig.from_env()
    return _default_config


def reset_ai_config():
    """重置全局配置（用于测试）"""
    global _default_config
    _default_config = None

