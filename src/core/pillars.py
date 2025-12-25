"""四柱计算模块"""
from datetime import datetime
from src.models import BaziPillar, BaziChart, Gender
from src.models.bazi_models import TianGan, DiZhi
from .constants import TIANGAN, DIZHI
from .calendar import get_jieqi_month


def _get_year_pillar(year: int, month: int, day: int) -> BaziPillar:
    """计算年柱（以立春为界）"""
    # 简化判断：2月4日前算上一年
    if month < 2 or (month == 2 and day < 4):
        year -= 1
    
    # 年干支计算：以1984年甲子年为基准
    gan_idx = (year - 4) % 10
    zhi_idx = (year - 4) % 12
    
    return BaziPillar(
        tiangan=TianGan(TIANGAN[gan_idx]),
        dizhi=DiZhi(DIZHI[zhi_idx])
    )


def _get_month_pillar(year_gan: str, month: int, day: int) -> BaziPillar:
    """
    计算月柱
    月柱地支固定：寅卯辰巳午未申酉戌亥子丑
    月柱天干由年干推算
    """
    jieqi_month = get_jieqi_month(datetime(2000, month, day))
    
    # 月支对应表（正月=寅）
    month_zhi_map = {
        1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 7,
        7: 8, 8: 9, 9: 10, 10: 11, 11: 0, 12: 1
    }
    zhi_idx = month_zhi_map.get(jieqi_month, 2)
    
    # 年干定月干口诀
    year_gan_idx = TIANGAN.index(year_gan)
    start_gan = (year_gan_idx % 5) * 2 + 2
    gan_idx = (start_gan + jieqi_month - 1) % 10
    
    return BaziPillar(
        tiangan=TianGan(TIANGAN[gan_idx]),
        dizhi=DiZhi(DIZHI[zhi_idx])
    )


def _get_day_pillar(dt: datetime) -> BaziPillar:
    """
    计算日柱
    使用高氏日柱公式简化版
    """
    year = dt.year
    month = dt.month
    day = dt.day
    
    # 世纪常数
    century = year // 100
    c_const = (century // 4 - century - 2) % 60
    
    # 年份尾数
    y = year % 100
    y_const = (5 * y + y // 4) % 60
    
    # 月份常数
    month_const = [0, 0, 31, -1, 30, 0, 31, 1, 32, 3, 33, 4, 34]
    m_const = month_const[month]
    
    # 闰年修正
    is_leap = (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
    if is_leap and month <= 2:
        m_const -= 1
    
    total = (c_const + y_const + m_const + day) % 60
    if total <= 0:
        total += 60
    
    gan_idx = (total - 1) % 10
    zhi_idx = (total - 1) % 12
    
    return BaziPillar(
        tiangan=TianGan(TIANGAN[gan_idx]),
        dizhi=DiZhi(DIZHI[zhi_idx])
    )


def _get_hour_pillar(day_gan: str, hour: int) -> BaziPillar:
    """
    计算时柱
    时支由时辰确定，时干由日干推算
    """
    # 时辰地支（23-1点为子时）
    hour_adjusted = (hour + 1) % 24
    zhi_idx = hour_adjusted // 2
    
    # 日干定时干
    day_gan_idx = TIANGAN.index(day_gan)
    start_gan = (day_gan_idx % 5) * 2
    gan_idx = (start_gan + zhi_idx) % 10
    
    return BaziPillar(
        tiangan=TianGan(TIANGAN[gan_idx]),
        dizhi=DiZhi(DIZHI[zhi_idx])
    )


def calculate_bazi(
    birth_dt: datetime,
    gender: Gender,
    birth_place: str | None = None
) -> BaziChart:
    """计算完整八字"""
    year_pillar = _get_year_pillar(birth_dt.year, birth_dt.month, birth_dt.day)
    month_pillar = _get_month_pillar(
        year_pillar.tiangan.value, birth_dt.month, birth_dt.day
    )
    day_pillar = _get_day_pillar(birth_dt)
    hour_pillar = _get_hour_pillar(day_pillar.tiangan.value, birth_dt.hour)
    
    return BaziChart(
        year_pillar=year_pillar,
        month_pillar=month_pillar,
        day_pillar=day_pillar,
        hour_pillar=hour_pillar,
        birth_datetime=birth_dt,
        gender=gender,
        birth_place=birth_place
    )

