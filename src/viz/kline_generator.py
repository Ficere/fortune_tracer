"""K线数据生成器 - 确保运势评级与K线形态匹配"""
from dataclasses import dataclass
from typing import Optional
from src.models.bazi_models import YearFortune


@dataclass
class KLineData:
    """单根K线数据"""
    year: int
    age: int
    open: float
    high: float
    low: float
    close: float
    score: float
    level: str
    hover_text: str


# 运势等级与K线形态的对应关系
KLINE_PARAMS = {
    "大吉": {"volatility": 8, "trend_bias": 1.0, "shadow_ratio": 0.3},   # 大阳线
    "吉": {"volatility": 6, "trend_bias": 0.7, "shadow_ratio": 0.4},     # 中阳线
    "小吉": {"volatility": 5, "trend_bias": 0.4, "shadow_ratio": 0.5},   # 小阳线
    "平": {"volatility": 4, "trend_bias": 0.0, "shadow_ratio": 0.6},     # 十字星
    "小凶": {"volatility": 5, "trend_bias": -0.4, "shadow_ratio": 0.5},  # 小阴线
    "凶": {"volatility": 6, "trend_bias": -0.7, "shadow_ratio": 0.4},    # 中阴线
    "大凶": {"volatility": 8, "trend_bias": -1.0, "shadow_ratio": 0.3},  # 大阴线
}


def generate_kline_data(fortunes: list[YearFortune]) -> list[KLineData]:
    """生成与运势评级匹配的K线数据
    
    核心原则：
    - K线收盘价 = 运势分数（保持一致性）
    - K线涨跌方向与评级匹配（吉则涨，凶则跌）
    - 波动幅度与评级程度成正比
    """
    klines = []
    prev_close = fortunes[0].score if fortunes else 60
    
    for f in fortunes:
        level = f.detail.level if f.detail else _get_level_from_score(f.score)
        params = KLINE_PARAMS.get(level, KLINE_PARAMS["平"])
        
        kline = _generate_single_kline(
            year=f.year,
            age=f.age,
            score=f.score,
            prev_close=prev_close,
            level=level,
            params=params,
            fortune=f
        )
        klines.append(kline)
        prev_close = f.score
    
    return klines


def _generate_single_kline(
    year: int, age: int, score: float, prev_close: float,
    level: str, params: dict, fortune: YearFortune
) -> KLineData:
    """生成单根K线

    核心原则：K线形态反映当年运势级别的"质量"
    - 吉类：实体饱满（收盘接近最高）
    - 凶类：实体下坠（收盘接近最低）
    - 波动幅度由运势变化决定
    """
    volatility = params["volatility"]
    shadow_ratio = params["shadow_ratio"]

    # 开盘价 = 前收盘价（保持连续性）
    open_price = prev_close
    # 收盘价 = 运势分数（核心锚定）
    close_price = score

    # 根据评级构建K线形态（而非单纯看涨跌）
    # 吉类：上影线短，下影线可以有
    # 凶类：下影线短，上影线可以有
    if level in ["大吉", "吉", "小吉"]:
        # 吉年形态：收盘接近最高点
        high_price = close_price + volatility * shadow_ratio * 0.3
        low_price = min(open_price, close_price) - volatility * shadow_ratio * 0.6
    elif level in ["大凶", "凶", "小凶"]:
        # 凶年形态：收盘接近最低点
        high_price = max(open_price, close_price) + volatility * shadow_ratio * 0.6
        low_price = close_price - volatility * shadow_ratio * 0.3
    else:  # 平
        # 十字星形态
        mid = (open_price + close_price) / 2
        high_price = mid + volatility * shadow_ratio
        low_price = mid - volatility * shadow_ratio

    # 确保合理范围
    high_price = min(high_price, 100)
    low_price = max(low_price, 20)

    # 确保K线数据有效
    high_price = max(high_price, open_price, close_price)
    low_price = min(low_price, open_price, close_price)

    # 生成hover文本
    change = close_price - open_price
    hover_text = _build_hover_text(fortune, level, change)

    return KLineData(
        year=year, age=age,
        open=round(open_price, 1),
        high=round(high_price, 1),
        low=round(low_price, 1),
        close=round(close_price, 1),
        score=score, level=level,
        hover_text=hover_text
    )


def _build_hover_text(fortune: YearFortune, level: str, change: float) -> str:
    """构建详细hover文本"""
    trend = "↑" if change > 0 else ("↓" if change < 0 else "→")
    text = f"{fortune.description}<br>{trend} {level}"
    
    if fortune.detail:
        text += f" {fortune.detail.emoji}"
        text += f"<br>五行: {fortune.wuxing} - {fortune.detail.wuxing_effect}"
        if fortune.detail.ganzhi_relations:
            relations = fortune.detail.ganzhi_relations[:2]
            text += f"<br>干支: {', '.join(relations)}"
    
    return text


def _get_level_from_score(score: float) -> str:
    """根据分数获取等级（简化版）"""
    if score >= 90: return "大吉"
    if score >= 80: return "吉"
    if score >= 70: return "小吉"
    if score >= 60: return "平"
    if score >= 50: return "小凶"
    if score >= 40: return "凶"
    return "大凶"

