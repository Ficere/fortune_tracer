"""流年运势详细分析模块"""
from datetime import datetime
from src.models import BaziChart, WuxingAnalysis
from src.models.bazi_models import LiuNianFortune, LiuNianAnalysis, DaYunInfo
from .constants import TIANGAN, DIZHI, TIANGAN_WUXING, DIZHI_LIUHE, DIZHI_LIUCHONG
from .nayin import get_nayin, get_nayin_wuxing
from .liunian_data import WUXING_MATTERS, get_level


def _get_year_ganzhi(year: int) -> tuple[str, str]:
    """获取年份干支"""
    return TIANGAN[(year - 4) % 10], DIZHI[(year - 4) % 12]


def _analyze_relations(year_zhi: str, bazi: BaziChart) -> list[tuple[str, str, str]]:
    """分析流年地支与八字的合冲关系"""
    relations = []
    pillars = [
        ("年", bazi.year_pillar), ("月", bazi.month_pillar),
        ("日", bazi.day_pillar), ("时", bazi.hour_pillar),
    ]
    
    for name, pillar in pillars:
        bazi_zhi = pillar.dizhi.value
        # 检查六合
        for (a, b) in DIZHI_LIUHE:
            if {year_zhi, bazi_zhi} == {a, b}:
                relations.append((f"{name}支", "合", f"流年与{name}支相合"))
        # 检查六冲
        for (a, b) in DIZHI_LIUCHONG:
            if {year_zhi, bazi_zhi} == {a, b}:
                relations.append((f"{name}支", "冲", f"流年与{name}支相冲"))
    
    return relations


def _calc_score(year_gan: str, wuxing: WuxingAnalysis, relations: list) -> int:
    """计算流年运势分数"""
    score = 60
    year_wx = TIANGAN_WUXING[year_gan]
    favorable = [w.value for w in wuxing.favorable]
    unfavorable = [w.value for w in wuxing.unfavorable]
    
    if year_wx in favorable:
        score += 20
    elif year_wx in unfavorable:
        score -= 15
    
    for _, rel_type, _ in relations:
        score += 10 if rel_type == "合" else -12 if rel_type == "冲" else 0
    
    score += (hash(year_gan) % 10) - 5
    return max(25, min(95, score))


def _get_advice(year_wx: str, score: int, relations: list) -> list[str]:
    """生成流年建议"""
    advice = []
    if score >= 80:
        advice.append("今年运势较好，可积极进取")
    elif score >= 60:
        advice.append("今年运势平稳，稳中求进")
    else:
        advice.append("今年运势一般，宜守不宜攻")
    
    matters = WUXING_MATTERS.get(year_wx, {})
    if score >= 70 and matters.get("favorable"):
        advice.append(f"有利事项：{matters['favorable'][0]}")
    if score < 60 and matters.get("unfavorable"):
        advice.append(f"注意事项：{matters['unfavorable'][0]}")
    
    if any("冲" in r[1] and "日" in r[0] for r in relations):
        advice.append("流年冲日支，注意健康和感情")
    
    return advice


def calculate_liunian(
    bazi: BaziChart, wuxing: WuxingAnalysis,
    dayun_info: DaYunInfo | None = None, years: int = 10
) -> LiuNianAnalysis:
    """计算流年运势"""
    current_year = datetime.now().year
    liunian_list = []
    
    for i in range(years):
        year = current_year + i
        year_gan, year_zhi = _get_year_ganzhi(year)
        ganzhi = f"{year_gan}{year_zhi}"
        year_wx = TIANGAN_WUXING[year_gan]
        nayin = get_nayin(ganzhi)
        
        relations = _analyze_relations(year_zhi, bazi)
        score = _calc_score(year_gan, wuxing, relations)
        level = get_level(score)
        advice = _get_advice(year_wx, score, relations)
        
        key_events = []
        if score >= 80:
            key_events.append("事业有成")
        if any("合" in r[1] for r in relations):
            key_events.append("贵人相助")
        if any("冲" in r[1] for r in relations):
            key_events.append("变动较大")
        
        liunian_list.append(LiuNianFortune(
            year=year, ganzhi=ganzhi, wuxing=year_wx, nayin=nayin,
            score=score, level=level,
            key_events=key_events or ["运势平稳"],
            advice=advice,
            relations=[f"{p}: {t}" for p, t, _ in relations] or ["无明显合冲"]
        ))
    
    avg_score = sum(f.score for f in liunian_list) / len(liunian_list)
    best = sorted(liunian_list, key=lambda x: x.score, reverse=True)[:3]
    worst = sorted(liunian_list, key=lambda x: x.score)[:2]
    
    summary = (
        f"未来{years}年平均运势{avg_score:.0f}分。"
        f"较好年份：{', '.join(str(y.year) for y in best)}。"
        f"需注意：{', '.join(str(y.year) for y in worst)}。"
    )
    
    return LiuNianAnalysis(
        liunian_list=liunian_list,
        summary=summary,
        best_years=[y.year for y in best],
        caution_years=[y.year for y in worst]
    )
