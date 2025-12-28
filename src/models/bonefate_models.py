"""称骨算命数据模型"""

from datetime import datetime
from pydantic import BaseModel, Field


class LunarDate(BaseModel):
    """农历日期"""
    year: int = Field(..., description="农历年")
    month: int = Field(..., description="农历月")
    day: int = Field(..., description="农历日")
    hour: str = Field(..., description="时辰地支")


class SolarDate(BaseModel):
    """阳历日期"""
    year: int = Field(..., description="阳历年")
    month: int = Field(..., description="阳历月")
    day: int = Field(..., description="阳历日")
    hour: int = Field(..., description="小时(24小时制)")


class BoneFateResult(BaseModel):
    """称骨算命结果"""
    weight: float = Field(..., description="骨重(两)")
    weight_display: str = Field(..., description="骨重显示文本")
    level: str = Field(..., description="命格等级")
    level_desc: str = Field(..., description="等级描述")
    title: str = Field(..., description="命格标题")
    poem: str = Field(..., description="命运诗词")
    lunar_date: LunarDate = Field(..., description="农历日期")
    solar_date: SolarDate = Field(..., description="阳历日期")
    created_at: datetime = Field(default_factory=datetime.now)
    
    def to_json(self) -> str:
        """转换为JSON字符串"""
        return self.model_dump_json(indent=2, ensure_ascii=False)
    
    @classmethod
    def from_dict(cls, data: dict) -> "BoneFateResult":
        """从字典创建实例"""
        return cls(
            weight=data["weight"],
            weight_display=data["weight_display"],
            level=data["level"],
            level_desc=data["level_desc"],
            title=data["title"],
            poem=data["poem"],
            lunar_date=LunarDate(**data["lunar_date"]),
            solar_date=SolarDate(**data["solar_date"]),
        )


class BoneFateRequest(BaseModel):
    """称骨算命请求"""
    year: int = Field(..., ge=1900, le=2100, description="年份")
    month: int = Field(..., ge=1, le=12, description="月份")
    day: int = Field(..., ge=1, le=31, description="日期")
    hour: int = Field(..., ge=0, le=23, description="小时(24小时制)")
    is_lunar: bool = Field(default=False, description="是否农历")
