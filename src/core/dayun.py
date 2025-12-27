"""大运计算模块"""
from datetime import datetime
from src.models import BaziChart, Gender
from src.models.bazi_models import DaYun, DaYunInfo
from .constants import TIANGAN, DIZHI, TIANGAN_WUXING


def _get_dayun_direction(year_gan: str, gender: Gender) -> int:
    """
    确定大运顺逆
    阳年男命、阴年女命顺行
    阴年男命、阳年女命逆行
    """
    gan_idx = TIANGAN.index(year_gan)
    is_yang_year = gan_idx % 2 == 0  # 甲丙戊庚壬为阳
    
    if gender == Gender.MALE:
        return 1 if is_yang_year else -1
    else:
        return -1 if is_yang_year else 1


def _calculate_start_age(
    birth_dt: datetime,
    year_gan: str,
    gender: Gender
) -> tuple[int, int]:
    """
    计算起运年龄
    从出生日到下一个（顺行）或上一个（逆行）节气的天数
    三天折一年
    
    返回: (起运年龄, 起运月份)
    """
    direction = _get_dayun_direction(year_gan, gender)
    
    # 简化计算：使用近似节气日期
    # 实际应使用精确节气计算
    month = birth_dt.month
    day = birth_dt.day
    
    # 每月节气近似日期（节）
    jieqi_days = {
        1: 6, 2: 4, 3: 6, 4: 5, 5: 6, 6: 6,
        7: 7, 8: 8, 9: 8, 10: 9, 11: 8, 12: 7
    }
    
    if direction > 0:
        # 顺行：到下一个节气
        if day < jieqi_days[month]:
            days = jieqi_days[month] - day
        else:
            next_month = month + 1 if month < 12 else 1
            days = (30 - day) + jieqi_days[next_month]
    else:
        # 逆行：到上一个节气
        if day >= jieqi_days[month]:
            days = day - jieqi_days[month]
        else:
            prev_month = month - 1 if month > 1 else 12
            days = day + (30 - jieqi_days[prev_month])
    
    # 三天折一年，一天折四个月
    start_age = days // 3
    extra_months = (days % 3) * 4
    
    return start_age, extra_months


def _get_dayun_pillar(
    month_gan: str, month_zhi: str,
    step: int, direction: int
) -> tuple[str, str]:
    """
    获取大运干支
    从月柱开始，按方向推算
    """
    gan_idx = TIANGAN.index(month_gan)
    zhi_idx = DIZHI.index(month_zhi)
    
    new_gan_idx = (gan_idx + step * direction) % 10
    new_zhi_idx = (zhi_idx + step * direction) % 12
    
    return TIANGAN[new_gan_idx], DIZHI[new_zhi_idx]


def calculate_dayun(bazi: BaziChart, num_dayun: int = 8) -> DaYunInfo:
    """
    计算大运
    
    Args:
        bazi: 八字信息
        num_dayun: 大运数量（默认8个，共80年）
    
    Returns:
        DaYunInfo: 大运信息
    """
    year_gan = bazi.year_pillar.tiangan.value
    month_gan = bazi.month_pillar.tiangan.value
    month_zhi = bazi.month_pillar.dizhi.value
    
    # 计算大运方向和起运年龄
    direction = _get_dayun_direction(year_gan, bazi.gender)
    start_age, extra_months = _calculate_start_age(
        bazi.birth_datetime, year_gan, bazi.gender
    )
    
    # 生成大运列表
    dayun_list = []
    birth_year = bazi.birth_datetime.year
    
    for i in range(1, num_dayun + 1):
        gan, zhi = _get_dayun_pillar(month_gan, month_zhi, i, direction)
        ganzhi = f"{gan}{zhi}"
        
        # 计算大运起止年龄和年份
        age_start = start_age + (i - 1) * 10
        age_end = age_start + 9
        year_start = birth_year + age_start
        year_end = birth_year + age_end
        
        # 大运五行
        wuxing = TIANGAN_WUXING[gan]
        
        dayun = DaYun(
            ganzhi=ganzhi,
            tiangan=gan,
            dizhi=zhi,
            wuxing=wuxing,
            start_age=age_start,
            end_age=age_end,
            start_year=year_start,
            end_year=year_end
        )
        dayun_list.append(dayun)
    
    # 大运方向描述
    direction_desc = "顺行" if direction > 0 else "逆行"
    
    return DaYunInfo(
        direction=direction_desc,
        start_age=start_age,
        extra_months=extra_months,
        dayun_list=dayun_list
    )


def get_current_dayun(dayun_info: DaYunInfo, age: int) -> DaYun | None:
    """获取当前所在大运"""
    for dayun in dayun_info.dayun_list:
        if dayun.start_age <= age <= dayun.end_age:
            return dayun
    return None
