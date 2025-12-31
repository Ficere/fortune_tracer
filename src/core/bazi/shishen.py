"""十神分析模块 - 日主与其他天干的五行生克阴阳关系"""
from src.models import BaziChart
from src.models.bazi_models import ShiShenInfo, ShiShenAnalysis
from src.core.bazi.constants import TIANGAN, TIANGAN_WUXING, WUXING_SHENG, WUXING_KE, DIZHI_CANGAN


# 十神名称
SHISHEN_NAMES = {
    ("同", True): "比肩",   # 同五行、同阴阳
    ("同", False): "劫财",  # 同五行、异阴阳
    ("生我", True): "偏印", # 生我者、同阴阳
    ("生我", False): "正印", # 生我者、异阴阳
    ("我生", True): "食神", # 我生者、同阴阳
    ("我生", False): "伤官", # 我生者、异阴阳
    ("克我", True): "七杀", # 克我者、同阴阳（也叫偏官）
    ("克我", False): "正官", # 克我者、异阴阳
    ("我克", True): "偏财", # 我克者、同阴阳
    ("我克", False): "正财", # 我克者、异阴阳
}

# 十神特性描述
SHISHEN_TRAITS = {
    "比肩": "自信独立，坚持己见，重视自我",
    "劫财": "竞争心强，敢于冒险，重情义",
    "偏印": "思维敏捷，兴趣广泛，善于钻研",
    "正印": "温和善良，重视学习，有责任感",
    "食神": "才华横溢，乐观开朗，享受生活",
    "伤官": "聪明伶俐，追求自由，富有创意",
    "七杀": "魄力十足，果断刚毅，有领导力",
    "正官": "正直守规，重视名誉，追求稳定",
    "偏财": "机遇多变，善于经营，人缘好",
    "正财": "勤劳务实，理财有方，重视家庭",
}


def _is_yang_gan(gan: str) -> bool:
    """判断天干是否为阳"""
    return TIANGAN.index(gan) % 2 == 0


def _get_wuxing_relation(day_wuxing: str, other_wuxing: str) -> str:
    """获取五行关系"""
    if day_wuxing == other_wuxing:
        return "同"
    elif WUXING_SHENG.get(other_wuxing) == day_wuxing:
        return "生我"
    elif WUXING_SHENG.get(day_wuxing) == other_wuxing:
        return "我生"
    elif WUXING_KE.get(other_wuxing) == day_wuxing:
        return "克我"
    elif WUXING_KE.get(day_wuxing) == other_wuxing:
        return "我克"
    return "同"


def _get_shishen(day_gan: str, other_gan: str) -> str:
    """
    获取十神
    
    Args:
        day_gan: 日主天干
        other_gan: 其他天干
    
    Returns:
        十神名称
    """
    day_wuxing = TIANGAN_WUXING[day_gan]
    other_wuxing = TIANGAN_WUXING[other_gan]
    
    relation = _get_wuxing_relation(day_wuxing, other_wuxing)
    same_yinyang = _is_yang_gan(day_gan) == _is_yang_gan(other_gan)
    
    return SHISHEN_NAMES.get((relation, same_yinyang), "比肩")


def analyze_shishen(bazi: BaziChart) -> ShiShenAnalysis:
    """
    分析八字中的十神
    
    返回每柱的十神和整体分析
    """
    day_gan = bazi.day_pillar.tiangan.value
    
    # 分析四柱天干的十神
    pillars = [
        ("年柱", bazi.year_pillar),
        ("月柱", bazi.month_pillar),
        ("日柱", bazi.day_pillar),
        ("时柱", bazi.hour_pillar),
    ]
    
    shishen_list = []
    shishen_count = {}
    
    for pillar_name, pillar in pillars:
        gan = pillar.tiangan.value
        zhi = pillar.dizhi.value
        
        # 天干十神（日主本身记为"日主"）
        if pillar_name == "日柱":
            gan_shishen = "日主"
        else:
            gan_shishen = _get_shishen(day_gan, gan)
            shishen_count[gan_shishen] = shishen_count.get(gan_shishen, 0) + 1
        
        # 地支藏干十神
        cangans = DIZHI_CANGAN.get(zhi, [])
        zhi_shishen_list = []
        for cg in cangans:
            cg_shishen = _get_shishen(day_gan, cg)
            zhi_shishen_list.append(cg_shishen)
            shishen_count[cg_shishen] = shishen_count.get(cg_shishen, 0) + 0.5
        
        info = ShiShenInfo(
            pillar_name=pillar_name,
            tiangan=gan,
            dizhi=zhi,
            tiangan_shishen=gan_shishen,
            dizhi_shishen=zhi_shishen_list,
            dizhi_cangan=cangans
        )
        shishen_list.append(info)
    
    # 确定格局（简化版）
    pattern = _determine_pattern(shishen_count)
    
    # 生成分析
    analysis = _generate_analysis(shishen_count, pattern)
    
    return ShiShenAnalysis(
        shishen_list=shishen_list,
        shishen_count=shishen_count,
        pattern=pattern,
        analysis=analysis
    )


def _determine_pattern(shishen_count: dict) -> str:
    """
    确定命局格局（简化版）
    
    实际格局判断更为复杂，需考虑透干、月令等
    """
    # 找出最多的十神
    if not shishen_count:
        return "普通格局"
    
    max_shishen = max(shishen_count, key=lambda x: shishen_count[x])
    
    pattern_map = {
        "正官": "正官格",
        "七杀": "七杀格",
        "正印": "正印格",
        "偏印": "偏印格",
        "正财": "正财格",
        "偏财": "偏财格",
        "食神": "食神格",
        "伤官": "伤官格",
        "比肩": "比肩格",
        "劫财": "劫财格",
    }
    
    return pattern_map.get(max_shishen, "普通格局")


def _generate_analysis(shishen_count: dict, pattern: str) -> str:
    """生成十神分析文字"""
    if not shishen_count:
        return "八字十神分布均匀，命局平和。"
    
    # 找出前三名
    sorted_shishen = sorted(
        shishen_count.items(),
        key=lambda x: x[1],
        reverse=True
    )[:3]
    
    analysis_parts = [f"命局为{pattern}。"]
    
    for shishen, count in sorted_shishen:
        if count >= 2:
            trait = SHISHEN_TRAITS.get(shishen, "")
            analysis_parts.append(f"{shishen}旺，{trait}。")
    
    # 检查缺失
    all_shishen = set(SHISHEN_TRAITS.keys())
    present = set(shishen_count.keys())
    missing = all_shishen - present
    
    if "正官" in missing and "七杀" in missing:
        analysis_parts.append("官杀不显，自由度高但需注意自律。")
    if "正财" in missing and "偏财" in missing:
        analysis_parts.append("财星不显，需努力开拓财源。")
    
    return "".join(analysis_parts)
