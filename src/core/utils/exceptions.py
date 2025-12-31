"""自定义异常类

提供结构化的错误处理
"""
from typing import Optional


class FortuneTracerError(Exception):
    """Fortune Tracer 基础异常类"""
    
    def __init__(
        self,
        message: str,
        code: str = "UNKNOWN_ERROR",
        details: Optional[dict] = None
    ):
        self.message = message
        self.code = code
        self.details = details or {}
        super().__init__(message)
    
    def to_dict(self) -> dict:
        return {
            "code": self.code,
            "message": self.message,
            "details": self.details
        }


class ValidationError(FortuneTracerError):
    """数据验证错误"""
    
    def __init__(self, message: str, field: Optional[str] = None):
        super().__init__(
            message=message,
            code="VALIDATION_ERROR",
            details={"field": field} if field else {}
        )


class BirthInfoError(ValidationError):
    """出生信息错误"""
    
    def __init__(self, message: str, field: Optional[str] = None):
        super().__init__(message=f"出生信息错误: {message}", field=field)


class DateTimeError(BirthInfoError):
    """日期时间错误"""
    
    def __init__(self, message: str):
        super().__init__(message=message, field="birth_datetime")


class GenderError(BirthInfoError):
    """性别参数错误"""
    
    def __init__(self, value: str):
        super().__init__(
            message=f"无效的性别值: {value}，应为'男'或'女'",
            field="gender"
        )


class LocationError(BirthInfoError):
    """地点信息错误"""
    
    def __init__(self, location: str):
        super().__init__(
            message=f"无法识别的地点: {location}",
            field="birth_place"
        )


class CalculationError(FortuneTracerError):
    """计算错误"""
    
    def __init__(self, message: str, calculation_type: str):
        super().__init__(
            message=message,
            code="CALCULATION_ERROR",
            details={"calculation_type": calculation_type}
        )


class PillarCalculationError(CalculationError):
    """四柱计算错误"""
    
    def __init__(self, message: str, pillar_type: str):
        super().__init__(
            message=f"{pillar_type}计算错误: {message}",
            calculation_type="pillar"
        )
        self.details["pillar_type"] = pillar_type


class WuxingCalculationError(CalculationError):
    """五行计算错误"""
    
    def __init__(self, message: str):
        super().__init__(
            message=f"五行分析错误: {message}",
            calculation_type="wuxing"
        )


class AIInterpretationError(FortuneTracerError):
    """AI 解读错误"""
    
    def __init__(self, message: str, original_error: Optional[str] = None):
        super().__init__(
            message=f"AI解读失败: {message}",
            code="AI_INTERPRETATION_ERROR",
            details={"original_error": original_error} if original_error else {}
        )


class APIKeyError(AIInterpretationError):
    """API Key 错误"""
    
    def __init__(self, message: str = "无效或缺失的API Key"):
        super().__init__(message=message)
        self.code = "API_KEY_ERROR"


class RateLimitError(AIInterpretationError):
    """请求频率限制错误"""
    
    def __init__(self, retry_after: Optional[int] = None):
        message = "请求过于频繁"
        if retry_after:
            message += f"，请在{retry_after}秒后重试"
        super().__init__(message=message)
        self.code = "RATE_LIMIT_ERROR"
        self.details["retry_after"] = retry_after


class ConfigurationError(FortuneTracerError):
    """配置错误"""
    
    def __init__(self, message: str, config_key: Optional[str] = None):
        super().__init__(
            message=f"配置错误: {message}",
            code="CONFIGURATION_ERROR",
            details={"config_key": config_key} if config_key else {}
        )
