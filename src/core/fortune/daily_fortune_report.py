"""每日运势完整报告生成器"""
from datetime import date, timedelta
from src.models.bazi_models import BaziChart, WuxingAnalysis
from src.models.daily_fortune_models import DailyFortuneReport, get_fortune_level
from src.core.fortune.daily_fortune_engine import DailyFortuneEngine
from src.core.fortune.dimension_scorer import DimensionScorer
from src.core.fortune.hour_fortune import calculate_hour_fortunes, get_lucky_hours

# 五行对应方位、颜色、数字
WUXING_DIRECTION = {"木": "东方", "火": "南方", "土": "中宫", "金": "西方", "水": "北方"}
WUXING_COLOR = {"木": "绿色", "火": "红色", "土": "黄色", "金": "白色", "水": "黑蓝色"}
WUXING_NUMBER = {"木": "3, 8", "火": "2, 7", "土": "5, 0", "金": "4, 9", "水": "1, 6"}

# 适宜/不宜事项库
SUITABLE_ACTIONS = {
    "high": ["商务洽谈", "签订合同", "开业典礼", "求职面试", "重要会议", "投资决策"],
    "medium": ["日常工作", "学习进修", "社交聚会", "购物消费", "出行旅游"],
    "low": ["静心休息", "整理思路", "阅读学习", "家务整理"],
}
UNSUITABLE_ACTIONS = {
    "high": ["激烈运动", "长途出行"],
    "medium": ["重大决策", "争执辩论", "冒险投机", "借贷担保"],
    "low": ["签约承诺", "投资理财", "求职应聘", "手术就医", "远行出游"],
}


def generate_daily_fortune_report(
    target_date: date, bazi: BaziChart, wuxing: WuxingAnalysis
) -> DailyFortuneReport:
    """生成完整的每日运势报告"""
    # 1. 初始化计算引擎
    engine = DailyFortuneEngine(bazi, wuxing, target_date)
    
    # 2. 计算基础分数
    total_score, breakdown = engine.get_base_score()
    total_level, total_emoji, level_desc = get_fortune_level(total_score)
    
    # 3. 计算七维度评分
    scorer = DimensionScorer(engine)
    dimensions = scorer.calculate_all()
    
    # 4. 计算吉时
    hour_fortunes = calculate_hour_fortunes(target_date, engine.day_gan, bazi, wuxing)
    lucky_hours = get_lucky_hours(hour_fortunes, 3)
    
    # 5. 生成总结和行动指南
    summary = _generate_summary(total_score, engine.day_wx, wuxing, dimensions)
    suitable, unsuitable = _get_action_guide(total_score, dimensions)
    tips = _get_enhancement_tips(wuxing, engine.day_wx)
    
    # 6. 幸运属性
    favor_wx = wuxing.favorable[0].value if wuxing.favorable else engine.day_wx
    
    return DailyFortuneReport(
        target_date=target_date,
        day_ganzhi=f"{engine.day_gan}{engine.day_zhi}",
        day_wuxing=engine.day_wx,
        total_score=total_score,
        total_level=total_level,
        total_emoji=total_emoji,
        total_summary=summary,
        career=dimensions["career"],
        wealth=dimensions["wealth"],
        love=dimensions["love"],
        health=dimensions["health"],
        emotion=dimensions["emotion"],
        family=dimensions["family"],
        opportunity=dimensions["opportunity"],
        lucky_hours=lucky_hours,
        suitable_actions=suitable,
        unsuitable_actions=unsuitable,
        enhancement_tips=tips,
        lucky_direction=WUXING_DIRECTION.get(favor_wx, "中宫"),
        lucky_color=WUXING_COLOR.get(favor_wx, "中性色"),
        lucky_number=WUXING_NUMBER.get(favor_wx, "5"),
        score_breakdown=breakdown
    )


def _generate_summary(score: float, day_wx: str, wuxing: WuxingAnalysis, dims: dict) -> str:
    """生成运势总结"""
    favorable = [w.value for w in wuxing.favorable]
    is_favorable = day_wx in favorable
    
    # 找出最高和最低维度
    sorted_dims = sorted(dims.items(), key=lambda x: x[1].score, reverse=True)
    best = sorted_dims[0]
    worst = sorted_dims[-1]
    
    if score >= 80:
        base = "今日运势极佳，诸事皆宜" if is_favorable else "今日运势大好，把握机遇"
    elif score >= 65:
        base = "今日运势良好，适合推进重要事务"
    elif score >= 50:
        base = "今日运势平稳，按部就班即可"
    else:
        base = "今日运势欠佳，谨慎行事为上"
    
    return f"{base}。{best[1].name}最旺（{int(best[1].score)}分），需关注{worst[1].name}（{int(worst[1].score)}分）。"


def _get_action_guide(score: float, dims: dict) -> tuple[list, list]:
    """获取行动指南"""
    if score >= 75:
        suitable = SUITABLE_ACTIONS["high"][:4]
        unsuitable = UNSUITABLE_ACTIONS["high"][:2]
    elif score >= 55:
        suitable = SUITABLE_ACTIONS["medium"][:4]
        unsuitable = UNSUITABLE_ACTIONS["medium"][:3]
    else:
        suitable = SUITABLE_ACTIONS["low"][:3]
        unsuitable = UNSUITABLE_ACTIONS["low"][:4]
    
    # 根据维度调整
    if dims["wealth"].score >= 75:
        suitable.append("理财投资")
    if dims["love"].score >= 75:
        suitable.append("社交约会")
    if dims["health"].score < 50:
        unsuitable.append("剧烈运动")
    
    return suitable[:5], unsuitable[:5]


def _get_enhancement_tips(wuxing: WuxingAnalysis, day_wx: str) -> list[str]:
    """获取增运建议"""
    tips = []
    favor = wuxing.favorable[0].value if wuxing.favorable else day_wx
    
    tips.append(f"穿戴{WUXING_COLOR.get(favor, '中性')}系服饰增运")
    tips.append(f"{WUXING_DIRECTION.get(favor, '中宫')}方位活动有利")
    tips.append(f"数字{WUXING_NUMBER.get(favor, '5')}为今日幸运数")
    
    return tips

