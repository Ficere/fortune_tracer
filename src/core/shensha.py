"""神煞计算模块 - 吉神凶煞分析"""
from src.models import BaziChart
from src.models.bazi_models import ShenShaInfo, ShenShaAnalysis
from .shensha_data import (
    TIANYI_GUIREN, WENCHANG, YIMA, TAOHUA,
    HUAGAI, JIANGXING, YANGREN, LUSHEN, SHENSHA_DESC
)

PILLAR_NAMES = ["年支", "月支", "日支", "时支"]


def _get_all_dizhi(bazi: BaziChart) -> list[str]:
    """获取八字所有地支"""
    return [
        bazi.year_pillar.dizhi.value,
        bazi.month_pillar.dizhi.value,
        bazi.day_pillar.dizhi.value,
        bazi.hour_pillar.dizhi.value,
    ]


def _check_shensha(target_zhi: str | list, all_dizhi: list[str]) -> list[str]:
    """检查神煞是否存在于八字中，返回所在柱位"""
    targets = [target_zhi] if isinstance(target_zhi, str) else target_zhi
    return [PILLAR_NAMES[i] for i, zhi in enumerate(all_dizhi) if zhi in targets]


def _add_shensha(
    name: str, target_zhi, all_dizhi: list[str],
    shensha_list: list, ji_shen: list, xiong_sha: list
) -> None:
    """检查并添加神煞到列表"""
    if not target_zhi:
        return
    
    found = _check_shensha(target_zhi, all_dizhi)
    if not found:
        return
    
    quality, desc = SHENSHA_DESC[name]
    shensha_list.append(ShenShaInfo(
        name=name, quality=quality, description=desc, positions=found
    ))
    
    if quality == "吉":
        ji_shen.append(name)
    elif quality == "凶":
        xiong_sha.append(name)


def calculate_shensha(bazi: BaziChart) -> ShenShaAnalysis:
    """计算八字神煞"""
    day_gan = bazi.day_pillar.tiangan.value
    day_zhi = bazi.day_pillar.dizhi.value
    all_dizhi = _get_all_dizhi(bazi)
    
    shensha_list = []
    ji_shen = []
    xiong_sha = []
    
    # 检查各类神煞
    checks = [
        ("天乙贵人", TIANYI_GUIREN.get(day_gan, [])),
        ("文昌贵人", WENCHANG.get(day_gan)),
        ("驿马", YIMA.get(day_zhi)),
        ("桃花", TAOHUA.get(day_zhi)),
        ("华盖", HUAGAI.get(day_zhi)),
        ("将星", JIANGXING.get(day_zhi)),
        ("羊刃", YANGREN.get(day_gan)),
        ("禄神", LUSHEN.get(day_gan)),
    ]
    
    for name, target in checks:
        _add_shensha(name, target, all_dizhi, shensha_list, ji_shen, xiong_sha)
    
    # 生成总结
    summary = _generate_summary(ji_shen, xiong_sha)
    
    return ShenShaAnalysis(
        shensha_list=shensha_list,
        ji_shen=ji_shen,
        xiong_sha=xiong_sha,
        summary=summary
    )


def _generate_summary(ji_shen: list[str], xiong_sha: list[str]) -> str:
    """生成神煞总结"""
    parts = []
    if ji_shen:
        parts.append(f"命带{', '.join(ji_shen)}等吉神")
    if xiong_sha:
        parts.append(f"有{', '.join(xiong_sha)}需注意")
    return "，".join(parts) + "。" if parts else "神煞配置平和，无明显吉凶。"
