"""八字配对计算模块"""
from src.models import BaziChart, WuxingAnalysis
from src.models.compatibility_models import (
    CompatibilityResult, WuxingCompatibility, GanZhiRelations,
    CompatibilityAdvice, RelationshipType
)
from src.core.bazi.constants import (
    TIANGAN_HE, TIANGAN_CHONG, DIZHI_LIUHE, DIZHI_LIUCHONG,
    DIZHI_SANHE, DIZHI_XING, WUXING_SHENG, WUXING_KE
)


def _check_pair(pairs_dict: dict, a: str, b: str) -> tuple | None:
    """检查两个元素是否在配对字典中"""
    if (a, b) in pairs_dict:
        return (a, b), pairs_dict[(a, b)]
    if (b, a) in pairs_dict:
        return (b, a), pairs_dict[(b, a)]
    return None


def _analyze_wuxing_compat(wx1: WuxingAnalysis, wx2: WuxingAnalysis) -> WuxingCompatibility:
    """分析五行互补性"""
    c1, c2 = wx1.counts.to_dict(), wx2.counts.to_dict()
    complementary, conflicting = [], []
    
    # 检查互补：一方弱的五行另一方强
    for wx in ["木", "火", "土", "金", "水"]:
        diff = abs(c1[wx] - c2[wx])
        if c1[wx] < 1.5 and c2[wx] >= 2:
            complementary.append(f"{wx}(对方补足)")
        elif c2[wx] < 1.5 and c1[wx] >= 2:
            complementary.append(f"{wx}(己方补足)")
    
    # 检查冲突：双方喜忌相冲
    for fav in wx1.favorable:
        if fav in wx2.unfavorable:
            conflicting.append(f"{fav.value}(喜忌相冲)")
    
    # 计算平衡分
    balance = 70
    balance += len(complementary) * 8
    balance -= len(conflicting) * 10
    balance = max(0, min(100, balance))
    
    analysis = f"五行互补{len(complementary)}项，冲突{len(conflicting)}项"
    return WuxingCompatibility(
        complementary=complementary, conflicting=conflicting,
        balance_score=balance, analysis=analysis
    )


def _analyze_ganzhi_relations(bazi1: BaziChart, bazi2: BaziChart) -> GanZhiRelations:
    """分析天干地支关系"""
    pillars1 = [bazi1.year_pillar, bazi1.month_pillar, bazi1.day_pillar, bazi1.hour_pillar]
    pillars2 = [bazi2.year_pillar, bazi2.month_pillar, bazi2.day_pillar, bazi2.hour_pillar]
    
    tiangan_he, tiangan_chong = [], []
    dizhi_he, dizhi_chong, dizhi_xing = [], [], []
    
    for p1 in pillars1:
        for p2 in pillars2:
            g1, g2 = p1.tiangan.value, p2.tiangan.value
            z1, z2 = p1.dizhi.value, p2.dizhi.value
            
            # 天干合
            if result := _check_pair(TIANGAN_HE, g1, g2):
                tiangan_he.append(RelationshipType(
                    relation="天干合", elements=[g1, g2],
                    score_impact=8, description=result[1]
                ))
            # 天干冲
            if result := _check_pair(TIANGAN_CHONG, g1, g2):
                tiangan_chong.append(RelationshipType(
                    relation="天干冲", elements=[g1, g2],
                    score_impact=-5, description=result[1]
                ))
            # 地支合
            if result := _check_pair(DIZHI_LIUHE, z1, z2):
                dizhi_he.append(RelationshipType(
                    relation="六合", elements=[z1, z2],
                    score_impact=10, description=f"合化{result[1]}"
                ))
            # 地支冲
            if result := _check_pair(DIZHI_LIUCHONG, z1, z2):
                dizhi_chong.append(RelationshipType(
                    relation="六冲", elements=[z1, z2],
                    score_impact=-8, description=result[1]
                ))
            # 地支刑
            if result := _check_pair(DIZHI_XING, z1, z2):
                dizhi_xing.append(RelationshipType(
                    relation="相刑", elements=[z1, z2],
                    score_impact=-6, description=result[1]
                ))
    
    return GanZhiRelations(
        tiangan_he=tiangan_he, tiangan_chong=tiangan_chong,
        dizhi_he=dizhi_he, dizhi_chong=dizhi_chong, dizhi_xing=dizhi_xing
    )


def _generate_advice(
    wuxing_compat: WuxingCompatibility, ganzhi: GanZhiRelations, score: int
) -> CompatibilityAdvice:
    """生成配对建议"""
    strengths, challenges, suggestions, cautions = [], [], [], []
    
    if ganzhi.tiangan_he:
        strengths.append("天干相合，心意相通，沟通顺畅")
    if ganzhi.dizhi_he:
        strengths.append("地支六合，情感和谐，相互吸引")
    if wuxing_compat.complementary:
        strengths.append("五行互补，取长补短，相得益彰")
    
    if ganzhi.dizhi_chong:
        challenges.append("地支相冲，需注意性格差异带来的摩擦")
    if ganzhi.dizhi_xing:
        challenges.append("地支相刑，可能存在相互伤害的情况")
    if wuxing_compat.conflicting:
        challenges.append("喜忌相冲，生活习惯可能存在分歧")
    
    if score >= 80:
        suggestions.append("缘分天定，珍惜彼此，共创美好")
    elif score >= 60:
        suggestions.append("多些包容理解，感情可长久")
    else:
        suggestions.append("需要更多努力经营感情")
    
    if ganzhi.dizhi_chong:
        cautions.append("避免在冲突时做重要决定")
    if not strengths:
        cautions.append("建议通过共同兴趣增进感情")
    
    return CompatibilityAdvice(
        strengths=strengths or ["相处自然，无明显冲突"],
        challenges=challenges or ["暂无明显挑战"],
        suggestions=suggestions,
        cautions=cautions or ["保持沟通，相互尊重"]
    )


def _calculate_score(wuxing_compat: WuxingCompatibility, ganzhi: GanZhiRelations) -> int:
    """计算配对总分"""
    score = 60  # 基础分
    score += wuxing_compat.balance_score // 5

    for rel in ganzhi.tiangan_he:
        score += rel.score_impact
    for rel in ganzhi.tiangan_chong:
        score += rel.score_impact
    for rel in ganzhi.dizhi_he:
        score += rel.score_impact
    for rel in ganzhi.dizhi_chong:
        score += rel.score_impact
    for rel in ganzhi.dizhi_xing:
        score += rel.score_impact

    return max(20, min(98, score))


def _get_grade(score: int) -> str:
    """获取评级"""
    if score >= 90:
        return "天作之合 💕"
    elif score >= 80:
        return "良缘佳配 ❤️"
    elif score >= 70:
        return "和谐美满 💛"
    elif score >= 60:
        return "相互包容 💚"
    elif score >= 50:
        return "需要磨合 💙"
    else:
        return "挑战较多 🤍"


def calculate_compatibility(
    bazi1: BaziChart, bazi2: BaziChart,
    wuxing1: WuxingAnalysis, wuxing2: WuxingAnalysis
) -> CompatibilityResult:
    """计算八字配对结果"""
    wuxing_compat = _analyze_wuxing_compat(wuxing1, wuxing2)
    ganzhi_relations = _analyze_ganzhi_relations(bazi1, bazi2)
    score = _calculate_score(wuxing_compat, ganzhi_relations)
    grade = _get_grade(score)
    advice = _generate_advice(wuxing_compat, ganzhi_relations, score)

    return CompatibilityResult(
        person1_bazi=bazi1, person2_bazi=bazi2,
        person1_wuxing=wuxing1, person2_wuxing=wuxing2,
        wuxing_compat=wuxing_compat, ganzhi_relations=ganzhi_relations,
        total_score=score, grade=grade, advice=advice
    )

