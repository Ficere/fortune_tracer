"""每日运势数据模型"""
from datetime import date
from pydantic import BaseModel, Field
from typing import Literal


class DimensionScore(BaseModel):
    """单维度运势评分"""
    name: str = Field(..., description="维度名称")
    score: float = Field(..., ge=0, le=100, description="评分")
    level: str = Field("平稳保守", description="等级标签")
    emoji: str = Field("😐", description="等级图标")
    factors: list[str] = Field(default_factory=list, description="成因分析")
    advice: list[str] = Field(default_factory=list, description="具体建议")
    keywords: list[str] = Field(default_factory=list, description="关键词")


class HourFortune(BaseModel):
    """时辰运势"""
    hour_zhi: str = Field(..., description="时辰地支")
    hour_name: str = Field(..., description="时辰名称")
    time_range: str = Field(..., description="时间范围")
    score: float = Field(..., ge=0, le=100)
    level: str = Field("平", description="等级")
    suitable: list[str] = Field(default_factory=list, description="适宜事项")


class DailyFortuneReport(BaseModel):
    """每日运势完整报告"""
    # 基础信息
    target_date: date = Field(..., description="目标日期")
    day_ganzhi: str = Field(..., description="日干支")
    day_wuxing: str = Field(..., description="日五行")
    
    # 总体评分
    total_score: float = Field(..., ge=0, le=100, description="总体评分")
    total_level: str = Field("平稳保守", description="总体等级")
    total_emoji: str = Field("😐", description="等级图标")
    total_summary: str = Field("", description="总体概述")
    
    # 七维度评分
    career: DimensionScore = Field(..., description="事业学业运")
    wealth: DimensionScore = Field(..., description="财富运势")
    love: DimensionScore = Field(..., description="感情人际运")
    health: DimensionScore = Field(..., description="健康体能运")
    emotion: DimensionScore = Field(..., description="心态情绪运")
    family: DimensionScore = Field(..., description="家庭生活运")
    opportunity: DimensionScore = Field(..., description="机遇贵人运")
    
    # 吉时推荐
    lucky_hours: list[HourFortune] = Field(default_factory=list, description="吉时列表")
    
    # 行为指南
    suitable_actions: list[str] = Field(default_factory=list, description="适宜事项")
    unsuitable_actions: list[str] = Field(default_factory=list, description="不宜事项")
    
    # 增运建议
    enhancement_tips: list[str] = Field(default_factory=list, description="增运建议")
    lucky_direction: str = Field("", description="吉方")
    lucky_color: str = Field("", description="幸运色")
    lucky_number: str = Field("", description="幸运数字")
    
    # 计算因素追溯
    score_breakdown: dict = Field(default_factory=dict, description="评分明细")


# 等级体系
FORTUNE_LEVELS = [
    (90, "大吉主动", "🌟", "运势极佳，可大胆行动"),
    (75, "良好推进", "✨", "运势向好，适合推进计划"),
    (60, "平稳保守", "😊", "运势平稳，按部就班即可"),
    (40, "谨慎观望", "😐", "运势一般，宜观望少动"),
    (20, "小心应对", "😟", "运势欠佳，需谨慎行事"),
    (0, "暂避锋芒", "⚠️", "运势低迷，宜静不宜动"),
]


def get_fortune_level(score: float) -> tuple[str, str, str]:
    """获取运势等级"""
    for threshold, level, emoji, desc in FORTUNE_LEVELS:
        if score >= threshold:
            return level, emoji, desc
    return "暂避锋芒", "⚠️", "运势低迷，宜静不宜动"

