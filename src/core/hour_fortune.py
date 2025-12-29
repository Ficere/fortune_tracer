"""吉时推荐模块 - 分析12时辰运势"""
from datetime import date
from src.core.constants import (
    TIANGAN, DIZHI, TIANGAN_WUXING, DIZHI_LIUHE, DIZHI_LIUCHONG, DIZHI_XING
)
from src.models.bazi_models import BaziChart, WuxingAnalysis
from src.models.daily_fortune_models import HourFortune, get_fortune_level

# 时辰信息
HOUR_INFO = [
    ("子", "子时", "23:00-01:00"), ("丑", "丑时", "01:00-03:00"),
    ("寅", "寅时", "03:00-05:00"), ("卯", "卯时", "05:00-07:00"),
    ("辰", "辰时", "07:00-09:00"), ("巳", "巳时", "09:00-11:00"),
    ("午", "午时", "11:00-13:00"), ("未", "未时", "13:00-15:00"),
    ("申", "申时", "15:00-17:00"), ("酉", "酉时", "17:00-19:00"),
    ("戌", "戌时", "19:00-21:00"), ("亥", "亥时", "21:00-23:00"),
]

# 时辰天干推算（日干决定时干起点）
HOUR_GAN_START = {"甲": 0, "己": 0, "乙": 2, "庚": 2, "丙": 4, "辛": 4, "丁": 6, "壬": 6, "戊": 8, "癸": 8}

# 时辰适宜事项
HOUR_SUITABLE = {
    "吉": ["重要会议", "签约", "商务谈判", "面试", "开业"],
    "中": ["日常工作", "社交活动", "购物", "学习"],
    "凶": ["休息为主", "避免重大决策"],
}


def calculate_hour_fortunes(
    target_date: date, day_gan: str, bazi: BaziChart, wuxing: WuxingAnalysis
) -> list[HourFortune]:
    """计算当日12时辰运势"""
    favorable = [w.value for w in wuxing.favorable]
    unfavorable = [w.value for w in wuxing.unfavorable]
    
    bazi_zhis = [
        bazi.year_pillar.dizhi.value, bazi.month_pillar.dizhi.value,
        bazi.day_pillar.dizhi.value, bazi.hour_pillar.dizhi.value,
    ]
    
    results = []
    gan_start = HOUR_GAN_START.get(day_gan, 0)
    
    for i, (zhi, name, time_range) in enumerate(HOUR_INFO):
        hour_gan = TIANGAN[(gan_start + i) % 10]
        score = _calc_hour_score(hour_gan, zhi, favorable, unfavorable, bazi_zhis)
        level, emoji, _ = get_fortune_level(score)
        
        # 根据分数确定适宜事项
        if score >= 75:
            suitable = HOUR_SUITABLE["吉"]
        elif score >= 55:
            suitable = HOUR_SUITABLE["中"]
        else:
            suitable = HOUR_SUITABLE["凶"]
        
        results.append(HourFortune(
            hour_zhi=zhi, hour_name=name, time_range=time_range,
            score=round(score, 0), level=level, suitable=suitable
        ))
    
    return results


def _calc_hour_score(
    hour_gan: str, hour_zhi: str, favorable: list, unfavorable: list, bazi_zhis: list
) -> float:
    """计算时辰分数"""
    score = 60.0
    hour_wx = TIANGAN_WUXING[hour_gan]
    
    # 喜忌判断
    if hour_wx in favorable:
        score += 15
    elif hour_wx in unfavorable:
        score -= 12
    
    # 地支关系
    for zhi in bazi_zhis:
        pair = tuple(sorted([hour_zhi, zhi]))
        rev_pair = (pair[1], pair[0])
        
        if pair in DIZHI_LIUHE or rev_pair in DIZHI_LIUHE:
            score += 6
        if pair in DIZHI_LIUCHONG or rev_pair in DIZHI_LIUCHONG:
            score -= 8
        if pair in DIZHI_XING or rev_pair in DIZHI_XING:
            score -= 5
    
    return min(max(score, 20), 95)


def get_lucky_hours(hour_fortunes: list[HourFortune], top_n: int = 3) -> list[HourFortune]:
    """获取最吉利的N个时辰"""
    sorted_hours = sorted(hour_fortunes, key=lambda x: x.score, reverse=True)
    return sorted_hours[:top_n]


def get_unlucky_hours(hour_fortunes: list[HourFortune], bottom_n: int = 2) -> list[HourFortune]:
    """获取最不利的N个时辰"""
    sorted_hours = sorted(hour_fortunes, key=lambda x: x.score)
    return sorted_hours[:bottom_n]

