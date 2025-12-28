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
    ShenShaInfo,
    ShenShaAnalysis,
    NaYinInfo,
    LiuNianFortune,
    LiuNianAnalysis,
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
from .bonefate_models import (
    LunarDate,
    SolarDate,
    BoneFateResult,
    BoneFateRequest,
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
    "ShenShaInfo",
    "ShenShaAnalysis",
    "NaYinInfo",
    "LiuNianFortune",
    "LiuNianAnalysis",
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
    # bonefate_models
    "LunarDate",
    "SolarDate",
    "BoneFateResult",
    "BoneFateRequest",
]

