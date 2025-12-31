"""择日计算模块"""
from datetime import date, timedelta, datetime
from src.models import BaziChart, WuxingAnalysis
from src.models.date_selection_models import (
    EventType, DayQuality, DayInfo, DateRecommendation
)
from src.core.bazi.constants import TIANGAN, DIZHI, TIANGAN_WUXING, DIZHI_LIUCHONG
from src.core.bazi.pillars import _get_day_pillar

# 事件与五行关系
EVENT_WUXING = {
    EventType.WEDDING: ["火", "木"],
    EventType.BUSINESS: ["金", "土"],
    EventType.MOVING: ["水", "木"],
    EventType.TRAVEL: ["水", "木"],
    EventType.SIGNING: ["金", "水"],
}

# 默认宜忌事项
DEFAULT_SUITABLE = {
    EventType.WEDDING: ["嫁娶", "订盟", "纳采", "祭祀", "祈福"],
    EventType.BUSINESS: ["开市", "交易", "立券", "纳财", "开光"],
    EventType.MOVING: ["入宅", "移徙", "安床", "安香", "祭祀"],
    EventType.TRAVEL: ["出行", "旅游", "上任", "赴任"],
    EventType.SIGNING: ["签约", "交易", "立券", "会友", "求财"],
}

# 地支对应生肖
DIZHI_SHENGXIAO = {
    "子": "鼠", "丑": "牛", "寅": "虎", "卯": "兔",
    "辰": "龙", "巳": "蛇", "午": "马", "未": "羊",
    "申": "猴", "酉": "鸡", "戌": "狗", "亥": "猪"
}


def _get_clash_zodiac(dizhi: str) -> str:
    """获取冲的生肖"""
    for (a, b), _ in DIZHI_LIUCHONG.items():
        if a == dizhi:
            return DIZHI_SHENGXIAO.get(b, "")
        if b == dizhi:
            return DIZHI_SHENGXIAO.get(a, "")
    return ""


def _calculate_day_score(
    day_pillar_gz: str,
    wuxing: WuxingAnalysis,
    event: EventType
) -> tuple[int, DayQuality]:
    """计算日期得分"""
    day_gan = day_pillar_gz[0]
    day_wx = TIANGAN_WUXING.get(day_gan, "土")
    
    score = 60  # 基础分
    
    # 事件相关五行加分
    event_wx = EVENT_WUXING.get(event, [])
    if day_wx in event_wx:
        score += 15
    
    # 喜用神加分
    favorable_wx = [w.value for w in wuxing.favorable]
    if day_wx in favorable_wx:
        score += 20
    
    # 忌神减分
    unfavorable_wx = [w.value for w in wuxing.unfavorable]
    if day_wx in unfavorable_wx:
        score -= 15
    
    # 随机因素（模拟黄历复杂计算）
    score += (hash(day_pillar_gz) % 15) - 7
    score = max(20, min(95, score))
    
    # 确定质量
    if score >= 85:
        quality = DayQuality.EXCELLENT
    elif score >= 70:
        quality = DayQuality.GOOD
    elif score >= 50:
        quality = DayQuality.NEUTRAL
    elif score >= 35:
        quality = DayQuality.BAD
    else:
        quality = DayQuality.TERRIBLE
    
    return score, quality


def _get_suitable_avoid(
    event: EventType, quality: DayQuality
) -> tuple[list[str], list[str]]:
    """获取宜忌事项"""
    base_suitable = DEFAULT_SUITABLE.get(event, [])[:3]
    
    if quality in [DayQuality.EXCELLENT, DayQuality.GOOD]:
        suitable = base_suitable + ["祭祀", "祈福"]
        avoid = ["诉讼", "安葬"]
    elif quality == DayQuality.NEUTRAL:
        suitable = base_suitable[:2]
        avoid = ["嫁娶", "开市", "动土"]
    else:
        suitable = ["祭祀"]
        avoid = base_suitable + ["出行", "动土"]
    
    return suitable, avoid


def select_dates(
    bazi: BaziChart,
    wuxing: WuxingAnalysis,
    event: EventType,
    start_date: date,
    days: int = 30
) -> DateRecommendation:
    """择日推荐"""
    recommended, avoided = [], []
    
    for i in range(days):
        current = start_date + timedelta(days=i)
        dt = datetime(current.year, current.month, current.day, 12)
        pillar = _get_day_pillar(dt)
        ganzhi = pillar.display
        
        score, quality = _calculate_day_score(ganzhi, wuxing, event)
        suitable, avoid = _get_suitable_avoid(event, quality)
        clash = _get_clash_zodiac(pillar.dizhi.value)
        
        day_info = DayInfo(
            date=current,
            ganzhi=ganzhi,
            quality=quality,
            score=score,
            suitable=suitable,
            avoid=avoid,
            clash_zodiac=clash,
            analysis=f"{ganzhi}日，{quality.value}"
        )
        
        if quality in [DayQuality.EXCELLENT, DayQuality.GOOD]:
            recommended.append(day_info)
        elif quality in [DayQuality.BAD, DayQuality.TERRIBLE]:
            avoided.append(day_info)
    
    # 排序
    recommended.sort(key=lambda x: x.score, reverse=True)
    avoided.sort(key=lambda x: x.score)
    
    summary = f"未来{days}天内，推荐{len(recommended)}个吉日，需避开{len(avoided)}个凶日"
    
    return DateRecommendation(
        event_type=event,
        recommended_dates=recommended[:10],
        avoid_dates=avoided[:5],
        summary=summary
    )

