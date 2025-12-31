"""辅星和煞星安星算法"""
from .constants import DIZHI, TIANGAN


def get_zuofu_youbi_pos(lunar_month: int) -> tuple[int, int]:
    """计算左辅右弼位置
    
    左辅：从辰宫起正月，顺时针数到生月
    右弼：从戌宫起正月，逆时针数到生月
    """
    # 辰=4, 戌=10
    zuofu_pos = (4 + lunar_month - 1) % 12
    youbi_pos = (10 - lunar_month + 1 + 12) % 12
    return zuofu_pos, youbi_pos


def get_wenchang_wenqu_pos(hour_zhi: str) -> tuple[int, int]:
    """计算文昌文曲位置
    
    文昌：从戌宫起子时，逆时针数到生时
    文曲：从辰宫起子时，顺时针数到生时
    """
    hour_idx = DIZHI.index(hour_zhi)
    # 戌=10, 逆时针
    wenchang_pos = (10 - hour_idx + 12) % 12
    # 辰=4, 顺时针
    wenqu_pos = (4 + hour_idx) % 12
    return wenchang_pos, wenqu_pos


def get_tiankui_tianyue_pos(year_gan: str) -> tuple[int, int]:
    """计算天魁天钺位置（根据年干）"""
    tiankui_map = {
        "甲": "丑", "戊": "丑", "庚": "丑",
        "乙": "子", "己": "子",
        "丙": "亥", "丁": "亥",
        "壬": "卯", "癸": "卯",
        "辛": "午",
    }
    tianyue_map = {
        "甲": "未", "戊": "未", "庚": "未",
        "乙": "申", "己": "申",
        "丙": "酉", "丁": "酉",
        "壬": "巳", "癸": "巳",
        "辛": "寅",
    }
    kui_zhi = tiankui_map.get(year_gan, "丑")
    yue_zhi = tianyue_map.get(year_gan, "未")
    return DIZHI.index(kui_zhi), DIZHI.index(yue_zhi)


def get_lucun_pos(year_gan: str) -> int:
    """计算禄存位置（根据年干）"""
    lucun_map = {
        "甲": "寅", "乙": "卯", "丙": "巳", "丁": "午",
        "戊": "巳", "己": "午", "庚": "申", "辛": "酉",
        "壬": "亥", "癸": "子",
    }
    return DIZHI.index(lucun_map.get(year_gan, "寅"))


def get_qingyang_tuoluo_pos(year_gan: str) -> tuple[int, int]:
    """计算擎羊陀罗位置
    
    擎羊：禄存顺一位
    陀罗：禄存逆一位
    """
    lucun_pos = get_lucun_pos(year_gan)
    qingyang_pos = (lucun_pos + 1) % 12
    tuoluo_pos = (lucun_pos - 1 + 12) % 12
    return qingyang_pos, tuoluo_pos


def get_huoxing_lingxing_pos(year_zhi: str, hour_zhi: str) -> tuple[int, int]:
    """计算火星铃星位置
    
    根据年支和时支确定（简化规则）
    """
    # 简化：按年支分组
    yin_wu_xu = ["寅", "午", "戌"]
    shen_zi_chen = ["申", "子", "辰"]
    si_you_chou = ["巳", "酉", "丑"]
    hai_mao_wei = ["亥", "卯", "未"]
    
    hour_idx = DIZHI.index(hour_zhi)
    
    if year_zhi in yin_wu_xu:
        huo_base, ling_base = 1, 10  # 丑、戌
    elif year_zhi in shen_zi_chen:
        huo_base, ling_base = 2, 10  # 寅、戌
    elif year_zhi in si_you_chou:
        huo_base, ling_base = 4, 10  # 辰、戌
    else:  # hai_mao_wei
        huo_base, ling_base = 9, 10  # 酉、戌
    
    huoxing_pos = (huo_base + hour_idx) % 12
    lingxing_pos = (ling_base + hour_idx) % 12
    return huoxing_pos, lingxing_pos


def get_dikong_dijie_pos(hour_zhi: str) -> tuple[int, int]:
    """计算地空地劫位置
    
    地空：从亥宫起子时，顺时针数到生时
    地劫：从亥宫起子时，逆时针数到生时
    """
    hour_idx = DIZHI.index(hour_zhi)
    # 亥=11
    dikong_pos = (11 + hour_idx) % 12
    dijie_pos = (11 - hour_idx + 12) % 12
    return dikong_pos, dijie_pos


def arrange_aux_sha_stars(
    lunar_month: int, hour_zhi: str, year_gan: str, year_zhi: str,
    palaces: list[dict]
) -> list[dict]:
    """安置辅星和煞星"""
    # 六吉星
    zuofu, youbi = get_zuofu_youbi_pos(lunar_month)
    wenchang, wenqu = get_wenchang_wenqu_pos(hour_zhi)
    tiankui, tianyue = get_tiankui_tianyue_pos(year_gan)
    lucun = get_lucun_pos(year_gan)
    
    aux_stars = [
        ("左辅", zuofu), ("右弼", youbi),
        ("文昌", wenchang), ("文曲", wenqu),
        ("天魁", tiankui), ("天钺", tianyue),
        ("禄存", lucun),
    ]
    
    # 六煞星
    qingyang, tuoluo = get_qingyang_tuoluo_pos(year_gan)
    huoxing, lingxing = get_huoxing_lingxing_pos(year_zhi, hour_zhi)
    dikong, dijie = get_dikong_dijie_pos(hour_zhi)
    
    sha_stars = [
        ("擎羊", qingyang), ("陀罗", tuoluo),
        ("火星", huoxing), ("铃星", lingxing),
        ("地空", dikong), ("地劫", dijie),
    ]
    
    # 安置到宫位
    for name, pos in aux_stars:
        for palace in palaces:
            if palace["position"] == pos:
                palace["aux_stars"].append({"name": name, "type": "辅星"})
                break
    
    for name, pos in sha_stars:
        for palace in palaces:
            if palace["position"] == pos:
                palace["sha_stars"].append({"name": name, "type": "煞星"})
                break
    
    return palaces

