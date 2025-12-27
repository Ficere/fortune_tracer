"""辅助宫位计算模块 - 命宫、胎元、身宫"""
from typing import NamedTuple
from .constants import TIANGAN, DIZHI
from .gong_descriptions import (
    MING_GONG_DESC, TAI_YUAN_DESC, SHEN_GONG_DESC, WU_HU_DUN
)


class GongInfo(NamedTuple):
    """宫位信息"""
    name: str        # 宫位名称
    tiangan: str     # 天干
    dizhi: str       # 地支
    ganzhi: str      # 干支组合
    description: str # 描述


class AuxiliaryInfo(NamedTuple):
    """辅助信息汇总"""
    ming_gong: GongInfo   # 命宫
    tai_yuan: GongInfo    # 胎元
    shen_gong: GongInfo   # 身宫


def _get_tiangan_by_wuhudun(year_gan: str, dizhi: str) -> str:
    """根据年干和地支，使用五虎遁推算天干"""
    start_gan = WU_HU_DUN[year_gan]
    start_idx = TIANGAN.index(start_gan)
    zhi_idx = DIZHI.index(dizhi)
    yin_idx = 2  # 寅的索引
    offset = (zhi_idx - yin_idx + 12) % 12
    return TIANGAN[(start_idx + offset) % 10]


def calculate_ming_gong(year_gan: str, month_zhi: str, hour_zhi: str) -> GongInfo:
    """
    计算命宫（先天禀赋和性格特质）
    公式：命宫地支 = (26 - 月支序号 - 时支序号) % 12
    """
    month_idx = DIZHI.index(month_zhi)
    hour_idx = DIZHI.index(hour_zhi)
    ming_idx = (26 - month_idx - hour_idx) % 12
    
    dizhi = DIZHI[ming_idx]
    tiangan = _get_tiangan_by_wuhudun(year_gan, dizhi)
    
    return GongInfo(
        name="命宫",
        tiangan=tiangan,
        dizhi=dizhi,
        ganzhi=f"{tiangan}{dizhi}",
        description=MING_GONG_DESC.get(dizhi, "")
    )


def calculate_tai_yuan(month_gan: str, month_zhi: str) -> GongInfo:
    """
    计算胎元（受胎时的能量场）
    公式：天干进一位，地支进三位
    """
    gan_idx = TIANGAN.index(month_gan)
    zhi_idx = DIZHI.index(month_zhi)
    
    tai_gan = TIANGAN[(gan_idx + 1) % 10]
    tai_zhi = DIZHI[(zhi_idx + 3) % 12]
    
    return GongInfo(
        name="胎元",
        tiangan=tai_gan,
        dizhi=tai_zhi,
        ganzhi=f"{tai_gan}{tai_zhi}",
        description=TAI_YUAN_DESC.get(tai_zhi, "")
    )


def calculate_shen_gong(year_gan: str, month_zhi: str, hour_zhi: str) -> GongInfo:
    """
    计算身宫（后天发展和行为模式）
    公式：身宫地支 = (月支序号 + 时支序号 + 2) % 12
    """
    month_idx = DIZHI.index(month_zhi)
    hour_idx = DIZHI.index(hour_zhi)
    shen_idx = (month_idx + hour_idx + 2) % 12
    
    dizhi = DIZHI[shen_idx]
    tiangan = _get_tiangan_by_wuhudun(year_gan, dizhi)
    
    return GongInfo(
        name="身宫",
        tiangan=tiangan,
        dizhi=dizhi,
        ganzhi=f"{tiangan}{dizhi}",
        description=SHEN_GONG_DESC.get(dizhi, "")
    )


def calculate_auxiliary(
    year_gan: str, month_gan: str, month_zhi: str, hour_zhi: str
) -> AuxiliaryInfo:
    """计算所有辅助宫位"""
    return AuxiliaryInfo(
        ming_gong=calculate_ming_gong(year_gan, month_zhi, hour_zhi),
        tai_yuan=calculate_tai_yuan(month_gan, month_zhi),
        shen_gong=calculate_shen_gong(year_gan, month_zhi, hour_zhi)
    )


def calculate_auxiliary_from_bazi(bazi) -> AuxiliaryInfo:
    """从八字对象计算辅助宫位"""
    return calculate_auxiliary(
        year_gan=bazi.year_pillar.tiangan,
        month_gan=bazi.month_pillar.tiangan,
        month_zhi=bazi.month_pillar.dizhi,
        hour_zhi=bazi.hour_pillar.dizhi
    )
