"""命宫及十二宫位计算"""
from .constants import DIZHI, TIANGAN, PALACE_NAMES, NAYIN_WUXING_JU, WUXING_JU_NUM


def get_hour_index(hour_zhi: str) -> int:
    """获取时辰地支索引（0-11）"""
    return DIZHI.index(hour_zhi)


def calculate_ming_gong_pos(lunar_month: int, hour_zhi: str) -> int:
    """计算命宫位置
    
    公式：命宫地支 = 寅 + (月 - 1) - (时 - 1) = 寅 + 月 - 时
    以寅为起点（索引2），顺时针排月，逆时针排时
    """
    hour_idx = get_hour_index(hour_zhi)
    # 寅位索引为2，月从1开始，时辰索引从0开始
    # 命宫位置 = (2 + 月 - 1 - 时辰索引 + 12) % 12
    ming_pos = (2 + lunar_month - 1 - hour_idx + 12) % 12
    return ming_pos


def calculate_shen_gong_pos(lunar_month: int, hour_zhi: str) -> int:
    """计算身宫位置
    
    公式：身宫地支 = 寅 + (月 - 1) + (时 - 1)
    以寅为起点，顺时针排月，顺时针排时
    """
    hour_idx = get_hour_index(hour_zhi)
    shen_pos = (2 + lunar_month - 1 + hour_idx) % 12
    return shen_pos


def get_wuxing_ju(year_gan: str, year_zhi: str) -> str:
    """获取五行局（根据年干支纳音）"""
    return NAYIN_WUXING_JU.get((year_gan, year_zhi), "土五局")


def get_palace_tiangan(year_gan: str, palace_pos: int) -> str:
    """获取宫位天干
    
    使用五虎遁：年干决定寅宫天干，其他宫位顺推
    甲己年起丙寅，乙庚年起戊寅，丙辛年起庚寅
    丁壬年起壬寅，戊癸年起甲寅
    """
    wuhudun = {"甲": "丙", "己": "丙", "乙": "戊", "庚": "戊",
               "丙": "庚", "辛": "庚", "丁": "壬", "壬": "壬",
               "戊": "甲", "癸": "甲"}
    yin_gan = wuhudun.get(year_gan, "丙")
    yin_idx = TIANGAN.index(yin_gan)
    # 寅位索引为2，palace_pos相对于寅的偏移
    offset = (palace_pos - 2 + 12) % 12
    return TIANGAN[(yin_idx + offset) % 10]


def arrange_palaces(
    lunar_month: int, hour_zhi: str, year_gan: str, year_zhi: str
) -> list[dict]:
    """排列十二宫位
    
    Returns:
        list of dict: 每个宫位的基本信息
    """
    ming_pos = calculate_ming_gong_pos(lunar_month, hour_zhi)
    
    palaces = []
    for i in range(12):
        # 宫位位置（从命宫开始顺时针）
        pos = (ming_pos + i) % 12
        dizhi = DIZHI[pos]
        tiangan = get_palace_tiangan(year_gan, pos)
        palace_name = PALACE_NAMES[i]
        
        palaces.append({
            "name": palace_name,
            "position": pos,
            "dizhi": dizhi,
            "tiangan": tiangan,
            "main_stars": [],
            "aux_stars": [],
            "sha_stars": [],
        })
    
    return palaces


def get_palace_by_pos(palaces: list[dict], pos: int) -> dict | None:
    """根据位置获取宫位"""
    for p in palaces:
        if p["position"] == pos:
            return p
    return None


def get_palace_by_name(palaces: list[dict], name: str) -> dict | None:
    """根据名称获取宫位"""
    for p in palaces:
        if p["name"] == name:
            return p
    return None

