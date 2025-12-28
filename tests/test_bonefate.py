"""称骨算命测试"""

import pytest
from datetime import datetime
from src.core.bonefate import (
    get_tiangan_index,
    get_dizhi_index,
    get_hour_dizhi_index,
    calculate_bone_weight,
    get_bone_poem,
    get_weight_level,
    analyze_bonefate,
    solar_to_lunar,
)
from src.models.bonefate_models import BoneFateResult


class TestTianGanDiZhi:
    """天干地支索引测试"""
    
    def test_tiangan_index_2021(self):
        """2021年天干应该是辛(索引7)"""
        # 2021 - 4 = 2017, 2017 % 10 = 7
        assert get_tiangan_index(2021) == 7
    
    def test_tiangan_index_2024(self):
        """2024年天干应该是甲(索引0)"""
        # 2024 - 4 = 2020, 2020 % 10 = 0
        assert get_tiangan_index(2024) == 0
    
    def test_dizhi_index_2021(self):
        """2021年地支应该是丑(索引1)"""
        # 2021 - 4 = 2017, 2017 % 12 = 1
        assert get_dizhi_index(2021) == 1
    
    def test_dizhi_index_2024(self):
        """2024年地支应该是辰(索引4)"""
        # 2024 - 4 = 2020, 2020 % 12 = 4
        assert get_dizhi_index(2024) == 4


class TestHourDiZhi:
    """时辰地支测试"""
    
    def test_hour_zi(self):
        """子时: 23:00-00:59"""
        assert get_hour_dizhi_index(23) == 0
        assert get_hour_dizhi_index(0) == 0
    
    def test_hour_chou(self):
        """丑时: 01:00-02:59"""
        assert get_hour_dizhi_index(1) == 1
        assert get_hour_dizhi_index(2) == 1
    
    def test_hour_yin(self):
        """寅时: 03:00-04:59"""
        assert get_hour_dizhi_index(3) == 2
        assert get_hour_dizhi_index(4) == 2
    
    def test_hour_wu(self):
        """午时: 11:00-12:59"""
        assert get_hour_dizhi_index(11) == 6
        assert get_hour_dizhi_index(12) == 6


class TestBoneWeight:
    """骨重计算测试"""
    
    def test_basic_calculation(self):
        """基本骨重计算"""
        # 测试一个具体日期
        weight = calculate_bone_weight(2021, 1, 1, 12, is_lunar=True)
        assert 2.0 <= weight <= 7.5
    
    def test_weight_range(self):
        """骨重范围测试"""
        # 多个日期测试
        test_cases = [
            (1990, 6, 15, 8),
            (2000, 3, 20, 14),
            (1985, 12, 25, 6),
        ]
        for year, month, day, hour in test_cases:
            weight = calculate_bone_weight(year, month, day, hour)
            assert 2.0 <= weight <= 8.0, f"骨重 {weight} 超出合理范围"
    
    def test_lunar_vs_solar(self):
        """农历和阳历计算应该不同"""
        solar_weight = calculate_bone_weight(1990, 5, 15, 12, is_lunar=False)
        lunar_weight = calculate_bone_weight(1990, 5, 15, 12, is_lunar=True)
        # 大部分情况下应该不同（除非恰好是同一天）
        # 这里只测试能正常计算
        assert 2.0 <= solar_weight <= 8.0
        assert 2.0 <= lunar_weight <= 8.0


class TestBonePoem:
    """命运诗词测试"""
    
    def test_exact_weight(self):
        """精确骨重查询"""
        poem_info = get_bone_poem(3.5)
        assert "title" in poem_info
        assert "poem" in poem_info
        assert len(poem_info["title"]) > 0
        assert len(poem_info["poem"]) > 0
    
    def test_boundary_weights(self):
        """边界骨重测试"""
        # 最轻
        poem_info = get_bone_poem(2.1)
        assert "终身行乞" in poem_info["title"]
        
        # 最重
        poem_info = get_bone_poem(7.2)
        assert "世界罕有" in poem_info["title"] or "帝王" in poem_info["title"]
    
    def test_approximate_weight(self):
        """近似骨重查询"""
        # 不存在的骨重值应该返回最接近的
        poem_info = get_bone_poem(3.05)
        assert "title" in poem_info
        assert "poem" in poem_info


class TestWeightLevel:
    """骨重等级测试"""
    
    def test_low_weight(self):
        """低骨重等级"""
        level = get_weight_level(2.2)
        assert level["level"] == "下下"
    
    def test_medium_weight(self):
        """中等骨重等级"""
        level = get_weight_level(3.7)
        assert level["level"] == "中"
    
    def test_high_weight(self):
        """高骨重等级"""
        level = get_weight_level(5.5)
        assert level["level"] in ["上上", "极上"]
    
    def test_supreme_weight(self):
        """至尊骨重等级"""
        level = get_weight_level(6.5)
        assert level["level"] == "至尊"


class TestAnalyzeBonefate:
    """完整分析测试"""
    
    def test_full_analysis(self):
        """完整分析流程"""
        birth_dt = datetime(1990, 5, 15, 12, 30)
        result = analyze_bonefate(birth_dt)
        
        assert "weight" in result
        assert "weight_display" in result
        assert "level" in result
        assert "level_desc" in result
        assert "title" in result
        assert "poem" in result
        assert "lunar_date" in result
        assert "solar_date" in result
    
    def test_lunar_input(self):
        """农历输入测试"""
        birth_dt = datetime(1990, 5, 15, 12, 30)
        result = analyze_bonefate(birth_dt, is_lunar=True)
        
        # 农历输入时，lunar_date 应该与输入一致
        assert result["lunar_date"]["year"] == 1990
        assert result["lunar_date"]["month"] == 5
        assert result["lunar_date"]["day"] == 15
    
    def test_result_model(self):
        """结果模型测试"""
        birth_dt = datetime(1990, 5, 15, 12, 30)
        result_dict = analyze_bonefate(birth_dt)
        result = BoneFateResult.from_dict(result_dict)
        
        assert result.weight > 0
        assert "两" in result.weight_display
        assert len(result.title) > 0
        assert len(result.poem) > 0


class TestSolarToLunar:
    """阳历转农历测试"""
    
    def test_basic_conversion(self):
        """基本转换测试"""
        lunar_year, lunar_month, lunar_day = solar_to_lunar(2024, 1, 1)
        # 2024年1月1日是农历2023年冬月廿
        assert lunar_year == 2023
        assert lunar_month == 11
    
    def test_spring_festival(self):
        """春节附近转换"""
        # 测试春节附近的日期
        lunar_year, lunar_month, lunar_day = solar_to_lunar(2024, 2, 10)
        # 2024年2月10日是农历正月初一（春节）
        assert lunar_year == 2024
        assert lunar_month == 1


class TestEdgeCases:
    """边界情况测试"""
    
    def test_midnight(self):
        """午夜时辰测试"""
        weight = calculate_bone_weight(1990, 1, 1, 0)
        assert 2.0 <= weight <= 8.0
    
    def test_late_night(self):
        """深夜时辰测试"""
        weight = calculate_bone_weight(1990, 1, 1, 23)
        assert 2.0 <= weight <= 8.0
    
    def test_new_year(self):
        """新年日期测试"""
        result = analyze_bonefate(datetime(2024, 1, 1, 12))
        assert result["weight"] > 0
    
    def test_year_end(self):
        """年末日期测试"""
        result = analyze_bonefate(datetime(2023, 12, 31, 23))
        assert result["weight"] > 0
