"""每日运势计算模块"""
from datetime import datetime, date, timedelta
from pydantic import BaseModel, Field
from src.core.bazi.constants import (
    TIANGAN, DIZHI, TIANGAN_WUXING, DIZHI_WUXING,
    DIZHI_LIUHE, DIZHI_LIUCHONG, DIZHI_XING
)
from src.models.bazi_models import BaziChart, WuxingAnalysis


class DailyFortune(BaseModel):
    """单日运势"""
    date: date
    ganzhi: str = Field(..., description="日干支")
    wuxing: str = Field(..., description="五行")
    score: float = Field(..., ge=0, le=100)
    level: str = Field("平", description="运势等级")
    emoji: str = Field("😐", description="等级图标")
    summary: str = Field("", description="运势总结")
    suitable: list[str] = Field(default_factory=list, description="宜")
    unsuitable: list[str] = Field(default_factory=list, description="忌")
    tips: list[str] = Field(default_factory=list, description="增运建议")
    health_tip: str = Field("", description="健康提示")
    lucky_direction: str = Field("", description="吉方")
    lucky_color: str = Field("", description="幸运色")


def calculate_daily_fortune(
    target_date: date, bazi: BaziChart, wuxing: WuxingAnalysis
) -> DailyFortune:
    """计算指定日期的运势"""
    # 计算日干支
    day_gan, day_zhi = _get_day_ganzhi(target_date)
    ganzhi = f"{day_gan}{day_zhi}"
    day_wx = TIANGAN_WUXING[day_gan]
    
    # 计算运势分数
    score = _calculate_score(day_gan, day_zhi, bazi, wuxing)
    level, emoji = _get_level(score)
    
    # 生成建议
    suitable, unsuitable = _get_daily_activities(day_wx, score, wuxing)
    tips = _get_enhancement_tips(day_wx, wuxing)
    
    # 吉方和幸运色基于喜用神
    lucky_direction = _get_lucky_direction(wuxing.favorable[0].value if wuxing.favorable else day_wx)
    lucky_color = _get_lucky_color(wuxing.favorable[0].value if wuxing.favorable else day_wx)
    
    return DailyFortune(
        date=target_date,
        ganzhi=ganzhi,
        wuxing=day_wx,
        score=score,
        level=level,
        emoji=emoji,
        summary=_generate_summary(level, day_wx, wuxing),
        suitable=suitable,
        unsuitable=unsuitable,
        tips=tips,
        health_tip=_get_health_tip(day_wx),
        lucky_direction=lucky_direction,
        lucky_color=lucky_color
    )


def calculate_three_days_fortune(
    bazi: BaziChart, wuxing: WuxingAnalysis
) -> list[DailyFortune]:
    """计算今日、明日、后日三天运势"""
    today = date.today()
    return [
        calculate_daily_fortune(today, bazi, wuxing),
        calculate_daily_fortune(today + timedelta(days=1), bazi, wuxing),
        calculate_daily_fortune(today + timedelta(days=2), bazi, wuxing),
    ]


def _get_day_ganzhi(target_date: date) -> tuple[str, str]:
    """计算日干支（基于已知基准日推算）"""
    # 基准日：2000年1月1日是己亥日
    base_date = date(2000, 1, 1)
    base_gan_idx = 5  # 己
    base_zhi_idx = 11  # 亥
    
    days_diff = (target_date - base_date).days
    gan_idx = (base_gan_idx + days_diff) % 10
    zhi_idx = (base_zhi_idx + days_diff) % 12
    
    return TIANGAN[gan_idx], DIZHI[zhi_idx]


def _calculate_score(
    day_gan: str, day_zhi: str, bazi: BaziChart, wuxing: WuxingAnalysis
) -> float:
    """计算日运势分数"""
    score = 60.0
    day_wx = TIANGAN_WUXING[day_gan]
    
    # 喜忌判断
    favorable = [w.value for w in wuxing.favorable]
    unfavorable = [w.value for w in wuxing.unfavorable]
    
    if day_wx in favorable:
        score += 15
    elif day_wx in unfavorable:
        score -= 10
    
    # 地支关系
    bazi_zhis = [
        bazi.year_pillar.dizhi.value,
        bazi.month_pillar.dizhi.value,
        bazi.day_pillar.dizhi.value,
        bazi.hour_pillar.dizhi.value,
    ]
    
    for zhi in bazi_zhis:
        pair = tuple(sorted([day_zhi, zhi]))
        if pair in DIZHI_LIUHE or (pair[1], pair[0]) in DIZHI_LIUHE:
            score += 5
        if pair in DIZHI_LIUCHONG or (pair[1], pair[0]) in DIZHI_LIUCHONG:
            score -= 8
        if pair in DIZHI_XING or (pair[1], pair[0]) in DIZHI_XING:
            score -= 5
    
    return round(min(max(score, 30), 95), 1)


def _get_level(score: float) -> tuple[str, str]:
    """获取运势等级"""
    levels = [
        (85, "大吉", "🌟"), (75, "吉", "✨"), (65, "小吉", "😊"),
        (55, "平", "😐"), (45, "小凶", "😟"), (35, "凶", "⚠️"),
        (0, "大凶", "❌")
    ]
    for threshold, level, emoji in levels:
        if score >= threshold:
            return level, emoji
    return "平", "😐"


def _get_daily_activities(day_wx: str, score: float, wuxing: WuxingAnalysis) -> tuple[list, list]:
    """获取每日宜忌"""
    suitable_map = {
        "木": ["学习", "会友", "运动"],
        "火": ["社交", "谈判", "表演"],
        "土": ["签约", "置业", "养生"],
        "金": ["决策", "理财", "出行"],
        "水": ["冥想", "创作", "旅行"]
    }
    unsuitable_map = {
        "木": ["争吵", "诉讼"],
        "火": ["冒险", "投机"],
        "土": ["搬迁", "变动"],
        "金": ["冲动消费"],
        "水": ["重大决定"]
    }

    suitable = suitable_map.get(day_wx, ["保持平常心"])
    unsuitable = unsuitable_map.get(day_wx, ["急躁冒进"])

    if score >= 70:
        suitable.insert(0, "重要事务")
    elif score < 50:
        unsuitable.insert(0, "重大决策")

    return suitable[:4], unsuitable[:3]


def _get_enhancement_tips(day_wx: str, wuxing: WuxingAnalysis) -> list[str]:
    """获取增运建议"""
    tips_map = {
        "木": ["穿绿色衣物增运", "适合东方活动"],
        "火": ["红色配饰助运", "南方有利"],
        "土": ["黄色系增稳定", "居家养生为佳"],
        "金": ["白色金色吉利", "西方方位有利"],
        "水": ["黑蓝色增智慧", "北方活动顺利"]
    }
    return tips_map.get(day_wx, ["保持积极心态"])


def _get_lucky_direction(wx: str) -> str:
    """获取吉方"""
    direction_map = {"木": "东方", "火": "南方", "土": "中宫", "金": "西方", "水": "北方"}
    return direction_map.get(wx, "中宫")


def _get_lucky_color(wx: str) -> str:
    """获取幸运色"""
    color_map = {"木": "绿色", "火": "红色", "土": "黄色", "金": "白色", "水": "黑蓝色"}
    return color_map.get(wx, "中性色")


def _get_health_tip(day_wx: str) -> str:
    """获取健康提示"""
    health_map = {
        "木": "注意肝胆，适当舒展筋骨",
        "火": "注意心血管，避免过度兴奋",
        "土": "注意脾胃，饮食规律清淡",
        "金": "注意呼吸系统，保持空气流通",
        "水": "注意肾脏泌尿，多补充水分"
    }
    return health_map.get(day_wx, "保持良好作息")


def _generate_summary(level: str, day_wx: str, wuxing: WuxingAnalysis) -> str:
    """生成运势总结"""
    favorable = [w.value for w in wuxing.favorable]
    is_favorable = day_wx in favorable

    summaries = {
        "大吉": "今日运势极佳，诸事皆宜，可放手一搏" if is_favorable else "今日运势大好，把握机遇",
        "吉": "今日运势良好，适合推进重要事务",
        "小吉": "今日运势平顺，循序渐进为佳",
        "平": "今日运势平平，宜守不宜攻",
        "小凶": "今日运势欠佳，谨慎行事为上",
        "凶": "今日运势不利，避免重大决策",
        "大凶": "今日运势低迷，宜静不宜动，避免冲突"
    }
    return summaries.get(level, "今日运势一般，保持平常心")

