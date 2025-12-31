"""七维度运势评分系统 - 使用通用计算器"""
from src.models.daily_fortune_models import DimensionScore
from src.core.fortune.daily_fortune_engine import DailyFortuneEngine
from src.core.fortune.dimension_calculators import calc_dimension

DIMENSION_KEYS = ["career", "wealth", "love", "health", "emotion", "family", "opportunity"]


class DimensionScorer:
    """七维度评分器"""

    def __init__(self, engine: DailyFortuneEngine):
        self.engine = engine
        self.day_shishen = engine.factors.get("day_shishen", "比肩")
        self.day_wx = engine.day_wx
        self.favorable = engine.favorable
        self.unfavorable = engine.unfavorable
        self.dizhi_score = engine.factors["scores"].get("dizhi", 0)

    def calculate_all(self) -> dict[str, DimensionScore]:
        """计算所有维度评分"""
        return {key: self._calc(key) for key in DIMENSION_KEYS}

    def _calc(self, key: str) -> DimensionScore:
        """计算单个维度"""
        return calc_dimension(
            key, self.day_shishen, self.day_wx,
            self.favorable, self.unfavorable, self.dizhi_score
        )

