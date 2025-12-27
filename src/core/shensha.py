"""神煞计算模块

神煞是根据八字干支推算的特殊星宿，分为吉神和凶煞。
包括：天乙贵人、文昌、驿马、桃花、华盖、将星等。
"""
from src.models import BaziChart
from src.models.bazi_models import ShenShaInfo, ShenShaAnalysis
from .constants import TIANGAN, DIZHI


# 天乙贵人（根据日干查）
TIANYI_GUIREN = {
    "甲": ["丑", "未"], "乙": ["子", "申"], "丙": ["亥", "酉"],
    "丁": ["亥", "酉"], "戊": ["丑", "未"], "己": ["子", "申"],
    "庚": ["丑", "未"], "辛": ["寅", "午"], "壬": ["卯", "巳"],
    "癸": ["卯", "巳"],
}

# 文昌贵人（根据日干查）
WENCHANG = {
    "甲": "巳", "乙": "午", "丙": "申", "丁": "酉", "戊": "申",
    "己": "酉", "庚": "亥", "辛": "子", "壬": "寅", "癸": "卯",
}

# 驿马（根据日支查，三合局第一位冲）
YIMA = {
    "申": "寅", "子": "寅", "辰": "寅",  # 水局驿马在寅
    "寅": "申", "午": "申", "戌": "申",  # 火局驿马在申
    "亥": "巳", "卯": "巳", "未": "巳",  # 木局驿马在巳
    "巳": "亥", "酉": "亥", "丑": "亥",  # 金局驿马在亥
}

# 桃花（根据日支查，三合局沐浴位）
TAOHUA = {
    "申": "酉", "子": "酉", "辰": "酉",  # 水局桃花在酉
    "寅": "卯", "午": "卯", "戌": "卯",  # 火局桃花在卯
    "亥": "子", "卯": "子", "未": "子",  # 木局桃花在子
    "巳": "午", "酉": "午", "丑": "午",  # 金局桃花在午
}

# 华盖（根据日支查，三合局墓库位）
HUAGAI = {
    "申": "辰", "子": "辰", "辰": "辰",  # 水局华盖在辰
    "寅": "戌", "午": "戌", "戌": "戌",  # 火局华盖在戌
    "亥": "未", "卯": "未", "未": "未",  # 木局华盖在未
    "巳": "丑", "酉": "丑", "丑": "丑",  # 金局华盖在丑
}

# 将星（根据日支查，三合局帝旺位）
JIANGXING = {
    "申": "子", "子": "子", "辰": "子",
    "寅": "午", "午": "午", "戌": "午",
    "亥": "卯", "卯": "卯", "未": "卯",
    "巳": "酉", "酉": "酉", "丑": "酉",
}

# 羊刃（根据日干查，阳干帝旺位，阴干无羊刃）
YANGREN = {
    "甲": "卯", "丙": "午", "戊": "午", "庚": "酉", "壬": "子",
}

# 禄神（根据日干查）
LUSHEN = {
    "甲": "寅", "乙": "卯", "丙": "巳", "丁": "午", "戊": "巳",
    "己": "午", "庚": "申", "辛": "酉", "壬": "亥", "癸": "子",
}

# 神煞描述
SHENSHA_DESC = {
    "天乙贵人": ("吉", "贵人相助，逢凶化吉，一生多遇贵人扶持"),
    "文昌贵人": ("吉", "聪明好学，利于考试升学，文艺才华出众"),
    "驿马": ("中", "主奔波劳碌，利于外出发展，适合流动性工作"),
    "桃花": ("中", "人缘好，异性缘佳，感情丰富，注意桃花劫"),
    "华盖": ("中", "聪明孤高，适合艺术宗教，有独特审美"),
    "将星": ("吉", "有领导才能，适合管理岗位，威严有魄力"),
    "羊刃": ("凶", "性格刚烈，易有意外伤害，需注意安全"),
    "禄神": ("吉", "衣食无忧，财运稳定，福禄双全"),
}


def _get_all_dizhi(bazi: BaziChart) -> list[str]:
    """获取八字所有地支"""
    return [
        bazi.year_pillar.dizhi.value,
        bazi.month_pillar.dizhi.value,
        bazi.day_pillar.dizhi.value,
        bazi.hour_pillar.dizhi.value,
    ]


def _check_shensha(
    name: str,
    target_zhi: str | list[str],
    all_dizhi: list[str]
) -> list[str]:
    """检查神煞是否存在于八字中"""
    if isinstance(target_zhi, str):
        target_zhi = [target_zhi]
    
    found = []
    pillar_names = ["年支", "月支", "日支", "时支"]
    
    for i, zhi in enumerate(all_dizhi):
        if zhi in target_zhi:
            found.append(pillar_names[i])
    
    return found


def calculate_shensha(bazi: BaziChart) -> ShenShaAnalysis:
    """
    计算八字神煞
    
    Args:
        bazi: 八字信息
    
    Returns:
        ShenShaAnalysis: 神煞分析结果
    """
    day_gan = bazi.day_pillar.tiangan.value
    day_zhi = bazi.day_pillar.dizhi.value
    all_dizhi = _get_all_dizhi(bazi)
    
    shensha_list = []
    ji_shen = []  # 吉神
    xiong_sha = []  # 凶煞
    
    # 检查天乙贵人
    tianyi_zhi = TIANYI_GUIREN.get(day_gan, [])
    found = _check_shensha("天乙贵人", tianyi_zhi, all_dizhi)
    if found:
        quality, desc = SHENSHA_DESC["天乙贵人"]
        info = ShenShaInfo(
            name="天乙贵人", quality=quality,
            description=desc, positions=found
        )
        shensha_list.append(info)
        ji_shen.append("天乙贵人")
    
    # 检查文昌贵人
    wenchang_zhi = WENCHANG.get(day_gan)
    if wenchang_zhi:
        found = _check_shensha("文昌贵人", wenchang_zhi, all_dizhi)
        if found:
            quality, desc = SHENSHA_DESC["文昌贵人"]
            info = ShenShaInfo(
                name="文昌贵人", quality=quality,
                description=desc, positions=found
            )
            shensha_list.append(info)
            ji_shen.append("文昌贵人")
    
    # 检查驿马
    yima_zhi = YIMA.get(day_zhi)
    if yima_zhi:
        found = _check_shensha("驿马", yima_zhi, all_dizhi)
        if found:
            quality, desc = SHENSHA_DESC["驿马"]
            info = ShenShaInfo(
                name="驿马", quality=quality,
                description=desc, positions=found
            )
            shensha_list.append(info)
    
    # 检查桃花
    taohua_zhi = TAOHUA.get(day_zhi)
    if taohua_zhi:
        found = _check_shensha("桃花", taohua_zhi, all_dizhi)
        if found:
            quality, desc = SHENSHA_DESC["桃花"]
            info = ShenShaInfo(
                name="桃花", quality=quality,
                description=desc, positions=found
            )
            shensha_list.append(info)
    
    # 检查华盖
    huagai_zhi = HUAGAI.get(day_zhi)
    if huagai_zhi:
        found = _check_shensha("华盖", huagai_zhi, all_dizhi)
        if found:
            quality, desc = SHENSHA_DESC["华盖"]
            info = ShenShaInfo(
                name="华盖", quality=quality,
                description=desc, positions=found
            )
            shensha_list.append(info)
    
    # 检查将星
    jiangxing_zhi = JIANGXING.get(day_zhi)
    if jiangxing_zhi:
        found = _check_shensha("将星", jiangxing_zhi, all_dizhi)
        if found:
            quality, desc = SHENSHA_DESC["将星"]
            info = ShenShaInfo(
                name="将星", quality=quality,
                description=desc, positions=found
            )
            shensha_list.append(info)
            ji_shen.append("将星")
    
    # 检查羊刃
    yangren_zhi = YANGREN.get(day_gan)
    if yangren_zhi:
        found = _check_shensha("羊刃", yangren_zhi, all_dizhi)
        if found:
            quality, desc = SHENSHA_DESC["羊刃"]
            info = ShenShaInfo(
                name="羊刃", quality=quality,
                description=desc, positions=found
            )
            shensha_list.append(info)
            xiong_sha.append("羊刃")
    
    # 检查禄神
    lushen_zhi = LUSHEN.get(day_gan)
    if lushen_zhi:
        found = _check_shensha("禄神", lushen_zhi, all_dizhi)
        if found:
            quality, desc = SHENSHA_DESC["禄神"]
            info = ShenShaInfo(
                name="禄神", quality=quality,
                description=desc, positions=found
            )
            shensha_list.append(info)
            ji_shen.append("禄神")
    
    # 生成总结
    summary = _generate_summary(ji_shen, xiong_sha, shensha_list)
    
    return ShenShaAnalysis(
        shensha_list=shensha_list,
        ji_shen=ji_shen,
        xiong_sha=xiong_sha,
        summary=summary
    )


def _generate_summary(
    ji_shen: list[str],
    xiong_sha: list[str],
    all_shensha: list
) -> str:
    """生成神煞总结"""
    parts = []
    
    if ji_shen:
        parts.append(f"命带{', '.join(ji_shen)}等吉神")
    
    if xiong_sha:
        parts.append(f"有{', '.join(xiong_sha)}需注意")
    
    if not parts:
        return "神煞配置平和，无明显吉凶。"
    
    return "，".join(parts) + "。"
