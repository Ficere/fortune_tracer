"""紫微斗数模块"""
from .chart import calculate_ziwei_chart, get_hour_zhi
from .analysis import generate_ziwei_analysis
from .palace import (
    calculate_ming_gong_pos, calculate_shen_gong_pos,
    get_wuxing_ju, arrange_palaces
)
from .main_stars import (
    calculate_ziwei_position, get_ziwei_series_positions,
    get_tianfu_series_positions, arrange_main_stars
)
from .aux_stars import arrange_aux_sha_stars
from .sihua import get_sihua, apply_sihua_to_palaces, analyze_sihua_pattern

__all__ = [
    # 星盘计算
    "calculate_ziwei_chart",
    "generate_ziwei_analysis",
    "get_hour_zhi",
    # 宫位
    "calculate_ming_gong_pos",
    "calculate_shen_gong_pos",
    "get_wuxing_ju",
    "arrange_palaces",
    # 主星
    "calculate_ziwei_position",
    "get_ziwei_series_positions",
    "get_tianfu_series_positions",
    "arrange_main_stars",
    # 辅煞星
    "arrange_aux_sha_stars",
    # 四化
    "get_sihua",
    "apply_sihua_to_palaces",
    "analyze_sihua_pattern",
]

