"""API请求和响应模型"""
from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel, Field


class BirthInfo(BaseModel):
    """出生信息请求"""
    birth_datetime: datetime = Field(..., description="出生时间")
    gender: str = Field(..., pattern="^(男|女)$", description="性别")
    birth_place: Optional[str] = Field(None, description="出生地点")


class BaziAnalyzeRequest(BaseModel):
    """八字分析请求"""
    birth_info: BirthInfo
    api_key: Optional[str] = Field(None, description="OpenAI API Key")
    include_dayun: bool = Field(True, description="是否包含大运")
    include_shishen: bool = Field(True, description="是否包含十神")
    include_shensha: bool = Field(True, description="是否包含神煞")
    include_nayin: bool = Field(True, description="是否包含纳音")


class CompatibilityRequest(BaseModel):
    """配对分析请求"""
    person1: BirthInfo
    person2: BirthInfo


class DateSelectionRequest(BaseModel):
    """择日分析请求"""
    birth_info: BirthInfo
    event_type: str = Field(..., description="事件类型: 结婚/开业/搬家/出行/签约")
    start_date: date = Field(default_factory=date.today, description="起始日期")
    search_days: int = Field(30, ge=7, le=90, description="搜索天数")


class DayunRequest(BaseModel):
    """大运计算请求"""
    birth_info: BirthInfo
    num_dayun: int = Field(8, ge=1, le=12, description="大运数量")


class ShiShenRequest(BaseModel):
    """十神分析请求"""
    birth_info: BirthInfo


class ShenShaRequest(BaseModel):
    """神煞分析请求"""
    birth_info: BirthInfo


class NaYinRequest(BaseModel):
    """纳音分析请求"""
    birth_info: BirthInfo


class YearNaYinRequest(BaseModel):
    """年命纳音请求"""
    year: int = Field(..., ge=1900, le=2100, description="年份")


class AuxiliaryRequest(BaseModel):
    """辅助宫位请求"""
    birth_info: BirthInfo


class GongInfoResponse(BaseModel):
    """宫位信息响应"""
    name: str
    tiangan: str
    dizhi: str
    ganzhi: str
    description: str


class AuxiliaryResponse(BaseModel):
    """辅助宫位响应"""
    ming_gong: GongInfoResponse
    tai_yuan: GongInfoResponse
    shen_gong: GongInfoResponse


class APIError(BaseModel):
    """API错误响应"""
    code: str
    message: str
    detail: Optional[str] = None

