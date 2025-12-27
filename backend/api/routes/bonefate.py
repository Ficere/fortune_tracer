"""称骨算命API路由"""

from datetime import datetime
from fastapi import APIRouter, HTTPException
from src.core import analyze_bonefate
from src.models import BoneFateRequest, BoneFateResult

router = APIRouter(prefix="/bonefate", tags=["称骨算命"])


@router.post("/analyze", response_model=BoneFateResult)
async def analyze(request: BoneFateRequest) -> BoneFateResult:
    """
    称骨算命分析
    
    根据出生时间计算骨重并返回命运诗词
    
    - **year**: 年份 (1900-2100)
    - **month**: 月份 (1-12)
    - **day**: 日期 (1-31)
    - **hour**: 小时，24小时制 (0-23)
    - **is_lunar**: 是否为农历日期，默认为阳历
    """
    try:
        birth_dt = datetime(
            request.year, request.month, request.day, request.hour
        )
        result_dict = analyze_bonefate(birth_dt, request.is_lunar)
        return BoneFateResult.from_dict(result_dict)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"日期无效: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"分析失败: {str(e)}")


@router.get("/weight/{year}/{month}/{day}/{hour}")
async def get_weight(
    year: int, month: int, day: int, hour: int, is_lunar: bool = False
) -> dict:
    """
    快速获取骨重
    
    通过URL路径参数快速计算骨重
    """
    try:
        from src.core import calculate_bone_weight
        weight = calculate_bone_weight(year, month, day, hour, is_lunar)
        return {
            "weight": weight,
            "weight_display": f"{weight:.1f}两",
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"日期无效: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"计算失败: {str(e)}")
