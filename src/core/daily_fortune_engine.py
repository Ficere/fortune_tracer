"""每日运势核心计算引擎 - 干支关系与十神分析"""
from datetime import date
from src.core.constants import (
    TIANGAN, DIZHI, TIANGAN_WUXING, DIZHI_WUXING, DIZHI_CANGAN,
    DIZHI_LIUHE, DIZHI_LIUCHONG, DIZHI_XING, DIZHI_SANHE,
    TIANGAN_HE, TIANGAN_CHONG, WUXING_SHENG, WUXING_KE
)
from src.models.bazi_models import BaziChart, WuxingAnalysis
from src.core.shishen import _get_shishen, _is_yang_gan


class DailyFortuneEngine:
    """每日运势计算引擎"""
    
    def __init__(self, bazi: BaziChart, wuxing: WuxingAnalysis, target_date: date):
        self.bazi = bazi
        self.wuxing = wuxing
        self.target_date = target_date
        
        # 计算当日干支
        self.day_gan, self.day_zhi = self._get_day_ganzhi()
        self.day_wx = TIANGAN_WUXING[self.day_gan]
        
        # 喜用神列表
        self.favorable = [w.value for w in wuxing.favorable]
        self.unfavorable = [w.value for w in wuxing.unfavorable]
        
        # 计算各项因素
        self._analyze_all()
    
    def _get_day_ganzhi(self) -> tuple[str, str]:
        """计算日干支"""
        base_date = date(2000, 1, 1)
        base_gan_idx, base_zhi_idx = 5, 11  # 己亥
        days_diff = (self.target_date - base_date).days
        return TIANGAN[(base_gan_idx + days_diff) % 10], DIZHI[(base_zhi_idx + days_diff) % 12]
    
    def _analyze_all(self):
        """分析所有命理因素"""
        self.factors = {"favorable": [], "unfavorable": [], "scores": {}}
        
        # 1. 喜用神分析
        self._analyze_favorable_god()
        # 2. 天干关系
        self._analyze_tiangan_relations()
        # 3. 地支关系
        self._analyze_dizhi_relations()
        # 4. 十神分析
        self._analyze_shishen()
    
    def _analyze_favorable_god(self):
        """喜用神当值分析"""
        if self.day_wx in self.favorable:
            self.factors["favorable"].append(f"流日五行{self.day_wx}为喜用神(+20)")
            self.factors["scores"]["favorable_god"] = 20
        elif self.day_wx in self.unfavorable:
            self.factors["unfavorable"].append(f"流日五行{self.day_wx}为忌神(-15)")
            self.factors["scores"]["unfavorable_god"] = -15
        else:
            self.factors["scores"]["neutral"] = 0
    
    def _analyze_tiangan_relations(self):
        """天干合冲分析"""
        bazi_gans = [
            self.bazi.year_pillar.tiangan.value,
            self.bazi.month_pillar.tiangan.value,
            self.bazi.day_pillar.tiangan.value,
            self.bazi.hour_pillar.tiangan.value,
        ]
        
        gan_score = 0
        for gan in bazi_gans:
            pair = tuple(sorted([self.day_gan, gan]))
            rev_pair = (pair[1], pair[0])
            
            # 天干五合
            if pair in TIANGAN_HE or rev_pair in TIANGAN_HE:
                self.factors["favorable"].append(f"{self.day_gan}与{gan}天干相合(+8)")
                gan_score += 8
            
            # 天干相冲
            if pair in TIANGAN_CHONG or rev_pair in TIANGAN_CHONG:
                self.factors["unfavorable"].append(f"{self.day_gan}与{gan}天干相冲(-10)")
                gan_score -= 10
        
        self.factors["scores"]["tiangan"] = gan_score
    
    def _analyze_dizhi_relations(self):
        """地支合冲刑害分析"""
        bazi_zhis = [
            (self.bazi.year_pillar.dizhi.value, "年支"),
            (self.bazi.month_pillar.dizhi.value, "月支"),
            (self.bazi.day_pillar.dizhi.value, "日支"),
            (self.bazi.hour_pillar.dizhi.value, "时支"),
        ]
        
        zhi_score = 0
        for zhi, name in bazi_zhis:
            pair = tuple(sorted([self.day_zhi, zhi]))
            rev_pair = (pair[1], pair[0])
            
            # 六合
            if pair in DIZHI_LIUHE or rev_pair in DIZHI_LIUHE:
                bonus = 10 if name == "日支" else 6
                self.factors["favorable"].append(f"{self.day_zhi}与{name}{zhi}六合(+{bonus})")
                zhi_score += bonus
            
            # 六冲
            if pair in DIZHI_LIUCHONG or rev_pair in DIZHI_LIUCHONG:
                penalty = -15 if name == "日支" else -10
                self.factors["unfavorable"].append(f"{self.day_zhi}与{name}{zhi}六冲({penalty})")
                zhi_score += penalty
            
            # 三刑
            if pair in DIZHI_XING or rev_pair in DIZHI_XING:
                self.factors["unfavorable"].append(f"{self.day_zhi}与{name}{zhi}相刑(-8)")
                zhi_score -= 8
        
        self.factors["scores"]["dizhi"] = zhi_score
    
    def _analyze_shishen(self):
        """十神星宿分析"""
        day_master = self.bazi.day_pillar.tiangan.value
        day_shishen = _get_shishen(day_master, self.day_gan)
        
        # 十神评分调整
        shishen_scores = {
            "正官": 5, "正印": 6, "正财": 5, "食神": 4,
            "七杀": -3, "伤官": -2, "劫财": -4, "偏印": 2,
            "偏财": 3, "比肩": 0
        }
        
        score = shishen_scores.get(day_shishen, 0)
        if score > 0:
            self.factors["favorable"].append(f"流日十神为{day_shishen}(+{score})")
        elif score < 0:
            self.factors["unfavorable"].append(f"流日十神为{day_shishen}({score})")
        
        self.factors["scores"]["shishen"] = score
        self.factors["day_shishen"] = day_shishen
    
    def get_base_score(self) -> tuple[float, dict]:
        """获取基础总分和明细"""
        base = 60.0
        breakdown = {"base": 60}
        
        for key, value in self.factors["scores"].items():
            base += value
            breakdown[key] = value
        
        return round(min(max(base, 15), 98), 1), breakdown

