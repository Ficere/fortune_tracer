"""八字核心计算模块"""
from src.core.bazi.pillars import calculate_bazi
from src.core.bazi.wuxing import analyze_wuxing
from src.core.bazi.shishen import analyze_shishen, _get_shishen, _is_yang_gan
from src.core.bazi.shensha import calculate_shensha
from src.core.bazi.nayin import calculate_nayin, get_year_nayin, get_nayin, get_nayin_wuxing
from src.core.bazi.auxiliary import (
    calculate_ming_gong,
    calculate_tai_yuan,
    calculate_shen_gong,
    calculate_auxiliary,
    calculate_auxiliary_from_bazi,
)
from src.core.bazi.constants import (
    TIANGAN, DIZHI, TIANGAN_WUXING, DIZHI_WUXING,
    WUXING_SHENG, WUXING_KE, DIZHI_CANGAN,
    DIZHI_LIUHE, DIZHI_LIUCHONG, DIZHI_XING,
)

__all__ = [
    # 核心计算
    "calculate_bazi", "analyze_wuxing", "analyze_shishen",
    "calculate_shensha", "calculate_nayin", "get_year_nayin",
    # 内部函数（供其他模块使用）
    "_get_shishen", "_is_yang_gan", "get_nayin", "get_nayin_wuxing",
    # 辅助宫位
    "calculate_ming_gong", "calculate_tai_yuan", "calculate_shen_gong",
    "calculate_auxiliary", "calculate_auxiliary_from_bazi",
    # 常量
    "TIANGAN", "DIZHI", "TIANGAN_WUXING", "DIZHI_WUXING",
    "WUXING_SHENG", "WUXING_KE", "DIZHI_CANGAN",
    "DIZHI_LIUHE", "DIZHI_LIUCHONG", "DIZHI_XING",
]

