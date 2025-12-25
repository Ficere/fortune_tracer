"""八字配对数据模型"""
from datetime import datetime
from pydantic import BaseModel, Field
from .bazi_models import BaziChart, WuxingAnalysis


class RelationshipType(BaseModel):
    """干支关系类型"""
    relation: str = Field(..., description="关系类型")
    elements: list[str] = Field(default_factory=list, description="涉及元素")
    score_impact: int = Field(0, description="分数影响")
    description: str = Field("", description="关系描述")


class WuxingCompatibility(BaseModel):
    """五行互补分析"""
    complementary: list[str] = Field(default_factory=list, description="互补五行")
    conflicting: list[str] = Field(default_factory=list, description="冲突五行")
    balance_score: int = Field(0, ge=0, le=100, description="平衡得分")
    analysis: str = Field("", description="分析说明")


class GanZhiRelations(BaseModel):
    """天干地支关系分析"""
    tiangan_he: list[RelationshipType] = Field(default_factory=list, description="天干相合")
    tiangan_chong: list[RelationshipType] = Field(default_factory=list, description="天干相冲")
    dizhi_he: list[RelationshipType] = Field(default_factory=list, description="地支六合")
    dizhi_chong: list[RelationshipType] = Field(default_factory=list, description="地支六冲")
    dizhi_sanhe: list[RelationshipType] = Field(default_factory=list, description="地支三合")
    dizhi_xing: list[RelationshipType] = Field(default_factory=list, description="地支相刑")


class CompatibilityAdvice(BaseModel):
    """配对建议"""
    strengths: list[str] = Field(default_factory=list, description="优势方面")
    challenges: list[str] = Field(default_factory=list, description="挑战方面")
    suggestions: list[str] = Field(default_factory=list, description="相处建议")
    cautions: list[str] = Field(default_factory=list, description="注意事项")


class CompatibilityResult(BaseModel):
    """配对分析结果"""
    person1_bazi: BaziChart
    person2_bazi: BaziChart
    person1_wuxing: WuxingAnalysis
    person2_wuxing: WuxingAnalysis
    wuxing_compat: WuxingCompatibility
    ganzhi_relations: GanZhiRelations
    total_score: int = Field(..., ge=0, le=100, description="总配对得分")
    grade: str = Field(..., description="评级")
    advice: CompatibilityAdvice
    created_at: datetime = Field(default_factory=datetime.now)

    def to_json(self) -> str:
        return self.model_dump_json(indent=2)

