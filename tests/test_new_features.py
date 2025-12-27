"""新功能测试 - 大运、十神、节气、真太阳时"""
import pytest
from datetime import datetime
from src.core import (
    calculate_bazi, analyze_wuxing,
    calculate_dayun, get_current_dayun,
    analyze_shishen,
    get_jieqi_month, is_before_lichun, get_jieqi_for_year,
    convert_to_true_solar_time, get_time_correction_info,
    get_settings,
)
from src.models.bazi_models import Gender, DaYunInfo, ShiShenAnalysis


class TestDayun:
    """大运计算测试"""
    
    def test_calculate_dayun_returns_info(self, sample_male_bazi):
        """应返回 DaYunInfo"""
        result = calculate_dayun(sample_male_bazi)
        assert isinstance(result, DaYunInfo)
    
    def test_calculate_dayun_direction(self, sample_male_bazi, sample_female_bazi):
        """大运方向应正确"""
        male_result = calculate_dayun(sample_male_bazi)
        female_result = calculate_dayun(sample_female_bazi)
        assert male_result.direction in ["顺行", "逆行"]
        assert female_result.direction in ["顺行", "逆行"]
    
    def test_calculate_dayun_list_length(self, sample_male_bazi):
        """大运列表长度应正确"""
        result = calculate_dayun(sample_male_bazi, num_dayun=8)
        assert len(result.dayun_list) == 8
    
    def test_calculate_dayun_ages(self, sample_male_bazi):
        """大运年龄应递增"""
        result = calculate_dayun(sample_male_bazi)
        for i, dayun in enumerate(result.dayun_list[:-1]):
            next_dayun = result.dayun_list[i + 1]
            assert next_dayun.start_age > dayun.start_age
    
    def test_get_current_dayun(self, sample_male_bazi):
        """应能获取当前大运"""
        dayun_info = calculate_dayun(sample_male_bazi)
        # 测试中间年龄
        current = get_current_dayun(dayun_info, 35)
        if current:
            assert current.start_age <= 35 <= current.end_age


class TestShishen:
    """十神分析测试"""
    
    def test_analyze_shishen_returns_analysis(self, sample_male_bazi):
        """应返回 ShiShenAnalysis"""
        result = analyze_shishen(sample_male_bazi)
        assert isinstance(result, ShiShenAnalysis)
    
    def test_analyze_shishen_list_length(self, sample_male_bazi):
        """应有四柱的十神信息"""
        result = analyze_shishen(sample_male_bazi)
        assert len(result.shishen_list) == 4
    
    def test_analyze_shishen_pattern(self, sample_male_bazi):
        """应有格局判断"""
        result = analyze_shishen(sample_male_bazi)
        assert result.pattern != ""
    
    def test_analyze_shishen_day_master(self, sample_male_bazi):
        """日柱天干应标记为日主"""
        result = analyze_shishen(sample_male_bazi)
        day_info = next(s for s in result.shishen_list if s.pillar_name == "日柱")
        assert day_info.tiangan_shishen == "日主"


class TestJieqi:
    """节气计算测试"""
    
    def test_get_jieqi_for_year(self):
        """应获取24个节气"""
        jieqi_list = get_jieqi_for_year(2024)
        assert len(jieqi_list) == 24
    
    def test_get_jieqi_month(self):
        """应返回正确的月份"""
        # 立春后应为寅月（1）
        month = get_jieqi_month(datetime(2024, 2, 10))
        assert 1 <= month <= 12
    
    def test_is_before_lichun(self):
        """应正确判断立春前后"""
        # 1月应在立春前
        assert is_before_lichun(datetime(2024, 1, 15))
        # 3月应在立春后
        assert not is_before_lichun(datetime(2024, 3, 15))


class TestSolarTime:
    """真太阳时测试"""
    
    def test_convert_to_true_solar_time_no_location(self):
        """无地点时应返回原时间"""
        local_time = datetime(2024, 6, 15, 12, 0)
        result = convert_to_true_solar_time(local_time, None)
        assert result == local_time
    
    def test_convert_to_true_solar_time_with_city(self):
        """有城市时应转换"""
        local_time = datetime(2024, 6, 15, 12, 0)
        result = convert_to_true_solar_time(local_time, "北京")
        # 北京在东八区，经度约116度，应有时间差
        assert result != local_time
    
    def test_convert_to_true_solar_time_unknown_city(self):
        """未知城市应返回原时间"""
        local_time = datetime(2024, 6, 15, 12, 0)
        result = convert_to_true_solar_time(local_time, "未知城市XYZ")
        assert result == local_time
    
    def test_get_time_correction_info(self):
        """应返回详细修正信息"""
        info = get_time_correction_info(datetime(2024, 6, 15, 12, 0), "上海")
        assert info["found"] is True
        assert "longitude_correction_minutes" in info
        assert "equation_of_time_minutes" in info


class TestConfig:
    """配置测试"""
    
    def test_get_settings(self):
        """应能获取配置"""
        settings = get_settings()
        assert settings.app_name == "Fortune Tracer"
    
    def test_settings_defaults(self):
        """应有默认值"""
        settings = get_settings()
        assert settings.log_level == "INFO"
        assert settings.default_dayun_count == 8
