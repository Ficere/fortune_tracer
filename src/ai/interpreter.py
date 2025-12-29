"""AI命理解读模块 - 基于JSON中间数据的AI分析工具链"""
import json
from typing import Optional
from openai import OpenAI
from src.models import BaziChart, WuxingAnalysis, AIInterpretation, DaYunInfo
from src.models.bazi_models import YearFortune
from .config import AIConfig, get_ai_config
from .serializer import serialize_bazi_for_ai, serialize_for_prompt
from .prompts import SYSTEM_PROMPT, build_analysis_prompt


def interpret_bazi(
    bazi: BaziChart,
    wuxing: WuxingAnalysis,
    api_key: Optional[str] = None,
    dayun: Optional[DaYunInfo] = None,
    config: Optional[AIConfig] = None
) -> AIInterpretation:
    """使用AI解读八字

    Args:
        bazi: 八字信息
        wuxing: 五行分析
        api_key: API Key（优先于config中的设置）
        dayun: 大运信息（可选，用于更全面的分析）
        config: AI配置（可选，默认使用全局配置）

    Returns:
        AI解读结果
    """
    # 获取配置
    cfg = config or get_ai_config()
    if api_key:
        cfg = cfg.with_api_key(api_key)

    if not cfg.is_valid():
        return _get_default_interpretation(bazi, wuxing)

    # 序列化数据为JSON
    bazi_data = serialize_bazi_for_ai(bazi, wuxing, dayun)
    bazi_json = serialize_for_prompt(bazi_data)

    # 调用AI分析
    return _call_ai_analysis(bazi_json, cfg, bazi, wuxing)


def _call_ai_analysis(
    bazi_json: str, cfg: AIConfig, bazi: BaziChart, wuxing: WuxingAnalysis
) -> AIInterpretation:
    """调用AI进行分析"""
    try:
        client_kwargs = {"api_key": cfg.api_key, "timeout": cfg.timeout}
        if cfg.base_url:
            client_kwargs["base_url"] = cfg.base_url

        client = OpenAI(**client_kwargs)

        request_kwargs = {
            "model": cfg.model,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": build_analysis_prompt(bazi_json)}
            ],
            "temperature": cfg.temperature,
            "max_tokens": cfg.max_tokens,
        }
        if cfg.use_json_mode:
            request_kwargs["response_format"] = {"type": "json_object"}

        response = client.chat.completions.create(**request_kwargs)
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


def _calculate_year_score(
    year: int, age: int, year_wx: str, year_zhi: str,
    bazi: BaziChart, wuxing: WuxingAnalysis
) -> float:
    """基于命理规则计算流年分数

    计算因素：
    1. 喜用神加分（+15-20），忌神减分（-10-15）
    2. 干支冲合关系（六合+8，六冲-12，刑-8）
    3. 五行生克关系（被生+5，被克-8）
    4. 年龄阶段微调（青年中年运势基数略高）
    """
    from src.core.constants import DIZHI_LIUHE, DIZHI_LIUCHONG, DIZHI_XING

    # 基础分60分（对应"平"级别）
    score = 60.0

    # 1. 喜忌判断（核心因素）
    favorable_wx = [w.value for w in wuxing.favorable]
    unfavorable_wx = [w.value for w in wuxing.unfavorable]

    if year_wx in favorable_wx:
        score += 18  # 喜神年大幅加分
    elif year_wx in unfavorable_wx:
        score -= 12  # 忌神年减分

    # 2. 地支关系分析
    bazi_zhis = [
        bazi.year_pillar.dizhi.value,
        bazi.month_pillar.dizhi.value,
        bazi.day_pillar.dizhi.value,
        bazi.hour_pillar.dizhi.value,
    ]

    for zhi in bazi_zhis:
        pair = tuple(sorted([year_zhi, zhi]))
        if pair in DIZHI_LIUHE or (pair[1], pair[0]) in DIZHI_LIUHE:
            score += 6  # 六合加分
        if pair in DIZHI_LIUCHONG or (pair[1], pair[0]) in DIZHI_LIUCHONG:
            score -= 10  # 六冲减分（冲日支影响更大）
            if zhi == bazi.day_pillar.dizhi.value:
                score -= 5  # 冲日支额外减分
        if pair in DIZHI_XING or (pair[1], pair[0]) in DIZHI_XING:
            score -= 6  # 刑减分

    # 3. 年龄阶段微调
    if 25 <= age <= 50:
        score += 3  # 壮年期基数略高
    elif age < 10 or age > 75:
        score -= 2  # 幼年老年微调

    # 4. 确保分数在合理范围且与评级匹配
    # 30-95分，避免极端值过多
    return round(min(max(score, 32), 93), 1)


def calculate_year_fortunes(
    bazi: BaziChart,
    wuxing: WuxingAnalysis,
    years: int = 91,
    with_detail: bool = True
) -> list[YearFortune]:
    """计算流年运势（从出生到指定年数）"""
    from src.core.constants import TIANGAN, DIZHI, TIANGAN_WUXING
    from src.core.fortune_interpreter import generate_year_detail
    from src.models.bazi_models import YearFortuneDetail

    birth_year = bazi.birth_datetime.year
    fortunes = []

    for age in range(years):
        year = birth_year + age
        gan_idx = (year - 4) % 10
        zhi_idx = (year - 4) % 12
        year_gan = TIANGAN[gan_idx]
        year_zhi = DIZHI[zhi_idx]
        ganzhi = f"{year_gan}{year_zhi}"
        year_wx = TIANGAN_WUXING[year_gan]

        # 基于命理规则计算分数
        score = _calculate_year_score(
            year, age, year_wx, year_zhi, bazi, wuxing
        )

        detail = None
        if with_detail:
            detail_data = generate_year_detail(year, age, score, bazi, wuxing)
            detail = YearFortuneDetail(
                level=detail_data["level"],
                emoji=detail_data["emoji"],
                wuxing_effect=detail_data["wuxing_effect"],
                ganzhi_relations=detail_data["ganzhi_relations"],
                career=detail_data["career"],
                love=detail_data["love"],
                health=detail_data["health"],
                wealth=detail_data["wealth"],
                suitable=detail_data["suitable"],
                unsuitable=detail_data["unsuitable"],
                score_factors=detail_data.get("score_factors", []),
                is_favorable_year=detail_data.get("is_favorable_year", False),
                wuxing_relation=detail_data.get("wuxing_relation", ""),
            )

        fortunes.append(YearFortune(
            year=year,
            score=score,
            description=f"{age}岁 {ganzhi}年",
            age=age,
            ganzhi=ganzhi,
            wuxing=year_wx,
            detail=detail
        ))

    return fortunes

