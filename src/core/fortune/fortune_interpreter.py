"""运势详细解读生成器"""
from src.models import BaziChart, WuxingAnalysis
from src.core.bazi.constants import TIANGAN, DIZHI, TIANGAN_WUXING, DIZHI_WUXING
from src.core.bazi.constants import DIZHI_LIUHE, DIZHI_LIUCHONG, DIZHI_XING
from src.core.fortune.fortune_data import (
    WUXING_RELATION, get_fortune_level, get_age_stage,
    CAREER_ADVICE, LOVE_ADVICE, HEALTH_ADVICE, WEALTH_ADVICE, get_activities_by_age
)


def _get_ganzhi_relations(
    year_zhi: str, bazi: BaziChart
) -> list[tuple[str, str]]:
    """分析流年地支与八字的关系"""
    relations = []
    pillars = [
        ("年支", bazi.year_pillar.dizhi.value),
        ("月支", bazi.month_pillar.dizhi.value),
        ("日支", bazi.day_pillar.dizhi.value),
        ("时支", bazi.hour_pillar.dizhi.value),
    ]
    for name, zhi in pillars:
        pair = tuple(sorted([year_zhi, zhi]))
        if pair in DIZHI_LIUHE or (pair[1], pair[0]) in DIZHI_LIUHE:
            relations.append((name, f"六合{name}"))
        if pair in DIZHI_LIUCHONG or (pair[1], pair[0]) in DIZHI_LIUCHONG:
            relations.append((name, f"冲{name}"))
        if pair in DIZHI_XING or (pair[1], pair[0]) in DIZHI_XING:
            relations.append((name, f"刑{name}"))
    return relations


def generate_year_detail(
    year: int, age: int, score: float,
    bazi: BaziChart, wuxing: WuxingAnalysis
) -> dict:
    """生成单年详细解读"""
    gan_idx = (year - 4) % 10
    zhi_idx = (year - 4) % 12
    year_gan, year_zhi = TIANGAN[gan_idx], DIZHI[zhi_idx]
    year_wx = TIANGAN_WUXING[year_gan]
    
    # 获取等级信息
    level, emoji, level_desc = get_fortune_level(score)
    stage, stage_desc = get_age_stage(age)
    
    # 五行关系分析
    dm_wx = wuxing.day_master.value
    relation, relation_desc = WUXING_RELATION.get(
        (dm_wx, year_wx), ("中性", "无明显生克")
    )
    
    # 喜忌分析
    favorable_wx = [w.value for w in wuxing.favorable]
    is_favorable = year_wx in favorable_wx
    wuxing_effect = "喜神当值，助力运势" if is_favorable else "忌神流年，需多努力"

    # 干支关系
    ganzhi_relations = _get_ganzhi_relations(year_zhi, bazi)
    relation_strs = [r[1] for r in ganzhi_relations] if ganzhi_relations else ["无特殊关系"]

    # 评分因素说明（用于AI解读）
    score_factors = []
    if is_favorable:
        score_factors.append(f"流年五行{year_wx}为喜神(+18)")
    else:
        score_factors.append(f"流年五行{year_wx}非喜神")
    if ganzhi_relations:
        for r in ganzhi_relations:
            score_factors.append(f"{r[1]}")

    # 综合建议
    return {
        "year": year,
        "age": age,
        "ganzhi": f"{year_gan}{year_zhi}",
        "wuxing": year_wx,
        "score": score,
        "level": level,
        "emoji": emoji,
        "level_desc": level_desc,
        "stage": stage,
        "stage_desc": stage_desc,
        "wuxing_relation": relation,
        "wuxing_desc": relation_desc,
        "wuxing_effect": wuxing_effect,
        "ganzhi_relations": relation_strs,
        "career": CAREER_ADVICE.get(level, ["保持平常心"])[0],
        "love": LOVE_ADVICE.get(level, ["顺其自然"])[0],
        "health": HEALTH_ADVICE[year_wx]["favorable" if is_favorable else "unfavorable"],
        "wealth": WEALTH_ADVICE.get(level, ["量力而行"])[0],
        "suitable": get_activities_by_age(age, level).get("suitable", [])[:3],
        "unsuitable": get_activities_by_age(age, level).get("unsuitable", [])[:3],
        "score_factors": score_factors,
        "is_favorable_year": is_favorable,
    }


def generate_dayun_detail(
    dayun_ganzhi: str, dayun_wx: str,
    start_age: int, end_age: int,
    bazi: BaziChart, wuxing: WuxingAnalysis
) -> dict:
    """生成大运详细解读"""
    gan, zhi = dayun_ganzhi[0], dayun_ganzhi[1]
    gan_wx = TIANGAN_WUXING[gan]
    zhi_wx = DIZHI_WUXING[zhi]
    
    dm_wx = wuxing.day_master.value
    gan_relation, gan_desc = WUXING_RELATION.get(
        (dm_wx, gan_wx), ("中性", "无明显影响")
    )
    zhi_relation, zhi_desc = WUXING_RELATION.get(
        (dm_wx, zhi_wx), ("中性", "无明显影响")
    )
    
    # 喜忌判断
    favorable_wx = [w.value for w in wuxing.favorable]
    gan_favorable = gan_wx in favorable_wx
    zhi_favorable = zhi_wx in favorable_wx
    
    # 综合评分
    score = 60
    if gan_favorable:
        score += 15
    if zhi_favorable:
        score += 15
    if gan_relation == "被生":
        score += 5
    if gan_relation == "被克":
        score -= 10
        
    score = min(max(score, 30), 95)
    level, emoji, level_desc = get_fortune_level(score)

    # 年龄段描述
    stage_start, _ = get_age_stage(start_age)
    stage_end, _ = get_age_stage(end_age)

    # 喜忌效果描述
    gan_effect = "喜神助力" if gan_favorable else "忌神克制"
    zhi_effect = "喜神助力" if zhi_favorable else "忌神克制"
    gan_summary = "喜神助力" if gan_favorable else "需多努力"
    zhi_summary = "运势平顺" if zhi_favorable else "宜谨慎行事"

    return {
        "ganzhi": dayun_ganzhi,
        "tiangan": gan,
        "dizhi": zhi,
        "tiangan_wuxing": gan_wx,
        "dizhi_wuxing": zhi_wx,
        "start_age": start_age,
        "end_age": end_age,
        "score": score,
        "level": level,
        "emoji": emoji,
        "level_desc": level_desc,
        "stage": f"{stage_start} → {stage_end}" if stage_start != stage_end else stage_start,
        "gan_relation": f"天干{gan}({gan_wx})与日主{dm_wx}: {gan_desc}",
        "zhi_relation": f"地支{zhi}({zhi_wx})与日主{dm_wx}: {zhi_desc}",
        "gan_effect": gan_effect,
        "zhi_effect": zhi_effect,
        "career": CAREER_ADVICE.get(level, ["保持平常心"]),
        "love": LOVE_ADVICE.get(level, ["顺其自然"]),
        "health": HEALTH_ADVICE[gan_wx]["favorable" if gan_favorable else "unfavorable"],
        "wealth": WEALTH_ADVICE.get(level, ["量力而行"]),
        "summary": f"此大运{level}，{level_desc}。天干{gan_summary}，地支{zhi_summary}。",
    }

