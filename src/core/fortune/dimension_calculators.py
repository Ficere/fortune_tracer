"""各维度评分计算器 - 拆分自dimension_scorer"""
from src.models.daily_fortune_models import DimensionScore, get_fortune_level
from src.core.fortune.dimension_advice import ADVICE_FUNCS

# 十神与各维度的关联权重
SHISHEN_WEIGHTS = {
    "career": {"正官": 15, "七杀": 10, "正印": 8, "偏印": 6, "食神": 5, "伤官": -5, "劫财": -8},
    "wealth": {"正财": 18, "偏财": 15, "食神": 8, "伤官": 10, "劫财": -15, "比肩": -5},
    "love": {"正财": 12, "偏财": 8, "正官": 10, "七杀": 5, "食神": 6, "伤官": -8},
    "health": {"正印": 12, "偏印": 8, "食神": 10, "七杀": -12, "伤官": -8, "劫财": -6},
    "emotion": {"正印": 15, "食神": 12, "正官": 6, "伤官": -15, "七杀": -10, "劫财": -8},
    "family": {"正印": 15, "正财": 12, "食神": 8, "伤官": -10, "劫财": -12, "七杀": -8},
    "opportunity": {"偏财": 15, "偏印": 10, "七杀": 8, "食神": 6, "正官": 5, "劫财": -5},
}

# 维度配置
DIM_CONFIG = {
    "career": {"name": "事业学业运", "base": 60},
    "wealth": {"name": "财富运势", "base": 60},
    "love": {"name": "感情人际运", "base": 60},
    "health": {"name": "健康体能运", "base": 65},
    "emotion": {"name": "心态情绪运", "base": 62},
    "family": {"name": "家庭生活运", "base": 63},
    "opportunity": {"name": "机遇贵人运", "base": 58},
}

# 十神因素描述
SHISHEN_FACTORS = {
    "career": {
        "positive": ["正官", "七杀", "正印", "偏印", "食神"],
        "negative": ["伤官", "劫财"],
        "pos_text": "利于事业发展", "neg_text": "不利于事业发展"
    },
    "wealth": {
        "positive": ["正财", "偏财"],
        "negative": ["劫财"],
        "pos_text": "财运亨通", "neg_text": "注意破财风险"
    },
    "love": {
        "positive": ["正财", "正官", "偏财"],
        "negative": ["伤官"],
        "pos_text": "感情稳定", "neg_text": "言语需谨慎"
    },
    "health": {
        "positive": ["正印", "食神"],
        "negative": ["七杀", "伤官"],
        "pos_text": "身心舒畅", "neg_text": "注意身体劳损"
    },
    "emotion": {
        "positive": ["正印", "食神"],
        "negative": ["伤官", "七杀"],
        "pos_text": "心境平和", "neg_text": "情绪易波动"
    },
    "family": {
        "positive": ["正印", "正财"],
        "negative": ["劫财", "伤官"],
        "pos_text": "家庭和睦", "neg_text": "家庭易有摩擦"
    },
    "opportunity": {
        "positive": ["偏财", "偏印"],
        "negative": [],
        "pos_text": "偏门机遇多", "neg_text": ""
    },
}

# 关键词
KEYWORDS = {
    "career": (["项目推进", "团队合作"], ["稳扎稳打", "避免冲突"]),
    "wealth": (["稳健理财", "把握机会"], ["谨慎消费", "避免投机"]),
    "love": (["感情升温", "贵人相助"], ["保持耐心", "避免争执"]),
    "health": (["精力充沛", "适度运动"], ["注意休息", "避免过劳"]),
    "emotion": (["心态稳定", "判断准确"], ["调节情绪", "避免冲动"]),
    "family": (["家庭和谐", "亲情温暖"], ["多些包容", "避免争吵"]),
    "opportunity": (["贵人相助", "把握时机"], ["主动出击", "创造机会"]),
}


def create_dimension(key: str, score: float, factors: list) -> DimensionScore:
    """创建维度评分对象"""
    config = DIM_CONFIG[key]
    level, emoji, _ = get_fortune_level(score)
    advice = ADVICE_FUNCS[key](score)
    keywords = KEYWORDS[key][0] if score >= 70 else KEYWORDS[key][1]
    
    return DimensionScore(
        name=config["name"], score=round(score, 0), level=level, emoji=emoji,
        factors=factors, advice=advice, keywords=keywords
    )


def calc_dimension(key: str, day_shishen: str, day_wx: str, 
                   favorable: list, unfavorable: list, dizhi_score: float) -> DimensionScore:
    """通用维度计算"""
    score = DIM_CONFIG[key]["base"]
    factors = []
    
    # 十神影响
    shishen_bonus = SHISHEN_WEIGHTS[key].get(day_shishen, 0)
    score += shishen_bonus
    
    factor_info = SHISHEN_FACTORS[key]
    if day_shishen in factor_info["positive"]:
        factors.append(f"{day_shishen}当值，{factor_info['pos_text']}")
    elif day_shishen in factor_info["negative"]:
        factors.append(f"{day_shishen}流日，{factor_info['neg_text']}")
    
    # 喜用神影响
    if day_wx in favorable:
        score += 10
        factors.append("喜用神当值")
    elif day_wx in unfavorable:
        score -= 8
    
    # 地支冲合影响（不同维度权重不同）
    zhi_weight = {"career": 0.5, "love": 0.8, "health": 0.6, "opportunity": 1.0}.get(key, 0.3)
    score += dizhi_score * zhi_weight
    
    if key == "love" and dizhi_score > 0:
        factors.append("地支相合，人际和谐")
    if key == "health" and dizhi_score < -10:
        factors.append("地支相冲，注意意外")
    if key == "opportunity" and dizhi_score > 5:
        factors.append("地支相合，贵人运旺")
    
    return create_dimension(key, min(max(score, 20), 95), factors)

