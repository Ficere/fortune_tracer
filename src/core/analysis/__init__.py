"""专项分析模块"""
from src.core.analysis.compatibility import calculate_compatibility
from src.core.analysis.date_selection import select_dates
from src.core.analysis.bonefate import (
    calculate_bone_weight,
    get_bone_poem,
    get_weight_level,
    analyze_bonefate,
)

__all__ = [
    # 配对
    "calculate_compatibility",
    # 择日
    "select_dates",
    # 称骨算命
    "calculate_bone_weight", "get_bone_poem",
    "get_weight_level", "analyze_bonefate",
]

