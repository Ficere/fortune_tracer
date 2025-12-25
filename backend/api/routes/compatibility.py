"""配对分析API路由"""
from fastapi import APIRouter, HTTPException
from backend.api.schemas import CompatibilityRequest
from src.core import calculate_bazi, analyze_wuxing, calculate_compatibility
from src.models import CompatibilityResult
from src.models.bazi_models import Gender

router = APIRouter(prefix="/compatibility", tags=["配对分析"])


@router.post("/analyze", response_model=CompatibilityResult)
async def analyze_compatibility(request: CompatibilityRequest) -> CompatibilityResult:
    """
    配对分析
    
    分析两人八字的五行互补、干支关系和配对得分
    """
    try:
        p1, p2 = request.person1, request.person2
        gender1 = Gender.MALE if p1.gender == "男" else Gender.FEMALE
        gender2 = Gender.MALE if p2.gender == "男" else Gender.FEMALE
        
        # 计算双方八字
        bazi1 = calculate_bazi(p1.birth_datetime, gender1, p1.birth_place)
        bazi2 = calculate_bazi(p2.birth_datetime, gender2, p2.birth_place)
        
        # 五行分析
        wuxing1 = analyze_wuxing(bazi1)
        wuxing2 = analyze_wuxing(bazi2)
        
        # 配对分析
        result = calculate_compatibility(bazi1, bazi2, wuxing1, wuxing2)
        
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"配对分析失败: {str(e)}")

