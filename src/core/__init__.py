"""核心计算模块"""
from .pillars import calculate_bazi
from .wuxing import analyze_wuxing
from .calendar import solar_to_lunar
from .compatibility import calculate_compatibility
from .date_selection import select_dates
from .dayun import calculate_dayun, get_current_dayun
from .shishen import analyze_shishen
from .shensha import calculate_shensha
from .nayin import calculate_nayin, get_year_nayin
from .liunian import calculate_liunian
from .jieqi import get_jieqi_month, is_before_lichun, get_jieqi_for_year
from .cache import cached, get_cache, clear_cache, cache_stats
from .solar_time import convert_to_true_solar_time, get_time_correction_info
from .config import get_settings, Settings
from .logging import get_logger, setup_logging
from .auxiliary import (
    calculate_ming_gong,
    calculate_tai_yuan,
    calculate_shen_gong,
    calculate_auxiliary,
    calculate_auxiliary_from_bazi,
)
from .exceptions import (
    FortuneTracerError,
    ValidationError,
    BirthInfoError,
    CalculationError,
    AIInterpretationError,
)

__all__ = [
    # 核心计算
    "calculate_bazi",
    "analyze_wuxing",
    "solar_to_lunar",
    "calculate_compatibility",
    "select_dates",
    "calculate_dayun",
    "get_current_dayun",
    "analyze_shishen",
    "calculate_shensha",
    "calculate_nayin",
    "get_year_nayin",
    "calculate_liunian",
    # 辅助宫位
    "calculate_ming_gong",
    "calculate_tai_yuan",
    "calculate_shen_gong",
    "calculate_auxiliary",
    "calculate_auxiliary_from_bazi",
    # 节气和时间
    "get_jieqi_month",
    "is_before_lichun",
    "get_jieqi_for_year",
    "convert_to_true_solar_time",
    "get_time_correction_info",
    # 缓存
    "cached",
    "get_cache",
    "clear_cache",
    "cache_stats",
    # 配置和日志
    "get_settings",
    "Settings",
    "get_logger",
    "setup_logging",
    # 异常
    "FortuneTracerError",
    "ValidationError",
    "BirthInfoError",
    "CalculationError",
    "AIInterpretationError",
]

