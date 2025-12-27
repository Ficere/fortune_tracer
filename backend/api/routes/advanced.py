"""高级分析API路由 - 大运、十神、神煞、纳音"""
from fastapi import APIRouter, HTTPException
from backend.api.schemas import (
    DayunRequest, ShiShenRequest, ShenShaRequest,
    NaYinRequest, YearNaYinRequest
)
from src.core import (
    calculate_bazi, calculate_dayun, analyze_shishen,
    calculate_shensha, calculate_nayin, get_year_nayin,
    convert_to_true_solar_time
)
from src.models import Gender
from src.models.bazi_models import (
    DaYunInfo, ShiShenAnalysis, ShenShaAnalysis, NaYinInfo
)

router = APIRouter(prefix="/advanced", tags=["高级分析"])


@router.post("/dayun", response_model=DaYunInfo)
async def get_dayun(request: DayunRequest) -> DaYunInfo:
    """
    计算大运
    
    根据出生信息计算大运排盘，包括起运年龄和运势周期
    """
    try:
        birth_info = request.birth_info
        gender = Gender.MALE if birth_info.gender == "男" else Gender.FEMALE
        
        # 真太阳时转换
        birth_dt = birth_info.birth_datetime
        if birth_info.birth_place:
            birth_dt = convert_to_true_solar_time(birth_dt, birth_info.birth_place)
        
        bazi = calculate_bazi(birth_dt, gender, birth_info.birth_place)
        dayun_info = calculate_dayun(bazi, request.num_dayun)
        
        return dayun_info
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"大运计算失败: {str(e)}")


@router.post("/shishen", response_model=ShiShenAnalysis)
async def get_shishen(request: ShiShenRequest) -> ShiShenAnalysis:
    """
    分析十神
    
    分析八字中的十神关系和格局
    """
    try:
        birth_info = request.birth_info
        gender = Gender.MALE if birth_info.gender == "男" else Gender.FEMALE
        
        birth_dt = birth_info.birth_datetime
        if birth_info.birth_place:
            birth_dt = convert_to_true_solar_time(birth_dt, birth_info.birth_place)
        
        bazi = calculate_bazi(birth_dt, gender, birth_info.birth_place)
        shishen = analyze_shishen(bazi)
        
        return shishen
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"十神分析失败: {str(e)}")


@router.post("/shensha", response_model=ShenShaAnalysis)
async def get_shensha(request: ShenShaRequest) -> ShenShaAnalysis:
    """
    计算神煞
    
    分析八字中的吉神和凶煞
    """
    try:
        birth_info = request.birth_info
        gender = Gender.MALE if birth_info.gender == "男" else Gender.FEMALE
        
        birth_dt = birth_info.birth_datetime
        if birth_info.birth_place:
            birth_dt = convert_to_true_solar_time(birth_dt, birth_info.birth_place)
        
        bazi = calculate_bazi(birth_dt, gender, birth_info.birth_place)
        shensha = calculate_shensha(bazi)
        
        return shensha
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"神煞计算失败: {str(e)}")


@router.post("/nayin", response_model=list[NaYinInfo])
async def get_nayin(request: NaYinRequest) -> list[NaYinInfo]:
    """
    计算纳音
    
    计算八字四柱的纳音五行
    """
    try:
        birth_info = request.birth_info
        gender = Gender.MALE if birth_info.gender == "男" else Gender.FEMALE
        
        birth_dt = birth_info.birth_datetime
        if birth_info.birth_place:
            birth_dt = convert_to_true_solar_time(birth_dt, birth_info.birth_place)
        
        bazi = calculate_bazi(birth_dt, gender, birth_info.birth_place)
        nayin_list = calculate_nayin(bazi)
        
        return nayin_list
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"纳音计算失败: {str(e)}")


@router.post("/year-nayin", response_model=NaYinInfo)
async def get_year_nayin_api(request: YearNaYinRequest) -> NaYinInfo:
    """
    获取年命纳音
    
    根据年份获取年命纳音
    """
    try:
        nayin_info = get_year_nayin(request.year)
        return nayin_info
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"年命纳音获取失败: {str(e)}")
