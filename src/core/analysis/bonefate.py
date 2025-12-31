"""称骨算命核心逻辑 - 袁天罡八字称骨算命

计算骨重并返回对应的命运诗词
"""

from decimal import Decimal
from datetime import datetime
from lunarcalendar import Converter, Lunar, Solar

from src.core.analysis.bonefate_data import (
    BONE_WEIGHT_POEMS, YEAR_WEIGHT_MATRIX, MONTH_WEIGHT,
    DAY_WEIGHT, HOUR_WEIGHT, DIZHI_INDEX, WEIGHT_LEVELS
)


def get_tiangan_index(year: int) -> int:
    """获取年份的天干索引 (0-9)"""
    return (year - 4) % 10


def get_dizhi_index(year: int) -> int:
    """获取年份的地支索引 (0-11)"""
    return (year - 4) % 12


def get_hour_dizhi_index(hour: int) -> int:
    """根据小时获取时辰地支索引 (0-11)
    
    Args:
        hour: 24小时制的小时数 (0-23)
    
    Returns:
        时辰地支索引
    """
    # 子时 23:00-00:59, 丑时 01:00-02:59, ...
    if hour == 23:
        return 0  # 子
    return (hour + 1) // 2


def solar_to_lunar(year: int, month: int, day: int) -> tuple[int, int, int]:
    """将阳历转换为农历
    
    Returns:
        (农历年, 农历月, 农历日)
    """
    solar = Solar(year, month, day)
    lunar = Converter.Solar2Lunar(solar)
    return lunar.year, lunar.month, lunar.day


def calculate_bone_weight(
    year: int, month: int, day: int, hour: int, is_lunar: bool = False
) -> float:
    """计算骨重
    
    Args:
        year: 年份
        month: 月份
        day: 日期
        hour: 时辰 (24小时制)
        is_lunar: 是否为农历日期
    
    Returns:
        骨重 (单位：两)
    """
    # 转换为农历
    if is_lunar:
        lunar_year, lunar_month, lunar_day = year, month, day
    else:
        lunar_year, lunar_month, lunar_day = solar_to_lunar(year, month, day)
    
    # 计算各部分骨重
    tiangan_idx = get_tiangan_index(lunar_year)
    dizhi_idx = get_dizhi_index(lunar_year)
    year_weight = YEAR_WEIGHT_MATRIX[dizhi_idx][tiangan_idx]
    
    month_weight = MONTH_WEIGHT[lunar_month - 1]
    day_weight = DAY_WEIGHT[lunar_day - 1]
    
    hour_idx = get_hour_dizhi_index(hour)
    hour_weight = HOUR_WEIGHT[hour_idx]
    
    # 使用 Decimal 精确计算避免浮点数误差
    total = sum(
        Decimal(str(w)) for w in [year_weight, month_weight, day_weight, hour_weight]
    )
    return float(total)


def get_bone_poem(weight: float) -> dict:
    """根据骨重获取对应的命运诗词
    
    Args:
        weight: 骨重 (单位：两)
    
    Returns:
        包含 title 和 poem 的字典
    """
    # 将骨重四舍五入到一位小数
    rounded_weight = round(weight, 1)
    
    # 查找对应的诗词
    if rounded_weight in BONE_WEIGHT_POEMS:
        return BONE_WEIGHT_POEMS[rounded_weight]
    
    # 如果找不到精确匹配，找最接近的
    weights = sorted(BONE_WEIGHT_POEMS.keys())
    closest = min(weights, key=lambda x: abs(x - rounded_weight))
    return BONE_WEIGHT_POEMS[closest]


def get_weight_level(weight: float) -> dict:
    """根据骨重获取等级评价
    
    Args:
        weight: 骨重 (单位：两)
    
    Returns:
        包含 level 和 desc 的字典
    """
    for (low, high), info in WEIGHT_LEVELS.items():
        if low <= weight < high:
            return info
    # 默认返回中等
    return {"level": "中", "desc": "中等福禄，平稳一生"}


def analyze_bonefate(
    birth_datetime: datetime, is_lunar: bool = False
) -> dict:
    """完整的称骨算命分析
    
    Args:
        birth_datetime: 出生日期时间
        is_lunar: 是否为农历
    
    Returns:
        完整的称骨算命结果
    """
    year = birth_datetime.year
    month = birth_datetime.month
    day = birth_datetime.day
    hour = birth_datetime.hour
    
    # 计算骨重
    weight = calculate_bone_weight(year, month, day, hour, is_lunar)
    
    # 获取诗词和等级
    poem_info = get_bone_poem(weight)
    level_info = get_weight_level(weight)
    
    # 获取农历日期用于显示
    if is_lunar:
        lunar_year, lunar_month, lunar_day = year, month, day
    else:
        lunar_year, lunar_month, lunar_day = solar_to_lunar(year, month, day)
    
    # 时辰名称
    dizhi_names = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    hour_name = dizhi_names[get_hour_dizhi_index(hour)]
    
    return {
        "weight": weight,
        "weight_display": f"{weight:.1f}两",
        "level": level_info["level"],
        "level_desc": level_info["desc"],
        "title": poem_info["title"],
        "poem": poem_info["poem"],
        "lunar_date": {
            "year": lunar_year,
            "month": lunar_month,
            "day": lunar_day,
            "hour": hour_name,
        },
        "solar_date": {
            "year": birth_datetime.year,
            "month": birth_datetime.month,
            "day": birth_datetime.day,
            "hour": hour,
        },
    }
