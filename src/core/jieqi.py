"""精确节气计算模块

使用天文算法计算二十四节气的精确时间
节气是根据太阳黄经位置确定的
"""
from datetime import datetime, timedelta
from typing import NamedTuple
import ephem
import math


class JieQiInfo(NamedTuple):
    """节气信息"""
    name: str           # 节气名称
    solar_longitude: int  # 太阳黄经度数
    datetime: datetime  # 精确时间


# 二十四节气对应的太阳黄经度数和名称
JIEQI_TABLE = [
    (315, "立春"), (330, "雨水"), (345, "惊蛰"), (0, "春分"),
    (15, "清明"), (30, "谷雨"), (45, "立夏"), (60, "小满"),
    (75, "芒种"), (90, "夏至"), (105, "小暑"), (120, "大暑"),
    (135, "立秋"), (150, "处暑"), (165, "白露"), (180, "秋分"),
    (195, "寒露"), (210, "霜降"), (225, "立冬"), (240, "小雪"),
    (255, "大雪"), (270, "冬至"), (285, "小寒"), (300, "大寒"),
]

# 节（用于确定月柱的节气，每月第一个节气）
JIE_NAMES = [
    "立春", "惊蛰", "清明", "立夏", "芒种", "小暑",
    "立秋", "白露", "寒露", "立冬", "大雪", "小寒"
]


def _get_sun_longitude(dt: datetime) -> float:
    """获取指定时间的太阳黄经（度）"""
    # 转换为ephem时间
    sun = ephem.Sun()
    observer = ephem.Observer()
    observer.date = ephem.Date(dt)
    sun.compute(observer)
    
    # 获取黄经（弧度转度数）
    longitude = float(sun.hlong) * 180.0 / math.pi
    return longitude % 360


def _find_jieqi_moment(year: int, target_longitude: float) -> datetime:
    """
    查找指定太阳黄经对应的精确时刻
    使用二分法逼近
    """
    # 估算初始日期
    if target_longitude == 315:  # 立春
        start = datetime(year, 2, 1)
    elif target_longitude == 0:  # 春分
        start = datetime(year, 3, 18)
    elif target_longitude == 90:  # 夏至
        start = datetime(year, 6, 18)
    elif target_longitude == 180:  # 秋分
        start = datetime(year, 9, 20)
    elif target_longitude == 270:  # 冬至
        start = datetime(year, 12, 18)
    else:
        # 根据黄经估算日期
        day_of_year = int((target_longitude / 360) * 365) + 80
        if day_of_year > 365:
            day_of_year -= 365
        start = datetime(year, 1, 1) + timedelta(days=day_of_year)
    
    # 二分法搜索
    low = start - timedelta(days=15)
    high = start + timedelta(days=15)
    
    for _ in range(50):  # 迭代50次足够精确到分钟
        mid = low + (high - low) / 2
        lon = _get_sun_longitude(mid)
        
        # 处理0度附近的跨界情况
        diff = lon - target_longitude
        if diff > 180:
            diff -= 360
        elif diff < -180:
            diff += 360
        
        if abs(diff) < 0.0001:  # 精度约为秒级
            return mid
        elif diff > 0:
            high = mid
        else:
            low = mid
    
    return mid


def get_jieqi_for_year(year: int) -> list[JieQiInfo]:
    """获取指定年份的所有节气"""
    jieqi_list = []
    
    for longitude, name in JIEQI_TABLE:
        # 冬至、小寒、大寒可能跨年
        if longitude >= 270:
            # 可能在前一年末或本年初
            dt = _find_jieqi_moment(year, longitude)
            if dt.month > 6:  # 属于前一年
                dt = _find_jieqi_moment(year + 1, longitude)
        else:
            dt = _find_jieqi_moment(year, longitude)
        
        jieqi_list.append(JieQiInfo(
            name=name,
            solar_longitude=longitude,
            datetime=dt
        ))
    
    # 按日期排序
    jieqi_list.sort(key=lambda x: x.datetime)
    return jieqi_list


def get_jie_for_month(year: int, month: int) -> JieQiInfo:
    """
    获取指定月份的节（用于月柱计算）
    返回该月的节气精确时间
    """
    # 月份对应的节气索引（立春开始）
    jie_index_map = {
        2: 0,   # 立春 -> 寅月
        3: 2,   # 惊蛰 -> 卯月
        4: 4,   # 清明 -> 辰月
        5: 6,   # 立夏 -> 巳月
        6: 8,   # 芒种 -> 午月
        7: 10,  # 小暑 -> 未月
        8: 12,  # 立秋 -> 申月
        9: 14,  # 白露 -> 酉月
        10: 16, # 寒露 -> 戌月
        11: 18, # 立冬 -> 亥月
        12: 20, # 大雪 -> 子月
        1: 22,  # 小寒 -> 丑月
    }
    
    idx = jie_index_map.get(month, 0)
    longitude, name = JIEQI_TABLE[idx % 24]
    
    # 1月的小寒可能在上一年
    target_year = year if month > 1 else year
    dt = _find_jieqi_moment(target_year, longitude)
    
    return JieQiInfo(name=name, solar_longitude=longitude, datetime=dt)


def get_jieqi_month(dt: datetime) -> int:
    """
    根据精确节气计算月份（用于月柱）
    返回农历月份（1-12，其中1=寅月）
    """
    year = dt.year
    
    # 获取当年所有节气
    jieqi_list = get_jieqi_for_year(year)
    
    # 找到dt之前最近的"节"
    current_jie = None
    for jq in jieqi_list:
        if jq.name in JIE_NAMES and jq.datetime <= dt:
            current_jie = jq
    
    # 如果在立春之前，检查前一年的节气
    if current_jie is None or dt < jieqi_list[0].datetime:
        prev_jieqi = get_jieqi_for_year(year - 1)
        for jq in reversed(prev_jieqi):
            if jq.name in JIE_NAMES and jq.datetime <= dt:
                current_jie = jq
                break
    
    if current_jie is None:
        # 默认返回丑月
        return 12
    
    # 节气名称到月份的映射
    jie_to_month = {
        "立春": 1, "惊蛰": 2, "清明": 3, "立夏": 4,
        "芒种": 5, "小暑": 6, "立秋": 7, "白露": 8,
        "寒露": 9, "立冬": 10, "大雪": 11, "小寒": 12
    }
    
    return jie_to_month.get(current_jie.name, 1)


def is_before_lichun(dt: datetime) -> bool:
    """判断日期是否在立春之前（用于年柱计算）"""
    year = dt.year
    lichun = _find_jieqi_moment(year, 315)  # 立春黄经315度
    return dt < lichun
