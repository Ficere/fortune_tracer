"""八字分析结果JSON序列化器 - 生成适合大模型分析的结构化数据"""
from typing import Optional
from src.models import BaziChart, WuxingAnalysis, DaYunInfo
from src.models.bazi_models import YearFortune, BaziPillar
from src.core.constants import TIANGAN_WUXING, DIZHI_WUXING


def serialize_bazi_for_ai(
    bazi: BaziChart,
    wuxing: WuxingAnalysis,
    dayun: Optional[DaYunInfo] = None,
    fortunes: Optional[list[YearFortune]] = None,
    include_fortunes_count: int = 10
) -> dict:
    """将八字分析结果序列化为AI分析友好的JSON格式
    
    Args:
        bazi: 八字信息
        wuxing: 五行分析
        dayun: 大运信息（可选）
        fortunes: 流年运势列表（可选）
        include_fortunes_count: 包含的流年数量
    
    Returns:
        结构化的JSON字典
    """
    data = {
        "basic_info": _serialize_basic_info(bazi),
        "pillars": _serialize_pillars(bazi),
        "wuxing_analysis": _serialize_wuxing(wuxing),
    }
    
    if dayun:
        data["dayun"] = _serialize_dayun(dayun)
    
    if fortunes:
        data["year_fortunes"] = _serialize_fortunes(fortunes, include_fortunes_count)
    
    return data


def _serialize_basic_info(bazi: BaziChart) -> dict:
    """序列化基本信息"""
    return {
        "birth_datetime": bazi.birth_datetime.strftime("%Y-%m-%d %H:%M"),
        "gender": bazi.gender.value,
        "birth_place": bazi.birth_place or "未知",
    }


def _serialize_pillars(bazi: BaziChart) -> dict:
    """序列化四柱信息"""
    pillars = [bazi.year_pillar, bazi.month_pillar, bazi.day_pillar, bazi.hour_pillar]
    names = ["年柱", "月柱", "日柱", "时柱"]

    return {
        name: _serialize_pillar(p)
        for name, p in zip(names, pillars)
    }


def _serialize_pillar(p: BaziPillar) -> dict:
    """序列化单柱信息"""
    return {
        "ganzhi": p.display,
        "tiangan": p.tiangan.value,
        "dizhi": p.dizhi.value,
        "tiangan_wuxing": TIANGAN_WUXING.get(p.tiangan.value, ""),
        "dizhi_wuxing": DIZHI_WUXING.get(p.dizhi.value, ""),
    }


def _serialize_wuxing(wuxing: WuxingAnalysis) -> dict:
    """序列化五行分析"""
    counts = wuxing.counts.to_dict()
    total = sum(counts.values())
    
    return {
        "day_master": {
            "wuxing": wuxing.day_master.value,
            "strength": wuxing.day_master_strength,
        },
        "counts": counts,
        "percentages": {k: round(v / total * 100, 1) for k, v in counts.items()},
        "favorable": [w.value for w in wuxing.favorable],
        "unfavorable": [w.value for w in wuxing.unfavorable],
        "balance_analysis": _analyze_balance(counts),
    }


def _analyze_balance(counts: dict) -> str:
    """分析五行平衡状态"""
    max_wx = max(counts, key=counts.get)
    min_wx = min(counts, key=counts.get)
    
    if counts[max_wx] - counts[min_wx] <= 1:
        return "五行较为平衡"
    elif counts[max_wx] >= 3:
        return f"{max_wx}偏旺，{min_wx}偏弱"
    else:
        return f"{min_wx}稍弱"


def _serialize_dayun(dayun: DaYunInfo) -> dict:
    """序列化大运信息"""
    return {
        "direction": dayun.direction,
        "start_age": dayun.start_age,
        "dayun_list": [
            {
                "ganzhi": dy.ganzhi,
                "wuxing": dy.wuxing,
                "age_range": f"{dy.start_age}-{dy.end_age}岁",
                "year_range": f"{dy.start_year}-{dy.end_year}",
                "score": dy.detail.score if dy.detail else None,
                "level": dy.detail.level if dy.detail else None,
            }
            for dy in dayun.dayun_list
        ],
    }


def _serialize_fortunes(fortunes: list[YearFortune], count: int) -> list[dict]:
    """序列化流年运势"""
    return [
        {
            "year": f.year,
            "age": f.age,
            "ganzhi": f.ganzhi,
            "wuxing": f.wuxing,
            "score": f.score,
            "level": f.detail.level if f.detail else None,
            "suitable": f.detail.suitable if f.detail else [],
        }
        for f in fortunes[:count]
    ]


def serialize_for_prompt(data: dict) -> str:
    """将序列化数据格式化为提示词友好的文本"""
    import json
    return json.dumps(data, ensure_ascii=False, indent=2)

