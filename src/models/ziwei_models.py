"""紫微斗数数据模型"""
from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class StarType(str, Enum):
    """星曜类型"""
    MAIN = "主星"      # 14主星
    AUX = "辅星"       # 左辅右弼等
    SHA = "煞星"       # 擎羊陀罗等
    HUA = "四化"       # 化禄权科忌
    MISC = "杂曜"      # 其他


class Palace(str, Enum):
    """十二宫位"""
    MING = "命宫"
    XIONGDI = "兄弟宫"
    FUQI = "夫妻宫"
    ZINV = "子女宫"
    CAIBO = "财帛宫"
    JIEE = "疾厄宫"
    QIANYI = "迁移宫"
    NUPU = "奴仆宫"
    GUANLU = "官禄宫"
    TIANZHAI = "田宅宫"
    FUDE = "福德宫"
    FUMU = "父母宫"


class WuxingJu(str, Enum):
    """五行局（定紫微位置的关键）"""
    SHUI_ER = "水二局"
    MU_SAN = "木三局"
    JIN_SI = "金四局"
    TU_WU = "土五局"
    HUO_LIU = "火六局"


class Star(BaseModel):
    """星曜信息"""
    name: str = Field(..., description="星名")
    star_type: StarType = Field(..., description="星曜类型")
    brightness: str = Field("", description="亮度：庙旺得利平陷")
    sihua: str = Field("", description="四化：禄权科忌")
    description: str = Field("", description="星曜特性描述")


class PalaceInfo(BaseModel):
    """宫位信息"""
    palace: Palace = Field(..., description="宫位名称")
    position: int = Field(..., ge=0, lt=12, description="位置索引(0-11)")
    dizhi: str = Field(..., description="地支")
    tiangan: str = Field(..., description="天干")
    main_stars: list[Star] = Field(default_factory=list, description="主星")
    aux_stars: list[Star] = Field(default_factory=list, description="辅星")
    sha_stars: list[Star] = Field(default_factory=list, description="煞星")
    analysis: str = Field("", description="宫位解读")


class ZiweiChart(BaseModel):
    """紫微斗数星盘"""
    # 基本信息
    birth_datetime: datetime = Field(..., description="出生时间")
    lunar_year: int = Field(..., description="农历年")
    lunar_month: int = Field(..., description="农历月")
    lunar_day: int = Field(..., description="农历日")
    hour_zhi: str = Field(..., description="时辰地支")
    gender: str = Field(..., description="性别")
    
    # 命盘核心
    wuxing_ju: WuxingJu = Field(..., description="五行局")
    ming_gong_pos: int = Field(..., description="命宫位置")
    shen_gong_pos: int = Field(..., description="身宫位置")
    
    # 十二宫
    palaces: list[PalaceInfo] = Field(default_factory=list, description="十二宫位")
    
    # 四化
    sihua_stars: dict[str, str] = Field(default_factory=dict, description="四化星")


class ZiweiAnalysis(BaseModel):
    """紫微斗数分析结果"""
    chart: ZiweiChart = Field(..., description="星盘")
    personality: str = Field("", description="性格特点")
    career: str = Field("", description="事业分析")
    wealth: str = Field("", description="财运分析")
    love: str = Field("", description="感情分析")
    health: str = Field("", description="健康分析")
    summary: str = Field("", description="综合评价")


# 简化的宫位描述模型
class PalaceSummary(BaseModel):
    """宫位摘要"""
    name: str
    stars: list[str]
    score: int = Field(60, ge=0, le=100)
    keywords: list[str] = Field(default_factory=list)

