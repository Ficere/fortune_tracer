"""配对分析测试"""
import pytest
from datetime import datetime
from src.core import calculate_bazi, analyze_wuxing, calculate_compatibility
from src.core.analysis.compatibility import (
    _check_pair, _analyze_wuxing_compat,
    _analyze_ganzhi_relations, _calculate_score, _get_grade
)
from src.models.bazi_models import Gender
from src.models.compatibility_models import (
    WuxingCompatibility, GanZhiRelations, CompatibilityResult
)


class TestCheckPair:
    """配对检查测试"""
    
    def test_check_pair_found(self):
        """应找到存在的配对"""
        pairs = {("甲", "己"): "中正之合"}
        result = _check_pair(pairs, "甲", "己")
        assert result is not None
        assert result[1] == "中正之合"
    
    def test_check_pair_reverse_order(self):
        """应支持反向查找"""
        pairs = {("甲", "己"): "中正之合"}
        result = _check_pair(pairs, "己", "甲")
        assert result is not None
    
    def test_check_pair_not_found(self):
        """不存在的配对应返回 None"""
        pairs = {("甲", "己"): "中正之合"}
        result = _check_pair(pairs, "甲", "乙")
        assert result is None


class TestAnalyzeWuxingCompat:
    """五行互补分析测试"""
    
    def test_analyze_wuxing_compat_returns_result(self, sample_wuxing):
        """应返回 WuxingCompatibility"""
        result = _analyze_wuxing_compat(sample_wuxing, sample_wuxing)
        assert isinstance(result, WuxingCompatibility)
    
    def test_analyze_wuxing_compat_balance_score(self, sample_wuxing):
        """平衡分应在有效范围内"""
        bazi2 = calculate_bazi(datetime(1992, 6, 20, 14), Gender.FEMALE)
        wuxing2 = analyze_wuxing(bazi2)
        result = _analyze_wuxing_compat(sample_wuxing, wuxing2)
        assert 0 <= result.balance_score <= 100


class TestAnalyzeGanzhiRelations:
    """干支关系分析测试"""
    
    def test_analyze_ganzhi_returns_relations(self, sample_male_bazi, sample_female_bazi):
        """应返回 GanZhiRelations"""
        result = _analyze_ganzhi_relations(sample_male_bazi, sample_female_bazi)
        assert isinstance(result, GanZhiRelations)
    
    def test_analyze_ganzhi_has_lists(self, sample_male_bazi, sample_female_bazi):
        """应包含所有关系列表"""
        result = _analyze_ganzhi_relations(sample_male_bazi, sample_female_bazi)
        assert hasattr(result, 'tiangan_he')
        assert hasattr(result, 'tiangan_chong')
        assert hasattr(result, 'dizhi_he')
        assert hasattr(result, 'dizhi_chong')
        assert hasattr(result, 'dizhi_xing')


class TestCalculateScore:
    """配对得分计算测试"""
    
    def test_calculate_score_range(self, sample_male_bazi, sample_female_bazi, sample_wuxing):
        """得分应在有效范围内"""
        wuxing2 = analyze_wuxing(sample_female_bazi)
        wuxing_compat = _analyze_wuxing_compat(sample_wuxing, wuxing2)
        ganzhi = _analyze_ganzhi_relations(sample_male_bazi, sample_female_bazi)
        score = _calculate_score(wuxing_compat, ganzhi)
        assert 20 <= score <= 98


class TestGetGrade:
    """评级测试"""
    
    @pytest.mark.parametrize("score,expected_contains", [
        (95, "天作之合"),
        (85, "良缘佳配"),
        (75, "和谐美满"),
        (65, "相互包容"),
        (55, "需要磨合"),
        (40, "挑战较多"),
    ])
    def test_get_grade_levels(self, score, expected_contains):
        """应返回正确的评级"""
        grade = _get_grade(score)
        assert expected_contains in grade


class TestCalculateCompatibility:
    """完整配对计算测试"""
    
    def test_calculate_compatibility_returns_result(
        self, sample_male_bazi, sample_female_bazi, sample_wuxing
    ):
        """应返回 CompatibilityResult"""
        wuxing2 = analyze_wuxing(sample_female_bazi)
        result = calculate_compatibility(
            sample_male_bazi, sample_female_bazi,
            sample_wuxing, wuxing2
        )
        assert isinstance(result, CompatibilityResult)
    
    def test_calculate_compatibility_has_advice(
        self, sample_male_bazi, sample_female_bazi, sample_wuxing
    ):
        """应包含配对建议"""
        wuxing2 = analyze_wuxing(sample_female_bazi)
        result = calculate_compatibility(
            sample_male_bazi, sample_female_bazi,
            sample_wuxing, wuxing2
        )
        assert result.advice is not None
        assert len(result.advice.strengths) > 0
        assert len(result.advice.suggestions) > 0
    
    def test_calculate_compatibility_to_json(
        self, sample_male_bazi, sample_female_bazi, sample_wuxing
    ):
        """应能序列化为 JSON"""
        wuxing2 = analyze_wuxing(sample_female_bazi)
        result = calculate_compatibility(
            sample_male_bazi, sample_female_bazi,
            sample_wuxing, wuxing2
        )
        json_str = result.to_json()
        assert isinstance(json_str, str)
        assert "total_score" in json_str
