"""真太阳时转换模块

真太阳时 = 地方平太阳时 + 时差（均时差）

地方平太阳时考虑经度差异
均时差考虑地球公转轨道椭圆和地轴倾斜
"""
from datetime import datetime, timedelta
from typing import NamedTuple
import math


class Location(NamedTuple):
    """地理位置"""
    name: str
    longitude: float  # 经度（东经为正）
    latitude: float   # 纬度（北纬为正）


# 北京时间基准经度（东八区中央经线）
BEIJING_TIME_LONGITUDE = 120.0


def get_location(city_name: str) -> Location | None:
    """
    根据城市名获取位置信息

    使用智能搜索，支持模糊匹配和拼音匹配
    """
    from .city_search import get_location_smart
    return get_location_smart(city_name)


def _calculate_equation_of_time(day_of_year: int) -> float:
    """
    计算均时差（分钟）
    
    均时差由两个因素引起：
    1. 地球公转轨道是椭圆
    2. 地轴相对于公转平面有倾斜
    """
    # 将日期转换为角度
    b = 2 * math.pi * (day_of_year - 81) / 365
    
    # 均时差公式（分钟）
    eot = (9.87 * math.sin(2 * b) 
           - 7.53 * math.cos(b) 
           - 1.5 * math.sin(b))
    
    return eot


def _calculate_longitude_correction(longitude: float) -> float:
    """
    计算经度修正（分钟）
    
    每度经度对应4分钟时差
    """
    delta_longitude = longitude - BEIJING_TIME_LONGITUDE
    return delta_longitude * 4  # 分钟


def convert_to_true_solar_time(
    local_time: datetime,
    location: Location | str | None = None
) -> datetime:
    """
    将北京时间转换为真太阳时
    
    Args:
        local_time: 北京时间
        location: 地点（城市名或Location对象）
    
    Returns:
        真太阳时
    """
    if location is None:
        # 不进行转换
        return local_time
    
    # 解析位置
    if isinstance(location, str):
        loc = get_location(location)
        if loc is None:
            # 未知城市，不转换
            return local_time
    else:
        loc = location
    
    # 计算年内第几天
    day_of_year = local_time.timetuple().tm_yday
    
    # 经度修正（分钟）
    longitude_correction = _calculate_longitude_correction(loc.longitude)
    
    # 均时差（分钟）
    equation_of_time = _calculate_equation_of_time(day_of_year)
    
    # 总修正（分钟）
    total_correction = longitude_correction + equation_of_time
    
    # 应用修正
    true_solar_time = local_time + timedelta(minutes=total_correction)
    
    return true_solar_time


def get_time_correction_info(
    local_time: datetime,
    location: str
) -> dict:
    """
    获取时间修正详情
    
    Returns:
        包含各项修正值的字典
    """
    loc = get_location(location)
    if loc is None:
        return {
            "location": location,
            "found": False,
            "message": "未找到城市信息，无法计算真太阳时"
        }
    
    day_of_year = local_time.timetuple().tm_yday
    longitude_correction = _calculate_longitude_correction(loc.longitude)
    equation_of_time = _calculate_equation_of_time(day_of_year)
    total_correction = longitude_correction + equation_of_time
    true_solar_time = local_time + timedelta(minutes=total_correction)
    
    return {
        "location": loc.name,
        "found": True,
        "longitude": loc.longitude,
        "latitude": loc.latitude,
        "longitude_correction_minutes": round(longitude_correction, 1),
        "equation_of_time_minutes": round(equation_of_time, 1),
        "total_correction_minutes": round(total_correction, 1),
        "local_time": local_time.strftime("%Y-%m-%d %H:%M:%S"),
        "true_solar_time": true_solar_time.strftime("%Y-%m-%d %H:%M:%S"),
    }
