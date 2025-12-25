"""AI命理解读模块"""
import os
from openai import OpenAI
from src.models import BaziChart, WuxingAnalysis, AIInterpretation
from src.models.bazi_models import YearFortune


def _build_prompt(bazi: BaziChart, wuxing: WuxingAnalysis) -> str:
    """构建AI解读提示词"""
    return f"""你是一位资深的命理学专家，请根据以下八字信息进行详细解读。

## 八字信息
- 年柱：{bazi.year_pillar.display}
- 月柱：{bazi.month_pillar.display}
- 日柱：{bazi.day_pillar.display}
- 时柱：{bazi.hour_pillar.display}
- 性别：{bazi.gender.value}
- 出生时间：{bazi.birth_datetime.strftime('%Y年%m月%d日 %H时')}

## 五行分析
- 日主：{wuxing.day_master.value}（{wuxing.day_master_strength}）
- 五行分布：木{wuxing.counts.mu} 火{wuxing.counts.huo} 土{wuxing.counts.tu} 金{wuxing.counts.jin} 水{wuxing.counts.shui}
- 喜用神：{', '.join(w.value for w in wuxing.favorable)}
- 忌神：{', '.join(w.value for w in wuxing.unfavorable)}

请提供以下维度的解读，每个维度100-200字：
1. 性格特点
2. 事业运势
3. 感情运势
4. 健康建议
5. 财运分析
6. 综合评价

请以JSON格式返回，格式如下：
{{
    "personality": "性格分析...",
    "career": "事业分析...",
    "love": "感情分析...",
    "health": "健康建议...",
    "wealth": "财运分析...",
    "summary": "综合评价..."
}}"""


def interpret_bazi(
    bazi: BaziChart,
    wuxing: WuxingAnalysis,
    api_key: str | None = None
) -> AIInterpretation:
    """使用AI解读八字"""
    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        return _get_default_interpretation(bazi, wuxing)
    
    try:
        client = OpenAI(api_key=key)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "你是命理学专家，请用JSON格式回复。"},
                {"role": "user", "content": _build_prompt(bazi, wuxing)}
            ],
            response_format={"type": "json_object"},
            temperature=0.7
        )
        
        import json
        result = json.loads(response.choices[0].message.content)
        return AIInterpretation(**result)
    except Exception:
        return _get_default_interpretation(bazi, wuxing)


def _get_default_interpretation(bazi: BaziChart, wuxing: WuxingAnalysis) -> AIInterpretation:
    """默认解读（无API时使用）"""
    dm = wuxing.day_master.value
    strength = wuxing.day_master_strength
    
    personality_map = {
        "木": "性格正直，有进取心，富有创造力",
        "火": "热情开朗，积极向上，具有领导力",
        "土": "稳重踏实，诚信可靠，重视家庭",
        "金": "意志坚定，果断干练，重义气",
        "水": "聪明机智，灵活变通，善于交际"
    }
    
    return AIInterpretation(
        personality=f"日主为{dm}，{strength}。{personality_map.get(dm, '')}",
        career=f"以{wuxing.favorable[0].value}相关行业为佳，事业发展稳健",
        love=f"感情方面需注意与{wuxing.unfavorable[0].value}属性之人的相处",
        health=f"注意{wuxing.counts.to_dict()}中较弱五行对应的身体部位",
        wealth="财运平稳，适当投资可获收益",
        summary=f"命局{strength}，整体运势{['需努力', '较为平衡', '较为顺利'][['身弱', '中和', '身旺'].index(strength)]}"
    )


def calculate_year_fortunes(
    bazi: BaziChart,
    wuxing: WuxingAnalysis,
    years: int = 10
) -> list[YearFortune]:
    """计算流年运势"""
    from datetime import datetime
    from src.core.constants import TIANGAN, DIZHI, TIANGAN_WUXING
    
    current_year = datetime.now().year
    fortunes = []
    
    for i in range(years):
        year = current_year + i
        gan_idx = (year - 4) % 10
        zhi_idx = (year - 4) % 12
        year_wx = TIANGAN_WUXING[TIANGAN[gan_idx]]
        
        # 基于喜忌计算分数
        favorable_wx = [w.value for w in wuxing.favorable]
        score = 70 if year_wx in favorable_wx else 50
        score += (hash(f"{year}{bazi.day_pillar.display}") % 20)
        score = min(max(score, 30), 95)
        
        fortunes.append(YearFortune(
            year=year,
            score=score,
            description=f"{TIANGAN[gan_idx]}{DIZHI[zhi_idx]}年"
        ))
    
    return fortunes

