"""择日功能测试"""
import pytest
from datetime import datetime, date, timedelta
from src.core import calculate_bazi, analyze_wuxing, select_dates
from src.core.analysis.date_selection import (
    _get_clash_zodiac, _calculate_day_score, _get_suitable_avoid
)
from src.models.bazi_models import Gender
from src.models.date_selection_models import (
    EventType, DayQuality, DayInfo, DateRecommendation
)


class TestGetClashZodiac:
    """冲生肖测试"""
    
    @pytest.mark.parametrize("dizhi,expected", [
        ("子", "马"),  # 子午冲
        ("午", "鼠"),
        ("丑", "羊"),  # 丑未冲
        ("寅", "猴"),  # 寅申冲
        ("卯", "鸡"),  # 卯酉冲
        ("辰", "狗"),  # 辰戌冲
        ("巳", "猪"),  # 巳亥冲
    ])
    def test_get_clash_zodiac_known(self, dizhi, expected):
        """应返回正确的冲生肖"""
        result = _get_clash_zodiac(dizhi)
        assert result == expected


class TestCalculateDayScore:
    """日期得分计算测试"""
    
    def test_calculate_day_score_returns_tuple(self, sample_wuxing):
        """应返回得分和质量元组"""
        result = _calculate_day_score("甲子", sample_wuxing, EventType.WEDDING)
        assert isinstance(result, tuple)
        assert len(result) == 2
    
    def test_calculate_day_score_range(self, sample_wuxing):
        """得分应在有效范围内"""
        score, quality = _calculate_day_score("甲子", sample_wuxing, EventType.WEDDING)
        assert 20 <= score <= 95
        assert isinstance(quality, DayQuality)
    
    @pytest.mark.parametrize("event", list(EventType))
    def test_calculate_day_score_all_events(self, sample_wuxing, event):
        """应支持所有事件类型"""
        score, quality = _calculate_day_score("甲子", sample_wuxing, event)
        assert score >= 0


class TestGetSuitableAvoid:
    """宜忌事项测试"""
    
    def test_get_suitable_avoid_returns_lists(self):
        """应返回两个列表"""
        suitable, avoid = _get_suitable_avoid(EventType.WEDDING, DayQuality.GOOD)
        assert isinstance(suitable, list)
        assert isinstance(avoid, list)
    
    def test_get_suitable_avoid_good_day(self):
        """吉日应有更多宜事项"""
        suitable_good, _ = _get_suitable_avoid(EventType.WEDDING, DayQuality.GOOD)
        suitable_bad, _ = _get_suitable_avoid(EventType.WEDDING, DayQuality.BAD)
        assert len(suitable_good) >= len(suitable_bad)


class TestSelectDates:
    """择日功能测试"""
    
    def test_select_dates_returns_recommendation(self, sample_male_bazi, sample_wuxing):
        """应返回 DateRecommendation"""
        result = select_dates(
            sample_male_bazi, sample_wuxing,
            EventType.WEDDING, date.today(), 30
        )
        assert isinstance(result, DateRecommendation)
    
    def test_select_dates_has_recommendations(self, sample_male_bazi, sample_wuxing):
        """应有推荐日期列表"""
        result = select_dates(
            sample_male_bazi, sample_wuxing,
            EventType.WEDDING, date.today(), 60
        )
        # 60天内应该有一些推荐
        assert hasattr(result, 'recommended_dates')
        assert hasattr(result, 'avoid_dates')
    
    def test_select_dates_summary(self, sample_male_bazi, sample_wuxing):
        """应有总结信息"""
        result = select_dates(
            sample_male_bazi, sample_wuxing,
            EventType.WEDDING, date.today(), 30
        )
        assert result.summary != ""
    
    @pytest.mark.parametrize("event", list(EventType))
    def test_select_dates_all_events(self, sample_male_bazi, sample_wuxing, event):
        """应支持所有事件类型"""
        result = select_dates(
            sample_male_bazi, sample_wuxing,
            event, date.today(), 30
        )
        assert result.event_type == event
    
    def test_select_dates_day_info_complete(self, sample_male_bazi, sample_wuxing):
        """DayInfo 应包含完整信息"""
        result = select_dates(
            sample_male_bazi, sample_wuxing,
            EventType.WEDDING, date.today(), 60
        )
        if result.recommended_dates:
            day = result.recommended_dates[0]
            assert day.date is not None
            assert day.ganzhi is not None
            assert day.quality is not None
            assert day.suitable is not None
            assert day.avoid is not None
    
    def test_select_dates_to_json(self, sample_male_bazi, sample_wuxing):
        """应能序列化为 JSON"""
        result = select_dates(
            sample_male_bazi, sample_wuxing,
            EventType.WEDDING, date.today(), 30
        )
        json_str = result.to_json()
        assert isinstance(json_str, str)
        assert "event_type" in json_str
