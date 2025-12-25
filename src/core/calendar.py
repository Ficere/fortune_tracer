"""农历转换模块"""
from datetime import datetime
from typing import NamedTuple
from lunarcalendar import Converter, Solar


class LunarDate(NamedTuple):
    """农历日期"""
    year: int
    month: int
    day: int
    is_leap: bool


def solar_to_lunar(dt: datetime) -> LunarDate:
    """公历转农历"""
    solar = Solar(dt.year, dt.month, dt.day)
    lunar = Converter.Solar2Lunar(solar)
    return LunarDate(
        year=lunar.year,
        month=lunar.month,
        day=lunar.day,
        is_leap=lunar.isleap
    )


def get_jieqi_month(dt: datetime) -> int:
    """
    根据节气获取月份（用于月柱计算）
    简化版本：基于固定日期判断节气月份
    """
    month = dt.month
    day = dt.day
    
    # 节气边界日期（简化版，实际应使用精确节气表）
    jieqi_boundaries = {
        1: 6,   # 小寒
        2: 4,   # 立春
        3: 6,   # 惊蛰
        4: 5,   # 清明
        5: 6,   # 立夏
        6: 6,   # 芒种
        7: 7,   # 小暑
        8: 8,   # 立秋
        9: 8,   # 白露
        10: 9,  # 寒露
        11: 8,  # 立冬
        12: 7,  # 大雪
    }
    
    boundary = jieqi_boundaries.get(month, 6)
    
    # 判断是否过了本月节气
    if day >= boundary:
        jieqi_month = month
    else:
        jieqi_month = month - 1 if month > 1 else 12
    
    # 转换为地支月（寅月为正月）
    return jieqi_month

