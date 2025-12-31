"""工具模块 - 通用工具函数和配置"""
from src.core.utils.cache import cached, get_cache, clear_cache, cache_stats
from src.core.utils.calendar import solar_to_lunar, get_jieqi_month
from src.core.utils.config import get_settings, Settings
from src.core.utils.logging import get_logger, setup_logging
from src.core.utils.solar_time import convert_to_true_solar_time, get_time_correction_info, Location
from src.core.utils.city_search import search_cities, get_location_smart as get_city_location
from src.core.utils.cities_data import CityInfo, get_all_cities, get_cities_by_name
from src.core.utils.exceptions import (
    FortuneTracerError,
    ValidationError,
    BirthInfoError,
    CalculationError,
    AIInterpretationError,
)

__all__ = [
    # 缓存
    "cached", "get_cache", "clear_cache", "cache_stats",
    # 历法
    "solar_to_lunar", "get_jieqi_month",
    # 配置
    "get_settings", "Settings",
    # 日志
    "get_logger", "setup_logging",
    # 太阳时
    "convert_to_true_solar_time", "get_time_correction_info", "Location",
    # 城市
    "search_cities", "get_city_location", "CityInfo", "get_all_cities", "get_cities_by_name",
    # 异常
    "FortuneTracerError", "ValidationError", "BirthInfoError",
    "CalculationError", "AIInterpretationError",
]

