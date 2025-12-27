"""配置管理模块

支持从环境变量和配置文件加载配置
"""
import os
from pathlib import Path
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """应用配置"""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # 应用基础配置
    app_name: str = Field(default="Fortune Tracer", description="应用名称")
    app_version: str = Field(default="0.1.0", description="应用版本")
    debug: bool = Field(default=False, description="调试模式")
    
    # API 配置
    api_host: str = Field(default="0.0.0.0", description="API服务地址")
    api_port: int = Field(default=8000, description="API服务端口")
    api_base_url: str = Field(
        default="http://localhost:8000",
        description="API基础URL（前端使用）"
    )
    
    # OpenAI 配置
    openai_api_key: Optional[str] = Field(default=None, description="OpenAI API Key")
    openai_model: str = Field(default="gpt-4o-mini", description="OpenAI模型")
    openai_timeout: int = Field(default=30, description="OpenAI请求超时(秒)")
    
    # 日志配置
    log_level: str = Field(default="INFO", description="日志级别")
    log_format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        description="日志格式"
    )
    log_file: Optional[str] = Field(default=None, description="日志文件路径")
    
    # 缓存配置
    cache_enabled: bool = Field(default=True, description="启用缓存")
    cache_ttl: int = Field(default=3600, description="缓存过期时间(秒)")
    
    # 计算配置
    use_true_solar_time: bool = Field(
        default=True,
        description="是否使用真太阳时"
    )
    use_precise_jieqi: bool = Field(
        default=True,
        description="是否使用精确节气计算"
    )
    default_dayun_count: int = Field(default=8, description="默认大运数量")
    default_year_fortune_count: int = Field(default=10, description="默认流年数量")


# 全局配置实例
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """获取配置实例（单例模式）"""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings


def reload_settings() -> Settings:
    """重新加载配置"""
    global _settings
    _settings = Settings()
    return _settings
