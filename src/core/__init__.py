"""核心计算模块 - 模块化重构版本

按功能域组织：
- bazi/: 八字核心计算（四柱、五行、十神、神煞、纳音、辅助宫位）
- fortune/: 运势分析（大运、流年、每日运势、吉时）
- analysis/: 专项分析（配对、择日、称骨算命）
- ziwei/: 紫微斗数（星盘计算、宫位分析）
- utils/: 工具模块（配置、日志、缓存、历法、城市）
"""
# 八字核心计算
from src.core.bazi import (
    calculate_bazi, analyze_wuxing, analyze_shishen,
    calculate_shensha, calculate_nayin, get_year_nayin,
    calculate_ming_gong, calculate_tai_yuan, calculate_shen_gong,
    calculate_auxiliary, calculate_auxiliary_from_bazi,
)
# 运势分析
from src.core.fortune import (
    calculate_dayun, get_current_dayun, calculate_liunian,
    get_jieqi_month, is_before_lichun, get_jieqi_for_year,
    calculate_daily_fortune, calculate_three_days_fortune,
    generate_daily_fortune_report, calculate_hour_fortunes, get_lucky_hours,
    generate_year_detail, generate_dayun_detail,
)
# 专项分析
from src.core.analysis import (
    calculate_compatibility, select_dates,
    calculate_bone_weight, get_bone_poem, get_weight_level, analyze_bonefate,
)
# 工具模块
from src.core.utils import (
    solar_to_lunar, cached, get_cache, clear_cache, cache_stats,
    convert_to_true_solar_time, get_time_correction_info,
    get_settings, Settings, get_logger, setup_logging,
    FortuneTracerError, ValidationError, BirthInfoError,
    CalculationError, AIInterpretationError,
)
# 紫微斗数
from src.core.ziwei import calculate_ziwei_chart, generate_ziwei_analysis

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
    # 称骨算命
    "calculate_bone_weight",
    "get_bone_poem",
    "get_weight_level",
    "analyze_bonefate",
    # 运势解读
    "generate_year_detail",
    "generate_dayun_detail",
    # 每日运势
    "calculate_daily_fortune",
    "calculate_three_days_fortune",
    "generate_daily_fortune_report",
    "calculate_hour_fortunes",
    "get_lucky_hours",
    # 紫微斗数
    "calculate_ziwei_chart",
    "generate_ziwei_analysis",
]

