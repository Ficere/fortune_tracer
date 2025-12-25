"""择日数据模型"""
from datetime import date
from enum import Enum
from pydantic import BaseModel, Field


class EventType(str, Enum):
    """事件类型"""
    WEDDING = "结婚"
    BUSINESS = "开业"
    MOVING = "搬家"
    TRAVEL = "出行"
    SIGNING = "签约"


class DayQuality(str, Enum):
    """日期质量"""
    EXCELLENT = "大吉"
    GOOD = "吉"
    NEUTRAL = "平"
    BAD = "凶"
    TERRIBLE = "大凶"


class DayInfo(BaseModel):
    """单日信息"""
    date: date
    ganzhi: str = Field(..., description="干支")
    quality: DayQuality = Field(..., description="吉凶")
    score: int = Field(..., ge=0, le=100, description="得分")
    suitable: list[str] = Field(default_factory=list, description="宜")
    avoid: list[str] = Field(default_factory=list, description="忌")
    clash_zodiac: str = Field("", description="冲生肖")
    analysis: str = Field("", description="分析说明")


class DateRecommendation(BaseModel):
    """择日推荐结果"""
    event_type: EventType
    recommended_dates: list[DayInfo] = Field(default_factory=list)
    avoid_dates: list[DayInfo] = Field(default_factory=list)
    summary: str = Field("", description="总结")

    def to_json(self) -> str:
        return self.model_dump_json(indent=2)

