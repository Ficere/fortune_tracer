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


class APIError(BaseModel):
    """API错误响应"""
    code: str
    message: str
    detail: Optional[str] = None

