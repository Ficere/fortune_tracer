"""纳音五行计算模块

纳音是根据干支组合确定的五行属性，共30种纳音。
每两个干支对应同一个纳音，形成60甲子纳音表。
"""
from src.models import BaziChart
from src.models.bazi_models import NaYinInfo
from .constants import TIANGAN, DIZHI


# 六十甲子纳音表
JIAZI_NAYIN = {
    "甲子": "海中金", "乙丑": "海中金",
    "丙寅": "炉中火", "丁卯": "炉中火",
    "戊辰": "大林木", "己巳": "大林木",
    "庚午": "路旁土", "辛未": "路旁土",
    "壬申": "剑锋金", "癸酉": "剑锋金",
    "甲戌": "山头火", "乙亥": "山头火",
    "丙子": "涧下水", "丁丑": "涧下水",
    "戊寅": "城头土", "己卯": "城头土",
    "庚辰": "白蜡金", "辛巳": "白蜡金",
    "壬午": "杨柳木", "癸未": "杨柳木",
    "甲申": "泉中水", "乙酉": "泉中水",
    "丙戌": "屋上土", "丁亥": "屋上土",
    "戊子": "霹雳火", "己丑": "霹雳火",
    "庚寅": "松柏木", "辛卯": "松柏木",
    "壬辰": "长流水", "癸巳": "长流水",
    "甲午": "沙中金", "乙未": "沙中金",
    "丙申": "山下火", "丁酉": "山下火",
    "戊戌": "平地木", "己亥": "平地木",
    "庚子": "壁上土", "辛丑": "壁上土",
    "壬寅": "金箔金", "癸卯": "金箔金",
    "甲辰": "覆灯火", "乙巳": "覆灯火",
    "丙午": "天河水", "丁未": "天河水",
    "戊申": "大驿土", "己酉": "大驿土",
    "庚戌": "钗钏金", "辛亥": "钗钏金",
    "壬子": "桑柘木", "癸丑": "桑柘木",
    "甲寅": "大溪水", "乙卯": "大溪水",
    "丙辰": "沙中土", "丁巳": "沙中土",
    "戊午": "天上火", "己未": "天上火",
    "庚申": "石榴木", "辛酉": "石榴木",
    "壬戌": "大海水", "癸亥": "大海水",
}

# 纳音五行提取
NAYIN_WUXING = {
    "金": ["海中金", "剑锋金", "白蜡金", "沙中金", "金箔金", "钗钏金"],
    "木": ["大林木", "杨柳木", "松柏木", "平地木", "桑柘木", "石榴木"],
    "水": ["涧下水", "泉中水", "长流水", "天河水", "大溪水", "大海水"],
    "火": ["炉中火", "山头火", "霹雳火", "山下火", "覆灯火", "天上火"],
    "土": ["路旁土", "城头土", "屋上土", "壁上土", "大驿土", "沙中土"],
}

# 纳音特性描述
NAYIN_DESC = {
    "海中金": "深藏不露，厚积薄发，大器晚成",
    "炉中火": "热情奔放，精力充沛，行动力强",
    "大林木": "气度宏大，胸怀宽广，成就可期",
    "路旁土": "务实稳重，脚踏实地，平凡中见真章",
    "剑锋金": "锋芒毕露，意志坚定，敢于挑战",
    "山头火": "志向高远，光明磊落，独立自主",
    "涧下水": "清澈纯净，柔中带刚，善于变通",
    "城头土": "坚固可靠，防守有道，保守稳健",
    "白蜡金": "温润如玉，内敛含蓄，品质高雅",
    "杨柳木": "柔韧性强，适应力佳，随遇而安",
    "泉中水": "源源不断，生机勃勃，潜力无限",
    "屋上土": "保护他人，责任心强，家庭观念重",
    "霹雳火": "爆发力强，突破困境，不鸣则已一鸣惊人",
    "松柏木": "坚韧不拔，经霜不凋，持久耐力",
    "长流水": "源远流长，持续发展，后劲十足",
    "沙中金": "隐藏实力，时机成熟方显光芒",
    "山下火": "温和有礼，照亮他人，乐于助人",
    "平地木": "平易近人，随和大方，人缘好",
    "壁上土": "支撑他人，默默付出，基础稳固",
    "金箔金": "华丽外表，善于包装，注重形象",
    "覆灯火": "照亮方向，指引他人，智慧之光",
    "天河水": "胸怀天下，格局宏大，不拘小节",
    "大驿土": "四通八达，交际广泛，信息灵通",
    "钗钏金": "精致细腻，善于装饰，审美能力强",
    "桑柘木": "实用主义，脚踏实地，注重实效",
    "大溪水": "奔流不息，勇往直前，活力充沛",
    "沙中土": "包容万物，吸收能力强，可塑性高",
    "天上火": "光芒四射，引人注目，富有魅力",
    "石榴木": "多子多福，繁衍能力强，生命力旺",
    "大海水": "包容一切，深不可测，胸怀宽广",
}


def get_nayin(ganzhi: str) -> str:
    """获取干支的纳音"""
    return JIAZI_NAYIN.get(ganzhi, "")


def get_nayin_wuxing(nayin: str) -> str:
    """获取纳音的五行属性"""
    for wuxing, nayins in NAYIN_WUXING.items():
        if nayin in nayins:
            return wuxing
    return ""


def calculate_nayin(bazi: BaziChart) -> list[NaYinInfo]:
    """
    计算八字四柱的纳音
    
    Args:
        bazi: 八字信息
    
    Returns:
        list[NaYinInfo]: 四柱纳音信息列表
    """
    pillars = [
        ("年柱", bazi.year_pillar),
        ("月柱", bazi.month_pillar),
        ("日柱", bazi.day_pillar),
        ("时柱", bazi.hour_pillar),
    ]
    
    nayin_list = []
    for name, pillar in pillars:
        ganzhi = pillar.display
        nayin = get_nayin(ganzhi)
        wuxing = get_nayin_wuxing(nayin)
        desc = NAYIN_DESC.get(nayin, "")
        
        info = NaYinInfo(
            pillar_name=name,
            ganzhi=ganzhi,
            nayin=nayin,
            wuxing=wuxing,
            description=desc
        )
        nayin_list.append(info)
    
    return nayin_list


def get_year_nayin(year: int) -> NaYinInfo:
    """获取指定年份的纳音（年命）"""
    # 计算年干支
    gan_idx = (year - 4) % 10
    zhi_idx = (year - 4) % 12
    ganzhi = f"{TIANGAN[gan_idx]}{DIZHI[zhi_idx]}"
    
    nayin = get_nayin(ganzhi)
    wuxing = get_nayin_wuxing(nayin)
    desc = NAYIN_DESC.get(nayin, "")
    
    return NaYinInfo(
        pillar_name="年命",
        ganzhi=ganzhi,
        nayin=nayin,
        wuxing=wuxing,
        description=desc
    )
