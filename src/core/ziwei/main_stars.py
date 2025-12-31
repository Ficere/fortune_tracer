"""主星安星算法"""
from .constants import DIZHI, WUXING_JU_NUM


def calculate_ziwei_position(lunar_day: int, wuxing_ju: str) -> int:
    """计算紫微星位置
    
    根据农历日和五行局数确定紫微星所在宫位
    公式：紫微位置 = (局数 - 1 + 日) % 局数 的映射位置
    """
    ju_num = WUXING_JU_NUM.get(wuxing_ju, 5)
    
    # 紫微星位置对照表（简化版）
    # 实际计算较复杂，这里使用查表法的简化算法
    # 根据五行局和农历日计算紫微落宫
    
    # 计算商和余数
    quotient = (lunar_day - 1) // ju_num
    remainder = (lunar_day - 1) % ju_num
    
    # 基础位置从寅宫(2)开始
    if remainder == 0:
        base_pos = quotient
    else:
        # 奇数向前偶数向后的规则
        if quotient % 2 == 0:
            base_pos = quotient + remainder
        else:
            base_pos = quotient + ju_num - remainder
    
    # 映射到十二宫位置
    ziwei_pos = (2 + base_pos) % 12
    return ziwei_pos


def get_ziwei_series_positions(ziwei_pos: int) -> dict[str, int]:
    """获取紫微星系各星位置
    
    紫微星系：紫微、天机、太阳、武曲、天同、廉贞
    按固定间隔顺序排列
    """
    # 紫微星系固定间隔（相对紫微）
    offsets = {
        "紫微": 0,
        "天机": -1,    # 紫微逆一位
        "太阳": -3,    # 紫微逆三位
        "武曲": -4,    # 紫微逆四位
        "天同": -5,    # 紫微逆五位
        "廉贞": -8,    # 紫微逆八位（跳过空位）
    }
    
    positions = {}
    for star, offset in offsets.items():
        positions[star] = (ziwei_pos + offset + 12) % 12
    
    return positions


def get_tianfu_series_positions(ziwei_pos: int) -> dict[str, int]:
    """获取天府星系各星位置
    
    天府星系：天府、太阴、贪狼、巨门、天相、天梁、七杀、破军
    天府与紫微关于寅-申轴对称
    """
    # 天府位置：与紫微关于寅申轴对称
    # 寅位索引2，申位索引8
    # 对称公式：天府位置 = (2 + 8 - 紫微位置) % 12 = (10 - 紫微位置) % 12
    tianfu_pos = (10 - ziwei_pos + 12) % 12
    
    # 天府星系固定间隔（相对天府顺时针）
    offsets = {
        "天府": 0,
        "太阴": 1,     # 天府顺一位
        "贪狼": 2,     # 天府顺二位
        "巨门": 3,     # 天府顺三位
        "天相": 4,     # 天府顺四位
        "天梁": 5,     # 天府顺五位
        "七杀": 6,     # 天府顺六位
        "破军": 10,    # 天府顺十位（紫微对宫）
    }
    
    positions = {}
    for star, offset in offsets.items():
        positions[star] = (tianfu_pos + offset) % 12
    
    return positions


def arrange_main_stars(
    lunar_day: int, wuxing_ju: str, palaces: list[dict]
) -> list[dict]:
    """安置主星到宫位"""
    ziwei_pos = calculate_ziwei_position(lunar_day, wuxing_ju)
    
    # 获取紫微星系位置
    ziwei_series = get_ziwei_series_positions(ziwei_pos)
    
    # 获取天府星系位置
    tianfu_series = get_tianfu_series_positions(ziwei_pos)
    
    # 将主星安置到对应宫位
    all_stars = {**ziwei_series, **tianfu_series}
    
    for star_name, pos in all_stars.items():
        for palace in palaces:
            if palace["position"] == pos:
                palace["main_stars"].append({
                    "name": star_name,
                    "type": "主星",
                    "brightness": get_star_brightness(star_name, palace["dizhi"]),
                })
                break
    
    return palaces


def get_star_brightness(star_name: str, dizhi: str) -> str:
    """获取星曜亮度（庙旺得利陷）
    
    简化版：根据星曜和地支的关系判断亮度
    """
    # 简化的亮度规则（实际规则更复杂）
    bright_map = {
        "紫微": {"子": "庙", "午": "庙", "卯": "旺", "酉": "旺"},
        "天府": {"戌": "庙", "丑": "庙", "寅": "旺", "申": "旺"},
        "太阳": {"卯": "庙", "辰": "旺", "巳": "旺", "午": "旺"},
        "太阴": {"酉": "庙", "戌": "旺", "亥": "旺", "子": "旺"},
    }
    
    star_bright = bright_map.get(star_name, {})
    return star_bright.get(dizhi, "平")

