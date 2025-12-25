"""择日分析API路由"""
from fastapi import APIRouter, HTTPException
from backend.api.schemas import DateSelectionRequest
from src.core import calculate_bazi, analyze_wuxing, select_dates
from src.models import EventType, DateRecommendation
from src.models.bazi_models import Gender

router = APIRouter(prefix="/date-selection", tags=["择日分析"])

EVENT_MAP = {
    "结婚": EventType.WEDDING,
    "开业": EventType.BUSINESS,
    "搬家": EventType.MOVING,
    "出行": EventType.TRAVEL,
    "签约": EventType.SIGNING,
}


@router.post("/analyze", response_model=DateRecommendation)
async def analyze_date_selection(request: DateSelectionRequest) -> DateRecommendation:
    """
    择日分析
    
    根据八字和事件类型推荐吉日
    """
    try:
        birth_info = request.birth_info
        gender_enum = Gender.MALE if birth_info.gender == "男" else Gender.FEMALE
        
        # 验证事件类型
        event = EVENT_MAP.get(request.event_type)
        if not event:
            raise ValueError(f"不支持的事件类型: {request.event_type}")
        
        # 计算八字
        bazi = calculate_bazi(
            birth_info.birth_datetime,
            gender_enum,
            birth_info.birth_place
        )
        wuxing = analyze_wuxing(bazi)
        
        # 择日
        result = select_dates(bazi, wuxing, event, request.start_date, request.search_days)
        
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"择日分析失败: {str(e)}")

