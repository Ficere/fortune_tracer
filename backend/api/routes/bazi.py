"""八字分析API路由"""
from fastapi import APIRouter, HTTPException
from backend.api.schemas import BaziAnalyzeRequest
from src.core import calculate_bazi, analyze_wuxing
from src.ai.interpreter import interpret_bazi, calculate_year_fortunes
from src.models import FortuneReport
from src.models.bazi_models import Gender

router = APIRouter(prefix="/bazi", tags=["八字分析"])


@router.post("/analyze", response_model=FortuneReport)
async def analyze_bazi(request: BaziAnalyzeRequest) -> FortuneReport:
    """
    个人八字分析
    
    根据出生时间计算八字、五行分析、AI解读和流年运势
    """
    try:
        birth_info = request.birth_info
        gender_enum = Gender.MALE if birth_info.gender == "男" else Gender.FEMALE
        
        # 计算八字
        bazi = calculate_bazi(
            birth_info.birth_datetime,
            gender_enum,
            birth_info.birth_place
        )
        
        # 五行分析
        wuxing = analyze_wuxing(bazi)
        
        # 流年运势
        fortunes = calculate_year_fortunes(bazi, wuxing, years=10)
        
        # AI解读
        interpretation = interpret_bazi(bazi, wuxing, request.api_key)
        
        return FortuneReport(
            bazi=bazi,
            wuxing=wuxing,
            interpretation=interpretation,
            year_fortunes=fortunes
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"分析失败: {str(e)}")

