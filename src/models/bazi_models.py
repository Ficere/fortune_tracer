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
    mu: float = Field(0, description="木")
    huo: float = Field(0, description="火")
    tu: float = Field(0, description="土")
    jin: float = Field(0, description="金")
    shui: float = Field(0, description="水")
    
    def to_dict(self) -> dict[str, float]:
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


class DaYun(BaseModel):
    """单步大运"""
    ganzhi: str = Field(..., description="干支")
    tiangan: str = Field(..., description="天干")
    dizhi: str = Field(..., description="地支")
    wuxing: str = Field(..., description="五行")
    start_age: int = Field(..., description="起始年龄")
    end_age: int = Field(..., description="结束年龄")
    start_year: int = Field(..., description="起始年份")
    end_year: int = Field(..., description="结束年份")


class DaYunInfo(BaseModel):
    """大运信息"""
    direction: str = Field(..., description="顺逆方向")
    start_age: int = Field(..., description="起运年龄")
    extra_months: int = Field(0, description="额外月份")
    dayun_list: list[DaYun] = Field(default_factory=list, description="大运列表")


class ShiShenInfo(BaseModel):
    """单柱十神信息"""
    pillar_name: str = Field(..., description="柱名")
    tiangan: str = Field(..., description="天干")
    dizhi: str = Field(..., description="地支")
    tiangan_shishen: str = Field(..., description="天干十神")
    dizhi_shishen: list[str] = Field(default_factory=list, description="地支藏干十神")
    dizhi_cangan: list[str] = Field(default_factory=list, description="地支藏干")


class ShiShenAnalysis(BaseModel):
    """十神分析结果"""
    shishen_list: list[ShiShenInfo] = Field(default_factory=list, description="四柱十神")
    shishen_count: dict[str, float] = Field(default_factory=dict, description="十神统计")
    pattern: str = Field("", description="格局")
    analysis: str = Field("", description="分析说明")


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

