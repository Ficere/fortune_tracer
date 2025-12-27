"""辅助宫位计算测试"""
import pytest
from datetime import datetime
from src.core import (
    calculate_bazi, calculate_ming_gong, calculate_tai_yuan, 
    calculate_shen_gong, calculate_auxiliary, calculate_auxiliary_from_bazi
)
from src.models.bazi_models import Gender


class TestMingGong:
    """命宫计算测试"""
    
    def test_ming_gong_returns_gonginfo(self):
        """测试命宫返回正确的结构"""
        result = calculate_ming_gong("甲", "寅", "子")
        assert result.name == "命宫"
        assert result.tiangan in "甲乙丙丁戊己庚辛壬癸"
        assert result.dizhi in "子丑寅卯辰巳午未申酉戌亥"
        assert len(result.ganzhi) == 2
    
    def test_ming_gong_all_months(self):
        """测试所有月支的命宫计算"""
        months = ["寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥", "子", "丑"]
        
        for month in months:
            result = calculate_ming_gong("甲", month, "子")
            assert result is not None
            assert result.dizhi in "子丑寅卯辰巳午未申酉戌亥"
    
    def test_ming_gong_all_hours(self):
        """测试所有时支的命宫计算"""
        hours = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
        
        for hour in hours:
            result = calculate_ming_gong("甲", "寅", hour)
            assert result is not None
    
    def test_ming_gong_all_year_gans(self):
        """测试所有年干的命宫天干计算"""
        year_gans = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
        
        for gan in year_gans:
            result = calculate_ming_gong(gan, "寅", "子")
            assert result.tiangan in "甲乙丙丁戊己庚辛壬癸"
    
    def test_ming_gong_has_description(self):
        """测试命宫有描述"""
        result = calculate_ming_gong("甲", "寅", "午")
        assert len(result.description) > 0


class TestTaiYuan:
    """胎元计算测试"""
    
    def test_tai_yuan_basic(self):
        """测试胎元基本计算"""
        # 月柱甲寅，胎元应该是乙巳（天干+1，地支+3）
        result = calculate_tai_yuan("甲", "寅")
        assert result.name == "胎元"
        assert result.tiangan == "乙"
        assert result.dizhi == "巳"
        assert result.ganzhi == "乙巳"
    
    def test_tai_yuan_wrap_around_gan(self):
        """测试胎元天干进位循环"""
        # 癸月干+1 = 甲
        result = calculate_tai_yuan("癸", "子")
        assert result.tiangan == "甲"
    
    def test_tai_yuan_wrap_around_zhi(self):
        """测试胎元地支进位循环"""
        # 戌月支+3 = 丑
        result = calculate_tai_yuan("甲", "戌")
        assert result.dizhi == "丑"
    
    def test_tai_yuan_all_months(self):
        """测试所有月份的胎元"""
        months = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
        gans = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸", "甲", "乙"]
        
        for gan, zhi in zip(gans, months):
            result = calculate_tai_yuan(gan, zhi)
            assert result is not None
            assert len(result.description) > 0


class TestShenGong:
    """身宫计算测试"""
    
    def test_shen_gong_returns_gonginfo(self):
        """测试身宫返回正确的结构"""
        result = calculate_shen_gong("甲", "寅", "子")
        assert result.name == "身宫"
        assert result.tiangan in "甲乙丙丁戊己庚辛壬癸"
        assert result.dizhi in "子丑寅卯辰巳午未申酉戌亥"
    
    def test_shen_gong_all_combinations(self):
        """测试多种组合"""
        months = ["寅", "午", "戌"]
        hours = ["子", "午", "卯", "酉"]
        
        for month in months:
            for hour in hours:
                result = calculate_shen_gong("甲", month, hour)
                assert result is not None
    
    def test_shen_gong_has_description(self):
        """测试身宫有描述"""
        result = calculate_shen_gong("甲", "寅", "午")
        assert len(result.description) > 0


class TestAuxiliary:
    """辅助计算综合测试"""
    
    def test_calculate_auxiliary_returns_all(self):
        """测试综合计算返回所有宫位"""
        result = calculate_auxiliary("甲", "丙", "寅", "子")
        
        assert result.ming_gong is not None
        assert result.tai_yuan is not None
        assert result.shen_gong is not None
        
        assert result.ming_gong.name == "命宫"
        assert result.tai_yuan.name == "胎元"
        assert result.shen_gong.name == "身宫"
    
    def test_calculate_auxiliary_from_bazi(self):
        """测试从八字对象计算辅助宫位"""
        bazi = calculate_bazi(datetime(1984, 2, 4, 12, 0), Gender.MALE)
        result = calculate_auxiliary_from_bazi(bazi)
        
        assert result.ming_gong is not None
        assert result.tai_yuan is not None
        assert result.shen_gong is not None
    
    def test_various_bazi_auxiliary(self):
        """测试多种八字的辅助宫位"""
        test_cases = [
            (datetime(1990, 6, 15, 8, 0), Gender.MALE),
            (datetime(2000, 12, 25, 22, 0), Gender.FEMALE),
            (datetime(1985, 3, 10, 5, 30), Gender.MALE),
        ]
        
        for dt, gender in test_cases:
            bazi = calculate_bazi(dt, gender)
            result = calculate_auxiliary_from_bazi(bazi)
            
            # 验证所有宫位都有效
            assert result.ming_gong.ganzhi
            assert result.tai_yuan.ganzhi
            assert result.shen_gong.ganzhi


class TestAuxiliaryConsistency:
    """辅助宫位一致性测试"""
    
    def test_same_input_same_output(self):
        """测试相同输入产生相同输出"""
        result1 = calculate_auxiliary("甲", "丙", "寅", "午")
        result2 = calculate_auxiliary("甲", "丙", "寅", "午")
        
        assert result1.ming_gong.ganzhi == result2.ming_gong.ganzhi
        assert result1.tai_yuan.ganzhi == result2.tai_yuan.ganzhi
        assert result1.shen_gong.ganzhi == result2.shen_gong.ganzhi
    
    def test_different_year_gan_affects_tiangan_only(self):
        """测试年干变化只影响天干"""
        result1 = calculate_auxiliary("甲", "丙", "寅", "午")
        result2 = calculate_auxiliary("乙", "丙", "寅", "午")
        
        # 命宫和身宫地支应相同（只由月支和时支决定）
        assert result1.ming_gong.dizhi == result2.ming_gong.dizhi
        assert result1.shen_gong.dizhi == result2.shen_gong.dizhi
        
        # 胎元不受年干影响
        assert result1.tai_yuan.ganzhi == result2.tai_yuan.ganzhi
