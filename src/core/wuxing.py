"""五行分析模块"""
from src.models import BaziChart, WuxingAnalysis
from src.models.bazi_models import WuxingCount, Wuxing
from .constants import TIANGAN_WUXING, DIZHI_WUXING, DIZHI_CANGAN, WUXING_SHENG, WUXING_KE


def _count_wuxing(bazi: BaziChart) -> WuxingCount:
    """统计八字中五行数量（含藏干）"""
    counts = {"木": 0, "火": 0, "土": 0, "金": 0, "水": 0}
    
    pillars = [bazi.year_pillar, bazi.month_pillar, bazi.day_pillar, bazi.hour_pillar]
    
    for pillar in pillars:
        # 天干五行
        gan_wx = TIANGAN_WUXING[pillar.tiangan.value]
        counts[gan_wx] += 1
        
        # 地支五行（主气）
        zhi_wx = DIZHI_WUXING[pillar.dizhi.value]
        counts[zhi_wx] += 0.7
        
        # 藏干五行（余气）
        cangans = DIZHI_CANGAN.get(pillar.dizhi.value, [])
        for i, cg in enumerate(cangans):
            weight = 0.3 if i == 0 else 0.15
            cg_wx = TIANGAN_WUXING[cg]
            counts[cg_wx] += weight
    
    return WuxingCount(
        mu=round(counts["木"], 1),
        huo=round(counts["火"], 1),
        tu=round(counts["土"], 1),
        jin=round(counts["金"], 1),
        shui=round(counts["水"], 1)
    )


def _get_day_master(bazi: BaziChart) -> Wuxing:
    """获取日主五行"""
    day_gan = bazi.day_pillar.tiangan.value
    return Wuxing(TIANGAN_WUXING[day_gan])


def _analyze_strength(counts: WuxingCount, day_master: Wuxing) -> str:
    """分析日主强弱"""
    dm_wx = day_master.value
    count_dict = counts.to_dict()
    
    # 日主自身力量
    self_power = count_dict[dm_wx]
    
    # 生我者（印星）力量
    for wx, target in WUXING_SHENG.items():
        if target == dm_wx:
            self_power += count_dict[wx] * 0.5
            break
    
    # 计算总力量
    total = sum(count_dict.values())
    ratio = self_power / total if total > 0 else 0
    
    if ratio > 0.45:
        return "身旺"
    elif ratio > 0.35:
        return "中和"
    else:
        return "身弱"


def _get_favorable_unfavorable(
    day_master: Wuxing, strength: str
) -> tuple[list[Wuxing], list[Wuxing]]:
    """确定喜用神和忌神"""
    dm = day_master.value
    
    # 生我者
    for wx, target in WUXING_SHENG.items():
        if target == dm:
            sheng_wo = wx
            break
    
    # 我生者
    wo_sheng = WUXING_SHENG[dm]
    # 克我者
    for wx, target in WUXING_KE.items():
        if target == dm:
            ke_wo = wx
            break
    # 我克者
    wo_ke = WUXING_KE[dm]
    
    if strength == "身旺":
        favorable = [Wuxing(wo_sheng), Wuxing(wo_ke), Wuxing(ke_wo)]
        unfavorable = [Wuxing(dm), Wuxing(sheng_wo)]
    else:
        favorable = [Wuxing(dm), Wuxing(sheng_wo)]
        unfavorable = [Wuxing(wo_sheng), Wuxing(wo_ke), Wuxing(ke_wo)]
    
    return favorable, unfavorable


def analyze_wuxing(bazi: BaziChart) -> WuxingAnalysis:
    """完整五行分析"""
    counts = _count_wuxing(bazi)
    day_master = _get_day_master(bazi)
    strength = _analyze_strength(counts, day_master)
    favorable, unfavorable = _get_favorable_unfavorable(day_master, strength)
    
    return WuxingAnalysis(
        counts=counts,
        day_master=day_master,
        day_master_strength=strength,
        favorable=favorable,
        unfavorable=unfavorable
    )

