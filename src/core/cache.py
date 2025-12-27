"""缓存模块

提供简单的内存缓存功能，用于缓存八字计算结果。
"""
import hashlib
import time
from functools import wraps
from typing import Any, Callable, Optional
from .config import get_settings


class SimpleCache:
    """简单的内存缓存实现"""
    
    def __init__(self, default_ttl: int = 3600):
        self._cache: dict[str, tuple[Any, float]] = {}
        self._default_ttl = default_ttl
    
    def _make_key(self, *args, **kwargs) -> str:
        """生成缓存键"""
        key_data = str(args) + str(sorted(kwargs.items()))
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def get(self, key: str) -> Optional[Any]:
        """获取缓存值"""
        if key in self._cache:
            value, expire_time = self._cache[key]
            if time.time() < expire_time:
                return value
            else:
                del self._cache[key]
        return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """设置缓存值"""
        expire_time = time.time() + (ttl or self._default_ttl)
        self._cache[key] = (value, expire_time)
    
    def delete(self, key: str) -> None:
        """删除缓存"""
        if key in self._cache:
            del self._cache[key]
    
    def clear(self) -> None:
        """清空缓存"""
        self._cache.clear()
    
    def cleanup(self) -> int:
        """清理过期缓存，返回清理数量"""
        now = time.time()
        expired_keys = [
            k for k, (_, expire_time) in self._cache.items()
            if expire_time <= now
        ]
        for key in expired_keys:
            del self._cache[key]
        return len(expired_keys)
    
    @property
    def size(self) -> int:
        """缓存大小"""
        return len(self._cache)


# 全局缓存实例
_cache: Optional[SimpleCache] = None


def get_cache() -> SimpleCache:
    """获取缓存实例"""
    global _cache
    if _cache is None:
        settings = get_settings()
        _cache = SimpleCache(default_ttl=settings.cache_ttl)
    return _cache


def cached(ttl: Optional[int] = None) -> Callable:
    """
    缓存装饰器
    
    使用方法:
        @cached(ttl=3600)
        def expensive_calculation(arg1, arg2):
            ...
    
    Args:
        ttl: 缓存过期时间（秒），None 使用默认值
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            settings = get_settings()
            if not settings.cache_enabled:
                return func(*args, **kwargs)
            
            cache = get_cache()
            key = f"{func.__module__}.{func.__name__}:" + cache._make_key(*args, **kwargs)
            
            # 尝试从缓存获取
            result = cache.get(key)
            if result is not None:
                return result
            
            # 计算并缓存
            result = func(*args, **kwargs)
            cache.set(key, result, ttl)
            return result
        
        return wrapper
    return decorator


def clear_cache() -> None:
    """清空全局缓存"""
    cache = get_cache()
    cache.clear()


def cache_stats() -> dict:
    """获取缓存统计信息"""
    cache = get_cache()
    return {
        "size": cache.size,
        "enabled": get_settings().cache_enabled,
        "default_ttl": get_settings().cache_ttl,
    }
