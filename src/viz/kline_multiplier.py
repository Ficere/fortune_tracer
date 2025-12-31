"""乘法模式K线生成器 - 产生自然复利波动效果"""
from dataclasses import dataclass
from src.models.bazi_models import YearFortune


@dataclass
class MultiplierKLine:
    """乘法模式K线数据"""
    year: int
    age: int
    open: float
    high: float
    low: float
    close: float
    multiplier: float
    level: str
    hover_text: str


# 运势等级对应的涨跌乘数
FORTUNE_MULTIPLIERS = {
    "大吉": 1.12,   # 涨12%
    "吉":   1.08,   # 涨8%
    "小吉": 1.04,   # 涨4%
    "平":   1.00,   # 持平
    "小凶": 0.97,   # 跌3%
    "凶":   0.93,   # 跌7%
    "大凶": 0.88,   # 跌12%
}

# 影线参数（按等级配置）
SHADOW_CONFIG = {
    "大吉": {"upper": 0.02, "lower": 0.04},
    "吉":   {"upper": 0.025, "lower": 0.035},
    "小吉": {"upper": 0.03, "lower": 0.03},
    "平":   {"upper": 0.035, "lower": 0.035},
    "小凶": {"upper": 0.035, "lower": 0.025},
    "凶":   {"upper": 0.04, "lower": 0.02},
    "大凶": {"upper": 0.05, "lower": 0.015},
}


def generate_multiplier_klines(
    fortunes: list[YearFortune],
    base_price: float = 100.0
) -> list[MultiplierKLine]:
    """生成乘法模式K线数据
    
    优点：
    1. 自然的复利波动，连续好年份则指数增长
    2. 无需硬编码上下限，K线自然展开
    3. 保持命理评级与K线形态的一致性
    """
    klines = []
    current_price = base_price
    
    for f in fortunes:
        level = f.detail.level if f.detail else _get_level_from_score(f.score)
        multiplier = FORTUNE_MULTIPLIERS.get(level, 1.0)
        
        open_price = current_price
        close_price = open_price * multiplier
        
        high_price, low_price = _calc_shadow(open_price, close_price, level)
        
        klines.append(MultiplierKLine(
            year=f.year, age=f.age,
            open=round(open_price, 2),
            high=round(high_price, 2),
            low=round(low_price, 2),
            close=round(close_price, 2),
            multiplier=multiplier,
            level=level,
            hover_text=_build_hover(f, level, multiplier)
        ))
        
        current_price = close_price
    
    return klines


def _calc_shadow(open_p: float, close_p: float, level: str) -> tuple[float, float]:
    """根据等级计算影线"""
    config = SHADOW_CONFIG.get(level, {"upper": 0.03, "lower": 0.03})
    max_price = max(open_p, close_p)
    min_price = min(open_p, close_p)
    
    high = max_price * (1 + config["upper"])
    low = min_price * (1 - config["lower"])
    
    return high, max(low, 1)


def _build_hover(f: YearFortune, level: str, mult: float) -> str:
    """生成hover文本"""
    pct = (mult - 1) * 100
    trend = "↑" if pct > 0 else ("↓" if pct < 0 else "→")
    text = f"{f.description}<br>{trend} {level} ({pct:+.1f}%)"
    
    if f.detail:
        text += f" {f.detail.emoji}"
        text += f"<br>五行: {f.wuxing} - {f.detail.wuxing_effect}"
        if f.detail.ganzhi_relations:
            relations = f.detail.ganzhi_relations[:2]
            text += f"<br>干支: {', '.join(relations)}"
    
    return text


def _get_level_from_score(score: float) -> str:
    """根据分数获取等级"""
    if score >= 85: return "大吉"
    if score >= 75: return "吉"
    if score >= 65: return "小吉"
    if score >= 55: return "平"
    if score >= 45: return "小凶"
    if score >= 35: return "凶"
    return "大凶"

