"""数据模型模块"""
from .bazi_models import (
    TianGan,
    DiZhi,
    Wuxing,
    Gender,
    BaziPillar,
    BaziChart,
    WuxingCount,
    WuxingAnalysis,
    YearFortune,
    DaYun,
    DaYunInfo,
    ShiShenInfo,
    ShiShenAnalysis,
    AIInterpretation,
    FortuneReport,
)
from .compatibility_models import (
    RelationshipType,
    CompatibilityResult,
    WuxingCompatibility,
    GanZhiRelations,
    CompatibilityAdvice,
)
from .date_selection_models import (
    EventType,
    DayQuality,
    DayInfo,
    DateRecommendation,
)

__all__ = [
    # bazi_models
    "TianGan",
    "DiZhi",
    "Wuxing",
    "Gender",
    "BaziPillar",
    "BaziChart",
    "WuxingCount",
    "WuxingAnalysis",
    "YearFortune",
    "DaYun",
    "DaYunInfo",
    "ShiShenInfo",
    "ShiShenAnalysis",
    "AIInterpretation",
    "FortuneReport",
    # compatibility_models
    "RelationshipType",
    "CompatibilityResult",
    "WuxingCompatibility",
    "GanZhiRelations",
    "CompatibilityAdvice",
    # date_selection_models
    "EventType",
    "DayQuality",
    "DayInfo",
    "DateRecommendation",
]

