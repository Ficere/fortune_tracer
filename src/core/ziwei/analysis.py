"""紫微斗数解读分析"""
from src.models.ziwei_models import ZiweiChart, ZiweiAnalysis, PalaceSummary


def analyze_personality(chart: ZiweiChart) -> str:
    """分析性格特点（根据命宫星曜）"""
    ming_palace = next((p for p in chart.palaces if p.palace.value == "命宫"), None)
    if not ming_palace:
        return "命宫信息不足"
    
    traits = []
    for star in ming_palace.main_stars:
        if star.name == "紫微":
            traits.append("有领导气质，自尊心强，喜欢掌控局面")
        elif star.name == "天机":
            traits.append("聪明灵活，善于思考，适应力强")
        elif star.name == "太阳":
            traits.append("热情开朗，乐于助人，有正义感")
        elif star.name == "武曲":
            traits.append("刚毅果断，重视实际，有财运天赋")
        elif star.name == "天同":
            traits.append("温和善良，知足常乐，福气深厚")
        elif star.name == "廉贞":
            traits.append("聪明干练，爱恨分明，有艺术天赋")
        elif star.name == "天府":
            traits.append("稳重大方，保守务实，适合守成")
        elif star.name == "太阴":
            traits.append("细腻温柔，内敛含蓄，重视感情")
        elif star.name == "贪狼":
            traits.append("多才多艺，欲望强烈，善于交际")
        elif star.name == "巨门":
            traits.append("口才好，分析力强，但易招是非")
        elif star.name == "天相":
            traits.append("谨慎稳重，善于协调，有贵人缘")
        elif star.name == "天梁":
            traits.append("正直善良，乐于助人，适合公职")
        elif star.name == "七杀":
            traits.append("刚强果断，有魄力，适合开创")
        elif star.name == "破军":
            traits.append("变动性强，敢于冒险，不守旧规")
    
    if not traits:
        traits.append("性格温和，随遇而安")
    
    return "；".join(traits)


def analyze_career(chart: ZiweiChart) -> str:
    """分析事业运势（根据官禄宫）"""
    guan_palace = next((p for p in chart.palaces if p.palace.value == "官禄宫"), None)
    if not guan_palace:
        return "官禄宫信息不足"
    
    analysis = []
    star_names = [s.name for s in guan_palace.main_stars]
    
    if "紫微" in star_names or "天府" in star_names:
        analysis.append("事业运势佳，适合从政或管理")
    if "太阳" in star_names:
        analysis.append("适合公众事业，有名声运")
    if "武曲" in star_names:
        analysis.append("适合金融财务，理财能力强")
    if "贪狼" in star_names:
        analysis.append("适合艺术娱乐或销售行业")
    if "七杀" in star_names or "破军" in star_names:
        analysis.append("适合开创型事业，军警法律")
    
    aux_names = [s.name for s in guan_palace.aux_stars]
    if "文昌" in aux_names or "文曲" in aux_names:
        analysis.append("有文职才华，适合文教工作")
    if "左辅" in aux_names or "右弼" in aux_names:
        analysis.append("有贵人相助，事业发展顺利")
    
    sha_names = [s.name for s in guan_palace.sha_stars]
    if sha_names:
        analysis.append("事业中需注意竞争压力和小人")
    
    return "；".join(analysis) if analysis else "事业运势平稳，宜稳扎稳打"


def analyze_wealth(chart: ZiweiChart) -> str:
    """分析财运（根据财帛宫）"""
    cai_palace = next((p for p in chart.palaces if p.palace.value == "财帛宫"), None)
    if not cai_palace:
        return "财帛宫信息不足"
    
    analysis = []
    star_names = [s.name for s in cai_palace.main_stars]
    
    if "武曲" in star_names:
        analysis.append("正财运极佳，善于理财投资")
    if "天府" in star_names:
        analysis.append("财库充盈，守财能力强")
    if "太阴" in star_names:
        analysis.append("财运稳定，宜从事稳定行业")
    if "贪狼" in star_names:
        analysis.append("偏财运好，但花钱也快")
    if "破军" in star_names:
        analysis.append("财运起伏大，宜控制开支")
    
    if "禄存" in [s.name for s in cai_palace.aux_stars]:
        analysis.append("有禄存入财帛，财源不断")
    
    return "；".join(analysis) if analysis else "财运中等，宜开源节流"


def analyze_love(chart: ZiweiChart) -> str:
    """分析感情运势（根据夫妻宫）"""
    fuqi_palace = next((p for p in chart.palaces if p.palace.value == "夫妻宫"), None)
    if not fuqi_palace:
        return "夫妻宫信息不足"
    
    analysis = []
    star_names = [s.name for s in fuqi_palace.main_stars]
    
    if "太阳" in star_names or "太阴" in star_names:
        analysis.append("感情稳定，配偶条件较好")
    if "天同" in star_names:
        analysis.append("婚姻和谐，家庭幸福")
    if "贪狼" in star_names:
        analysis.append("桃花运旺，但需注意专一")
    if "巨门" in star_names:
        analysis.append("感情中易有口舌，需多沟通")
    if "七杀" in star_names or "破军" in star_names:
        analysis.append("感情波折较多，宜晚婚")
    
    return "；".join(analysis) if analysis else "感情平顺，缘分自然"


def generate_ziwei_analysis(chart: ZiweiChart) -> ZiweiAnalysis:
    """生成完整的紫微分析结果"""
    personality = analyze_personality(chart)
    career = analyze_career(chart)
    wealth = analyze_wealth(chart)
    love = analyze_love(chart)
    health = _analyze_health(chart)
    summary = _generate_summary(chart)
    
    return ZiweiAnalysis(
        chart=chart,
        personality=personality,
        career=career,
        wealth=wealth,
        love=love,
        health=health,
        summary=summary,
    )


def _analyze_health(chart: ZiweiChart) -> str:
    """分析健康运势"""
    ji_palace = next((p for p in chart.palaces if p.palace.value == "疾厄宫"), None)
    if not ji_palace:
        return "疾厄宫信息不足"
    
    if ji_palace.sha_stars:
        return "需注意身体保养，定期体检"
    return "身体底子较好，保持规律作息"


def _generate_summary(chart: ZiweiChart) -> str:
    """生成综合评价"""
    ming_palace = next((p for p in chart.palaces if p.palace.value == "命宫"), None)
    stars = [s.name for s in ming_palace.main_stars] if ming_palace else []
    
    if "紫微" in stars or "天府" in stars:
        return "命格高贵，一生多有贵人相助，适合从事管理或领导工作"
    if "太阳" in stars:
        return "光明磊落，热心助人，社会地位可期"
    if "武曲" in stars:
        return "财运亨通，适合经商或金融行业"
    return "命格中正，一生平稳，宜脚踏实地"

