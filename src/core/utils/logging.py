"""日志管理模块

提供统一的日志配置和获取方式
"""
import logging
import sys
from typing import Optional
from src.core.utils.config import get_settings


# 日志器缓存
_loggers: dict[str, logging.Logger] = {}


def setup_logging() -> None:
    """初始化日志系统"""
    settings = get_settings()
    
    # 设置根日志器
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, settings.log_level.upper()))
    
    # 清除已有处理器
    root_logger.handlers.clear()
    
    # 创建格式化器
    formatter = logging.Formatter(settings.log_format)
    
    # 控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # 文件处理器（如果配置了）
    if settings.log_file:
        file_handler = logging.FileHandler(
            settings.log_file, encoding="utf-8"
        )
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)


def get_logger(name: str) -> logging.Logger:
    """
    获取指定名称的日志器
    
    Args:
        name: 日志器名称，通常使用 __name__
    
    Returns:
        配置好的日志器实例
    
    Example:
        >>> logger = get_logger(__name__)
        >>> logger.info("计算八字完成")
    """
    if name not in _loggers:
        settings = get_settings()
        logger = logging.getLogger(name)
        logger.setLevel(getattr(logging, settings.log_level.upper()))
        _loggers[name] = logger
    return _loggers[name]


class LoggerMixin:
    """日志器混入类
    
    为类提供便捷的日志访问
    
    Example:
        >>> class MyService(LoggerMixin):
        ...     def do_something(self):
        ...         self.logger.info("Doing something")
    """
    
    @property
    def logger(self) -> logging.Logger:
        if not hasattr(self, "_logger"):
            self._logger = get_logger(self.__class__.__name__)
        return self._logger
