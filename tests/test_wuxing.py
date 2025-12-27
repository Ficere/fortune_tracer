"""五行分析测试"""
import pytest
from src.core import calculate_bazi, analyze_wuxing
from src.core.wuxing import (
    _count_wuxing, _get_day_master,
    _analyze_strength, _get_favorable_unfavorable
)
from src.models.bazi_models import Gender, Wuxing, WuxingCount
from datetime import datetime


class TestCountWuxing:
    """五行统计测试"""
    
    def test_count_wuxing_returns_count(self, sample_male_bazi):
        """应返回 WuxingCount 对象"""
        counts = _count_wuxing(sample_male_bazi)
        assert isinstance(counts, WuxingCount)
    
    def test_count_wuxing_all_elements(self, sample_male_bazi):
        """应统计所有五行"""
        counts = _count_wuxing(sample_male_bazi)
        assert hasattr(counts, 'mu')
        assert hasattr(counts, 'huo')
        assert hasattr(counts, 'tu')
        assert hasattr(counts, 'jin')
        assert hasattr(counts, 'shui')
    
    def test_count_wuxing_positive_values(self, sample_male_bazi):
        """五行数量应为非负数"""
        counts = _count_wuxing(sample_male_bazi)
        assert counts.mu >= 0
        assert counts.huo >= 0
        assert counts.tu >= 0
        assert counts.jin >= 0
        assert counts.shui >= 0
    
    def test_count_wuxing_to_dict(self, sample_male_bazi):
        """to_dict 应返回正确格式"""
        counts = _count_wuxing(sample_male_bazi)
        d = counts.to_dict()
        assert "木" in d
        assert "火" in d
        assert "土" in d
        assert "金" in d
        assert "水" in d


class TestGetDayMaster:
    """日主测试"""
    
    def test_get_day_master_returns_wuxing(self, sample_male_bazi):
        """应返回 Wuxing 枚举"""
        dm = _get_day_master(sample_male_bazi)
        assert isinstance(dm, Wuxing)
    
    def test_get_day_master_valid(self, sample_male_bazi):
        """日主应是有效的五行"""
        dm = _get_day_master(sample_male_bazi)
        assert dm.value in ["木", "火", "土", "金", "水"]


class TestAnalyzeStrength:
    """日主强弱分析测试"""
    
    def test_analyze_strength_returns_string(self, sample_male_bazi):
        """应返回字符串"""
        counts = _count_wuxing(sample_male_bazi)
        dm = _get_day_master(sample_male_bazi)
        strength = _analyze_strength(counts, dm)
        assert isinstance(strength, str)
    
    def test_analyze_strength_valid_values(self, sample_male_bazi):
        """应返回有效的强弱描述"""
        counts = _count_wuxing(sample_male_bazi)
        dm = _get_day_master(sample_male_bazi)
        strength = _analyze_strength(counts, dm)
        assert strength in ["身旺", "中和", "身弱"]


class TestGetFavorableUnfavorable:
    """喜忌神测试"""
    
    def test_get_favorable_returns_lists(self, sample_male_bazi):
        """应返回两个列表"""
        dm = _get_day_master(sample_male_bazi)
        favorable, unfavorable = _get_favorable_unfavorable(dm, "身旺")
        assert isinstance(favorable, list)
        assert isinstance(unfavorable, list)
    
    def test_get_favorable_not_empty(self, sample_male_bazi):
        """喜忌神列表不应为空"""
        dm = _get_day_master(sample_male_bazi)
        favorable, unfavorable = _get_favorable_unfavorable(dm, "身旺")
        assert len(favorable) > 0
        assert len(unfavorable) > 0
    
    def test_favorable_unfavorable_different(self, sample_male_bazi):
        """喜用神和忌神应不同"""
        dm = _get_day_master(sample_male_bazi)
        favorable, unfavorable = _get_favorable_unfavorable(dm, "身旺")
        favorable_values = set(f.value for f in favorable)
        unfavorable_values = set(u.value for u in unfavorable)
        assert favorable_values.isdisjoint(unfavorable_values)


class TestAnalyzeWuxing:
    """完整五行分析测试"""
    
    def test_analyze_wuxing_returns_analysis(self, sample_male_bazi):
        """应返回完整的 WuxingAnalysis"""
        analysis = analyze_wuxing(sample_male_bazi)
        assert analysis.counts is not None
        assert analysis.day_master is not None
        assert analysis.day_master_strength is not None
        assert analysis.favorable is not None
        assert analysis.unfavorable is not None
    
    def test_analyze_wuxing_consistency(self, sample_male_bazi):
        """相同输入应产生相同结果"""
        analysis1 = analyze_wuxing(sample_male_bazi)
        analysis2 = analyze_wuxing(sample_male_bazi)
        assert analysis1.day_master == analysis2.day_master
        assert analysis1.day_master_strength == analysis2.day_master_strength
    
    @pytest.mark.parametrize("dt,gender", [
        (datetime(1990, 1, 15, 8, 30), Gender.MALE),
        (datetime(1985, 6, 20, 14, 0), Gender.FEMALE),
        (datetime(2000, 12, 31, 23, 59), Gender.MALE),
        (datetime(1970, 3, 8, 6, 0), Gender.FEMALE),
    ])
    def test_analyze_wuxing_various_inputs(self, dt, gender):
        """应能处理各种输入"""
        bazi = calculate_bazi(dt, gender)
        analysis = analyze_wuxing(bazi)
        assert analysis is not None
        assert len(analysis.favorable) > 0
