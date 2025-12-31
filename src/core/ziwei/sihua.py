"""四化飞星计算"""
from .constants import SIHUA_TABLE


def get_sihua(year_gan: str) -> dict[str, str]:
    """获取四化星（根据年干）
    
    返回：化禄、化权、化科、化忌对应的星曜
    """
    return SIHUA_TABLE.get(year_gan, {
        "禄": "贪狼", "权": "太阴", "科": "右弼", "忌": "天机"
    })


def apply_sihua_to_palaces(
    year_gan: str, palaces: list[dict]
) -> tuple[list[dict], dict[str, str]]:
    """将四化应用到宫位中的星曜
    
    Args:
        year_gan: 年干
        palaces: 宫位列表
    
    Returns:
        更新后的宫位列表和四化星字典
    """
    sihua = get_sihua(year_gan)
    sihua_result = {}
    
    # 四化类型映射
    hua_types = {
        "禄": "化禄",
        "权": "化权",
        "科": "化科",
        "忌": "化忌",
    }
    
    for hua_key, hua_name in hua_types.items():
        star_name = sihua.get(hua_key, "")
        if not star_name:
            continue
        
        # 在宫位中查找该星曜并标记四化
        for palace in palaces:
            # 检查主星
            for star in palace["main_stars"]:
                if star["name"] == star_name:
                    star["sihua"] = hua_name
                    sihua_result[hua_name] = f"{star_name}({palace['name']})"
                    break
            
            # 检查辅星（文昌文曲可能化科或化忌）
            for star in palace["aux_stars"]:
                if star["name"] == star_name:
                    star["sihua"] = hua_name
                    sihua_result[hua_name] = f"{star_name}({palace['name']})"
                    break
    
    return palaces, sihua_result


def get_sihua_description(sihua_result: dict[str, str]) -> str:
    """生成四化描述文字"""
    descriptions = []
    
    hua_meanings = {
        "化禄": "主财禄、顺利、机遇",
        "化权": "主权力、掌控、开创",
        "化科": "主名声、学业、贵人",
        "化忌": "主阻碍、烦恼、执念",
    }
    
    for hua_name, star_palace in sihua_result.items():
        meaning = hua_meanings.get(hua_name, "")
        descriptions.append(f"{star_palace}{hua_name}：{meaning}")
    
    return "；".join(descriptions)


def analyze_sihua_pattern(sihua_result: dict[str, str], palaces: list[dict]) -> str:
    """分析四化格局"""
    analysis = []
    
    # 检查化禄在命宫
    if "化禄" in sihua_result:
        lu_info = sihua_result["化禄"]
        if "命宫" in lu_info:
            analysis.append("化禄入命，一生财禄丰厚，事业顺利")
        if "财帛宫" in lu_info:
            analysis.append("化禄入财帛，财源广进，理财有方")
        if "官禄宫" in lu_info:
            analysis.append("化禄入官禄，事业运势极佳，晋升有望")
    
    # 检查化忌
    if "化忌" in sihua_result:
        ji_info = sihua_result["化忌"]
        if "命宫" in ji_info:
            analysis.append("化忌入命，需注意身体健康和人际关系")
        if "夫妻宫" in ji_info:
            analysis.append("化忌入夫妻，感情需多经营，注意沟通")
        if "疾厄宫" in ji_info:
            analysis.append("化忌入疾厄，需注意身体保养")
    
    # 检查化权
    if "化权" in sihua_result:
        quan_info = sihua_result["化权"]
        if "官禄宫" in quan_info:
            analysis.append("化权入官禄，掌权有方，领导能力强")
        if "命宫" in quan_info:
            analysis.append("化权入命，性格刚强，有开创精神")
    
    # 检查化科
    if "化科" in sihua_result:
        ke_info = sihua_result["化科"]
        if "命宫" in ke_info or "官禄宫" in ke_info:
            analysis.append("化科入命/官禄，有贵人相助，声名远播")
    
    if not analysis:
        analysis.append("四化分布均衡，人生起伏较平稳")
    
    return "。".join(analysis)

