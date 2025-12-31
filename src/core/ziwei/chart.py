"""紫微斗数星盘生成器"""
from datetime import datetime
from typing import Optional
from src.core.utils import solar_to_lunar
from src.models.ziwei_models import (
    ZiweiChart, ZiweiAnalysis, PalaceInfo, Star, StarType, Palace, WuxingJu
)
from .constants import DIZHI, STAR_DESC
from .palace import (
    arrange_palaces, calculate_ming_gong_pos, calculate_shen_gong_pos,
    get_wuxing_ju
)
from .main_stars import arrange_main_stars
from .aux_stars import arrange_aux_sha_stars
from .sihua import apply_sihua_to_palaces, analyze_sihua_pattern


def get_hour_zhi(hour: int) -> str:
    """获取时辰地支"""
    hour_map = [
        (23, 1, "子"), (1, 3, "丑"), (3, 5, "寅"), (5, 7, "卯"),
        (7, 9, "辰"), (9, 11, "巳"), (11, 13, "午"), (13, 15, "未"),
        (15, 17, "申"), (17, 19, "酉"), (19, 21, "戌"), (21, 23, "亥"),
    ]
    for start, end, zhi in hour_map:
        if start <= hour < end or (start == 23 and hour >= 23):
            return zhi
    return "子"


def calculate_ziwei_chart(
    birth_datetime: datetime, gender: str, birth_place: Optional[str] = None
) -> ZiweiChart:
    """计算紫微斗数星盘
    
    Args:
        birth_datetime: 出生时间
        gender: 性别（"男"或"女"）
        birth_place: 出生地点（可选）
    
    Returns:
        ZiweiChart: 完整的紫微星盘
    """
    # 1. 转换为农历
    lunar = solar_to_lunar(birth_datetime)
    lunar_year = lunar.year
    lunar_month = lunar.month
    lunar_day = lunar.day
    
    # 2. 获取年干支和时辰
    year_gan, year_zhi = _get_year_ganzhi(lunar_year)
    hour_zhi = get_hour_zhi(birth_datetime.hour)
    
    # 3. 计算五行局
    wuxing_ju = get_wuxing_ju(year_gan, year_zhi)
    
    # 4. 计算命宫身宫位置
    ming_gong_pos = calculate_ming_gong_pos(lunar_month, hour_zhi)
    shen_gong_pos = calculate_shen_gong_pos(lunar_month, hour_zhi)
    
    # 5. 排十二宫
    palaces = arrange_palaces(lunar_month, hour_zhi, year_gan, year_zhi)
    
    # 6. 安主星
    palaces = arrange_main_stars(lunar_day, wuxing_ju, palaces)
    
    # 7. 安辅星煞星
    palaces = arrange_aux_sha_stars(
        lunar_month, hour_zhi, year_gan, year_zhi, palaces
    )
    
    # 8. 应用四化
    palaces, sihua_stars = apply_sihua_to_palaces(year_gan, palaces)
    
    # 9. 转换为模型
    palace_infos = _convert_palaces_to_models(palaces)
    
    return ZiweiChart(
        birth_datetime=birth_datetime,
        lunar_year=lunar_year,
        lunar_month=lunar_month,
        lunar_day=lunar_day,
        hour_zhi=hour_zhi,
        gender=gender,
        wuxing_ju=WuxingJu(wuxing_ju),
        ming_gong_pos=ming_gong_pos,
        shen_gong_pos=shen_gong_pos,
        palaces=palace_infos,
        sihua_stars=sihua_stars,
    )


def _get_year_ganzhi(lunar_year: int) -> tuple[str, str]:
    """获取年干支"""
    from src.core.bazi.constants import TIANGAN, DIZHI
    gan_idx = (lunar_year - 4) % 10
    zhi_idx = (lunar_year - 4) % 12
    return TIANGAN[gan_idx], DIZHI[zhi_idx]


def _convert_palaces_to_models(palaces: list[dict]) -> list[PalaceInfo]:
    """将字典格式转换为PalaceInfo模型"""
    palace_map = {p.value: p for p in Palace}
    result = []
    
    for p in palaces:
        main_stars = [
            Star(
                name=s["name"],
                star_type=StarType.MAIN,
                brightness=s.get("brightness", ""),
                sihua=s.get("sihua", ""),
                description=STAR_DESC.get(s["name"], ""),
            )
            for s in p["main_stars"]
        ]
        
        aux_stars = [
            Star(
                name=s["name"],
                star_type=StarType.AUX,
                sihua=s.get("sihua", ""),
            )
            for s in p["aux_stars"]
        ]
        
        sha_stars = [
            Star(name=s["name"], star_type=StarType.SHA)
            for s in p["sha_stars"]
        ]
        
        palace_enum = palace_map.get(p["name"], Palace.MING)
        
        result.append(PalaceInfo(
            palace=palace_enum,
            position=p["position"],
            dizhi=p["dizhi"],
            tiangan=p["tiangan"],
            main_stars=main_stars,
            aux_stars=aux_stars,
            sha_stars=sha_stars,
        ))
    
    return result

