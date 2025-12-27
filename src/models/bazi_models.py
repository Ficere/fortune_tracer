"""八字数据模型定义"""
from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class TianGan(str, Enum):
    """十天干"""
    JIA = "甲"
    YI = "乙"
    BING = "丙"
    DING = "丁"
    WU = "戊"
    JI = "己"
    GENG = "庚"
    XIN = "辛"
    REN = "壬"
    GUI = "癸"


class DiZhi(str, Enum):
    """十二地支"""
    ZI = "子"
    CHOU = "丑"
    YIN = "寅"
    MAO = "卯"
    CHEN = "辰"
    SI = "巳"
    WU = "午"
    WEI = "未"
    SHEN = "申"
    YOU = "酉"
    XU = "戌"
    HAI = "亥"


class Wuxing(str, Enum):
    """五行"""
    MU = "木"
    HUO = "火"
    TU = "土"
    JIN = "金"
    SHUI = "水"


class Gender(str, Enum):
    """性别"""
    MALE = "男"
    FEMALE = "女"


class BaziPillar(BaseModel):
    """八字单柱"""
    tiangan: TianGan = Field(..., description="天干")
    dizhi: DiZhi = Field(..., description="地支")
    
    @property
    def display(self) -> str:
        return f"{self.tiangan.value}{self.dizhi.value}"


class BaziChart(BaseModel):
    """完整八字盘"""
    year_pillar: BaziPillar = Field(..., description="年柱")
    month_pillar: BaziPillar = Field(..., description="月柱")
    day_pillar: BaziPillar = Field(..., description="日柱")
    hour_pillar: BaziPillar = Field(..., description="时柱")
    birth_datetime: datetime = Field(..., description="出生时间")
    gender: Gender = Field(..., description="性别")
    birth_place: Optional[str] = Field(None, description="出生地点")


class WuxingCount(BaseModel):
    """五行统计"""
    mu: int = Field(0, description="木")
    huo: int = Field(0, description="火")
    tu: int = Field(0, description="土")
    jin: int = Field(0, description="金")
    shui: int = Field(0, description="水")
    
    def to_dict(self) -> dict[str, int]:
        return {"木": self.mu, "火": self.huo, "土": self.tu, "金": self.jin, "水": self.shui}


class WuxingAnalysis(BaseModel):
    """五行分析结果"""
    counts: WuxingCount = Field(..., description="五行数量统计")
    day_master: Wuxing = Field(..., description="日主五行")
    day_master_strength: str = Field(..., description="日主强弱")
    favorable: list[Wuxing] = Field(default_factory=list, description="喜用神")
    unfavorable: list[Wuxing] = Field(default_factory=list, description="忌神")


class YearFortune(BaseModel):
    """流年运势"""
    year: int
    score: float = Field(..., ge=0, le=100)
    description: str


class AIInterpretation(BaseModel):
    """AI解读结果"""
    personality: str = Field(..., description="性格特点")
    career: str = Field(..., description="事业运势")
    love: str = Field(..., description="感情运势")
    health: str = Field(..., description="健康建议")
    wealth: str = Field(..., description="财运分析")
    summary: str = Field(..., description="综合评价")


class FortuneReport(BaseModel):
    """完整命理报告"""
    bazi: BaziChart
    wuxing: WuxingAnalysis
    interpretation: Optional[AIInterpretation] = None
    year_fortunes: list[YearFortune] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)
    
    def to_json(self) -> str:
        return self.model_dump_json(indent=2)

