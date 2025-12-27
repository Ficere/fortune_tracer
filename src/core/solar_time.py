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


# 中国主要城市经纬度
CHINA_CITIES = {
    "北京": Location("北京", 116.4074, 39.9042),
    "上海": Location("上海", 121.4737, 31.2304),
    "广州": Location("广州", 113.2644, 23.1291),
    "深圳": Location("深圳", 114.0579, 22.5431),
    "成都": Location("成都", 104.0657, 30.6595),
    "重庆": Location("重庆", 106.5516, 29.5630),
    "天津": Location("天津", 117.1901, 39.1256),
    "武汉": Location("武汉", 114.3055, 30.5928),
    "南京": Location("南京", 118.7969, 32.0603),
    "杭州": Location("杭州", 120.1536, 30.2875),
    "西安": Location("西安", 108.9402, 34.3416),
    "长沙": Location("长沙", 112.9388, 28.2282),
    "沈阳": Location("沈阳", 123.4315, 41.8057),
    "哈尔滨": Location("哈尔滨", 126.5346, 45.8038),
    "大连": Location("大连", 121.6147, 38.9140),
    "青岛": Location("青岛", 120.3826, 36.0671),
    "济南": Location("济南", 117.1209, 36.6512),
    "郑州": Location("郑州", 113.6254, 34.7466),
    "福州": Location("福州", 119.2965, 26.0745),
    "厦门": Location("厦门", 118.0894, 24.4798),
    "昆明": Location("昆明", 102.8329, 24.8801),
    "贵阳": Location("贵阳", 106.6302, 26.6477),
    "南宁": Location("南宁", 108.3661, 22.8170),
    "海口": Location("海口", 110.1999, 20.0444),
    "太原": Location("太原", 112.5489, 37.8706),
    "石家庄": Location("石家庄", 114.5149, 38.0428),
    "合肥": Location("合肥", 117.2272, 31.8206),
    "南昌": Location("南昌", 115.8579, 28.6820),
    "长春": Location("长春", 125.3235, 43.8171),
    "呼和浩特": Location("呼和浩特", 111.7490, 40.8424),
    "乌鲁木齐": Location("乌鲁木齐", 87.6177, 43.7928),
    "拉萨": Location("拉萨", 91.1322, 29.6600),
    "兰州": Location("兰州", 103.8343, 36.0611),
    "银川": Location("银川", 106.2309, 38.4872),
    "西宁": Location("西宁", 101.7782, 36.6171),
    "台北": Location("台北", 121.5654, 25.0330),
    "香港": Location("香港", 114.1095, 22.3964),
    "澳门": Location("澳门", 113.5439, 22.1987),
}

# 北京时间基准经度（东八区中央经线）
BEIJING_TIME_LONGITUDE = 120.0


def get_location(city_name: str) -> Location | None:
    """根据城市名获取位置信息"""
    # 直接匹配
    if city_name in CHINA_CITIES:
        return CHINA_CITIES[city_name]
    
    # 模糊匹配
    for name, loc in CHINA_CITIES.items():
        if name in city_name or city_name in name:
            return loc
    
    return None


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
