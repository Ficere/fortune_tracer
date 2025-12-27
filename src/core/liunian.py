"""流年运势详细分析模块

流年是根据当年干支与八字的关系来分析该年的运势。
包括：流年与日主的关系、与大运的关系、吉凶事项等。
"""
from datetime import datetime
from src.models import BaziChart, WuxingAnalysis
from src.models.bazi_models import (
    LiuNianFortune, LiuNianAnalysis, DaYunInfo
)
from .constants import (
    TIANGAN, DIZHI, TIANGAN_WUXING, DIZHI_WUXING,
    WUXING_SHENG, WUXING_KE, DIZHI_LIUHE, DIZHI_LIUCHONG
)
from .nayin import get_nayin, get_nayin_wuxing


# 五行对应事项
WUXING_MATTERS = {
    "木": {
        "favorable": ["事业发展", "学业进步", "健康向好", "贵人相助"],
        "unfavorable": ["肝胆问题", "情绪波动", "计划受阻"],
    },
    "火": {
        "favorable": ["人际提升", "名声显达", "喜事临门", "考试顺利"],
        "unfavorable": ["心脑问题", "口舌是非", "破财风险"],
    },
    "土": {
        "favorable": ["财运稳定", "置业购房", "婚姻喜事", "贵人扶持"],
        "unfavorable": ["脾胃问题", "投资谨慎", "文书纠纷"],
    },
    "金": {
        "favorable": ["财运亨通", "事业晋升", "贵人助力", "健康改善"],
        "unfavorable": ["肺部问题", "刑伤风险", "是非困扰"],
    },
    "水": {
        "favorable": ["智慧增长", "财源广进", "桃花运旺", "出行顺利"],
        "unfavorable": ["肾脏问题", "小人暗算", "漂泊不定"],
    },
}

# 干支关系影响
GANZHI_EFFECTS = {
    "合": ("吉", "贵人相助，合作顺利"),
    "冲": ("凶", "变动较大，谨慎行事"),
    "刑": ("凶", "是非困扰，注意健康"),
    "生": ("吉", "得到助力，顺风顺水"),
    "克": ("凶", "阻碍较多，需要努力"),
}


def _get_year_ganzhi(year: int) -> tuple[str, str]:
    """获取年份干支"""
    gan_idx = (year - 4) % 10
    zhi_idx = (year - 4) % 12
    return TIANGAN[gan_idx], DIZHI[zhi_idx]


def _analyze_year_relations(
    year_gan: str, year_zhi: str,
    bazi: BaziChart
) -> list[tuple[str, str, str]]:
    """分析流年与八字的关系"""
    relations = []
    
    pillars = [
        ("年", bazi.year_pillar),
        ("月", bazi.month_pillar),
        ("日", bazi.day_pillar),
        ("时", bazi.hour_pillar),
    ]
    
    for pillar_name, pillar in pillars:
        bazi_zhi = pillar.dizhi.value
        
        # 检查六合
        for (a, b), _ in DIZHI_LIUHE.items():
            if (year_zhi == a and bazi_zhi == b) or (year_zhi == b and bazi_zhi == a):
                relations.append((f"{pillar_name}支", "合", f"流年{year_zhi}与{pillar_name}支{bazi_zhi}相合"))
        
        # 检查六冲
        for (a, b), _ in DIZHI_LIUCHONG.items():
            if (year_zhi == a and bazi_zhi == b) or (year_zhi == b and bazi_zhi == a):
                relations.append((f"{pillar_name}支", "冲", f"流年{year_zhi}与{pillar_name}支{bazi_zhi}相冲"))
    
    return relations


def _calculate_year_score(
    year_gan: str, year_zhi: str,
    wuxing: WuxingAnalysis,
    relations: list[tuple[str, str, str]]
) -> int:
    """计算流年运势分数"""
    score = 60  # 基础分
    
    year_wx = TIANGAN_WUXING[year_gan]
    favorable_wx = [w.value for w in wuxing.favorable]
    unfavorable_wx = [w.value for w in wuxing.unfavorable]
    
    # 流年五行与喜忌
    if year_wx in favorable_wx:
        score += 20
    elif year_wx in unfavorable_wx:
        score -= 15
    
    # 干支关系影响
    for _, rel_type, _ in relations:
        if rel_type == "合":
            score += 10
        elif rel_type == "冲":
            score -= 12
    
    # 随机因素（模拟其他复杂因素）
    score += (hash(f"{year_gan}{year_zhi}") % 10) - 5
    
    return max(25, min(95, score))


def _get_year_advice(
    year_wx: str,
    score: int,
    relations: list[tuple[str, str, str]]
) -> list[str]:
    """生成流年建议"""
    advice = []
    
    if score >= 80:
        advice.append("今年运势较好，可积极进取")
    elif score >= 60:
        advice.append("今年运势平稳，稳中求进")
    else:
        advice.append("今年运势一般，宜守不宜攻")
    
    # 根据五行添加建议
    matters = WUXING_MATTERS.get(year_wx, {})
    if score >= 70 and matters.get("favorable"):
        advice.append(f"有利事项：{matters['favorable'][0]}")
    if score < 60 and matters.get("unfavorable"):
        advice.append(f"注意事项：{matters['unfavorable'][0]}")
    
    # 根据关系添加建议
    for pillar, rel_type, _ in relations:
        if rel_type == "冲" and "日" in pillar:
            advice.append("流年冲日支，注意身体健康和感情稳定")
            break
    
    return advice


def calculate_liunian(
    bazi: BaziChart,
    wuxing: WuxingAnalysis,
    dayun_info: DaYunInfo | None = None,
    years: int = 10
) -> LiuNianAnalysis:
    """
    计算流年运势
    
    Args:
        bazi: 八字信息
        wuxing: 五行分析
        dayun_info: 大运信息（可选）
        years: 分析年数
    
    Returns:
        LiuNianAnalysis: 流年分析结果
    """
    current_year = datetime.now().year
    liunian_list = []
    
    for i in range(years):
        year = current_year + i
        year_gan, year_zhi = _get_year_ganzhi(year)
        ganzhi = f"{year_gan}{year_zhi}"
        
        # 流年五行
        year_wx = TIANGAN_WUXING[year_gan]
        
        # 纳音
        nayin = get_nayin(ganzhi)
        nayin_wx = get_nayin_wuxing(nayin)
        
        # 分析关系
        relations = _analyze_year_relations(year_gan, year_zhi, bazi)
        
        # 计算分数
        score = _calculate_year_score(year_gan, year_zhi, wuxing, relations)
        
        # 确定等级
        if score >= 85:
            level = "大吉"
        elif score >= 70:
            level = "吉"
        elif score >= 55:
            level = "平"
        elif score >= 40:
            level = "凶"
        else:
            level = "大凶"
        
        # 生成建议
        advice = _get_year_advice(year_wx, score, relations)
        
        # 主要事项
        key_events = []
        if score >= 80:
            key_events.append("事业有成")
        if any("合" in r[1] for r in relations):
            key_events.append("贵人相助")
        if any("冲" in r[1] for r in relations):
            key_events.append("变动较大")
        
        fortune = LiuNianFortune(
            year=year,
            ganzhi=ganzhi,
            wuxing=year_wx,
            nayin=nayin,
            score=score,
            level=level,
            key_events=key_events or ["运势平稳"],
            advice=advice,
            relations=[f"{p}: {t}" for p, t, _ in relations] if relations else ["无明显合冲"]
        )
        liunian_list.append(fortune)
    
    # 生成总结
    avg_score = sum(f.score for f in liunian_list) / len(liunian_list)
    best_years = sorted(liunian_list, key=lambda x: x.score, reverse=True)[:3]
    worst_years = sorted(liunian_list, key=lambda x: x.score)[:2]
    
    summary = (
        f"未来{years}年平均运势{avg_score:.0f}分。"
        f"较好年份：{', '.join(str(y.year) for y in best_years)}。"
        f"需注意：{', '.join(str(y.year) for y in worst_years)}。"
    )
    
    return LiuNianAnalysis(
        liunian_list=liunian_list,
        summary=summary,
        best_years=[y.year for y in best_years],
        caution_years=[y.year for y in worst_years]
    )
