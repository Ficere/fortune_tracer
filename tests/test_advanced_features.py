"""高级功能测试 - 神煞、纳音、流年"""
import pytest
from datetime import datetime
from src.core import (
    calculate_bazi, analyze_wuxing, calculate_dayun,
    calculate_shensha, calculate_nayin, get_year_nayin,
    calculate_liunian
)
from src.models.bazi_models import (
    Gender, ShenShaAnalysis, NaYinInfo, LiuNianAnalysis
)


class TestShensha:
    """神煞计算测试"""
    
    def test_calculate_shensha_returns_analysis(self, sample_male_bazi):
        """应返回 ShenShaAnalysis"""
        result = calculate_shensha(sample_male_bazi)
        assert isinstance(result, ShenShaAnalysis)
    
    def test_calculate_shensha_has_lists(self, sample_male_bazi):
        """应包含神煞列表"""
        result = calculate_shensha(sample_male_bazi)
        assert hasattr(result, 'shensha_list')
        assert hasattr(result, 'ji_shen')
        assert hasattr(result, 'xiong_sha')
    
    def test_calculate_shensha_has_summary(self, sample_male_bazi):
        """应有总结"""
        result = calculate_shensha(sample_male_bazi)
        assert result.summary != ""
    
    def test_shensha_info_has_quality(self, sample_male_bazi):
        """神煞应有吉凶属性"""
        result = calculate_shensha(sample_male_bazi)
        for shensha in result.shensha_list:
            assert shensha.quality in ["吉", "凶", "中"]


class TestNayin:
    """纳音计算测试"""
    
    def test_calculate_nayin_returns_list(self, sample_male_bazi):
        """应返回四柱纳音列表"""
        result = calculate_nayin(sample_male_bazi)
        assert isinstance(result, list)
        assert len(result) == 4
    
    def test_calculate_nayin_info_complete(self, sample_male_bazi):
        """纳音信息应完整"""
        result = calculate_nayin(sample_male_bazi)
        for info in result:
            assert isinstance(info, NaYinInfo)
            assert info.ganzhi != ""
            assert info.nayin != ""
            assert info.wuxing in ["金", "木", "水", "火", "土"]
    
    def test_get_year_nayin(self):
        """应能获取年命纳音"""
        info = get_year_nayin(1990)
        assert isinstance(info, NaYinInfo)
        assert info.pillar_name == "年命"
        assert info.ganzhi == "庚午"
        assert info.nayin == "路旁土"
    
    @pytest.mark.parametrize("year,expected_nayin", [
        (1984, "海中金"),  # 甲子年
        (1990, "路旁土"),  # 庚午年
        (2000, "白蜡金"),  # 庚辰年
        (2024, "覆灯火"),  # 甲辰年
    ])
    def test_get_year_nayin_known_years(self, year, expected_nayin):
        """测试已知年份的纳音"""
        info = get_year_nayin(year)
        assert info.nayin == expected_nayin


class TestLiunian:
    """流年分析测试"""
    
    def test_calculate_liunian_returns_analysis(self, sample_male_bazi, sample_wuxing):
        """应返回 LiuNianAnalysis"""
        result = calculate_liunian(sample_male_bazi, sample_wuxing)
        assert isinstance(result, LiuNianAnalysis)
    
    def test_calculate_liunian_list_length(self, sample_male_bazi, sample_wuxing):
        """应有正确数量的流年"""
        result = calculate_liunian(sample_male_bazi, sample_wuxing, years=10)
        assert len(result.liunian_list) == 10
    
    def test_calculate_liunian_has_summary(self, sample_male_bazi, sample_wuxing):
        """应有总结"""
        result = calculate_liunian(sample_male_bazi, sample_wuxing)
        assert result.summary != ""
    
    def test_liunian_fortune_complete(self, sample_male_bazi, sample_wuxing):
        """流年运势信息应完整"""
        result = calculate_liunian(sample_male_bazi, sample_wuxing, years=5)
        current_year = datetime.now().year
        
        for i, fortune in enumerate(result.liunian_list):
            assert fortune.year == current_year + i
            assert fortune.ganzhi != ""
            assert fortune.wuxing in ["金", "木", "水", "火", "土"]
            assert 0 <= fortune.score <= 100
            assert fortune.level in ["大吉", "吉", "平", "凶", "大凶"]
    
    def test_liunian_best_caution_years(self, sample_male_bazi, sample_wuxing):
        """应有较好和需注意年份"""
        result = calculate_liunian(sample_male_bazi, sample_wuxing, years=10)
        assert len(result.best_years) > 0
        assert len(result.caution_years) > 0


class TestCache:
    """缓存测试"""
    
    def test_cache_import(self):
        """应能导入缓存模块"""
        from src.core import get_cache, clear_cache, cache_stats
        
        cache = get_cache()
        assert cache is not None
    
    def test_cache_operations(self):
        """缓存操作应正常"""
        from src.core import get_cache, clear_cache
        
        cache = get_cache()
        
        # 设置
        cache.set("test_key", "test_value", ttl=60)
        
        # 获取
        value = cache.get("test_key")
        assert value == "test_value"
        
        # 删除
        cache.delete("test_key")
        assert cache.get("test_key") is None
        
        # 清空
        cache.set("key1", "value1")
        cache.set("key2", "value2")
        clear_cache()
        assert cache.size == 0
    
    def test_cache_stats(self):
        """缓存统计应正常"""
        from src.core import cache_stats
        
        stats = cache_stats()
        assert "size" in stats
        assert "enabled" in stats
