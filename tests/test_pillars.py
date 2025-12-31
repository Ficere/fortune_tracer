"""四柱计算测试"""
import pytest
from datetime import datetime
from src.core import calculate_bazi
from src.core.bazi.pillars import (
    _get_year_pillar, _get_month_pillar,
    _get_day_pillar, _get_hour_pillar
)
from src.models.bazi_models import Gender


class TestYearPillar:
    """年柱计算测试"""
    
    def test_year_pillar_after_lichun(self):
        """立春后应使用当年年柱"""
        pillar = _get_year_pillar(1984, 2, 5)
        assert pillar.display == "甲子"
    
    def test_year_pillar_before_lichun(self):
        """立春前应使用上一年年柱"""
        pillar = _get_year_pillar(1984, 2, 3)
        assert pillar.display == "癸亥"
    
    def test_year_pillar_cycle(self):
        """测试60年甲子循环"""
        pillar_1984 = _get_year_pillar(1984, 6, 1)
        pillar_2044 = _get_year_pillar(2044, 6, 1)
        assert pillar_1984.display == pillar_2044.display == "甲子"
    
    @pytest.mark.parametrize("year,expected", [
        (1984, "甲子"),
        (1985, "乙丑"),
        (1990, "庚午"),
        (2000, "庚辰"),
        (2024, "甲辰"),
    ])
    def test_year_pillar_known_years(self, year, expected):
        """测试已知年份的年柱"""
        pillar = _get_year_pillar(year, 6, 1)  # 年中避免立春问题
        assert pillar.display == expected


class TestMonthPillar:
    """月柱计算测试"""
    
    def test_month_pillar_basic(self):
        """基本月柱计算"""
        pillar = _get_month_pillar("甲", 3, 15)
        assert pillar.tiangan.value in "甲乙丙丁戊己庚辛壬癸"
        assert pillar.dizhi.value in "子丑寅卯辰巳午未申酉戌亥"
    
    def test_month_pillar_consistency(self):
        """同一月份的月柱应一致"""
        pillar1 = _get_month_pillar("甲", 6, 10)
        pillar2 = _get_month_pillar("甲", 6, 20)
        assert pillar1.display == pillar2.display


class TestDayPillar:
    """日柱计算测试"""
    
    def test_day_pillar_basic(self):
        """基本日柱计算"""
        pillar = _get_day_pillar(datetime(1990, 1, 15))
        assert len(pillar.display) == 2
    
    def test_day_pillar_consecutive_days(self):
        """连续日期的日柱应不同"""
        pillar1 = _get_day_pillar(datetime(2024, 1, 1))
        pillar2 = _get_day_pillar(datetime(2024, 1, 2))
        assert pillar1.display != pillar2.display
    
    def test_day_pillar_60_day_cycle(self):
        """60天循环后日柱应相同"""
        pillar1 = _get_day_pillar(datetime(2024, 1, 1))
        pillar2 = _get_day_pillar(datetime(2024, 3, 1))  # 60天后
        assert pillar1.display == pillar2.display


class TestHourPillar:
    """时柱计算测试"""
    
    @pytest.mark.parametrize("hour,expected_zhi", [
        (0, "子"),    # 23:00-00:59 为子时
        (1, "丑"),    # 01:00-02:59 为丑时
        (3, "寅"),    # 03:00-04:59 为寅时
        (5, "卯"),    # 05:00-06:59 为卯时
        (7, "辰"),    # 07:00-08:59 为辰时
        (9, "巳"),    # 09:00-10:59 为巳时
        (11, "午"),   # 11:00-12:59 为午时
        (13, "未"),   # 13:00-14:59 为未时
        (15, "申"),   # 15:00-16:59 为申时
        (17, "酉"),   # 17:00-18:59 为酉时
        (19, "戌"),   # 19:00-20:59 为戌时
        (21, "亥"),   # 21:00-22:59 为亥时
        (23, "子"),   # 23:00-23:59 为子时
    ])
    def test_hour_pillar_dizhi(self, hour, expected_zhi):
        """测试时柱地支对应"""
        pillar = _get_hour_pillar("甲", hour)
        assert pillar.dizhi.value == expected_zhi


class TestCalculateBazi:
    """完整八字计算测试"""
    
    def test_calculate_bazi_returns_chart(self, sample_birth_datetime):
        """应返回完整的 BaziChart"""
        bazi = calculate_bazi(sample_birth_datetime, Gender.MALE)
        assert bazi.year_pillar is not None
        assert bazi.month_pillar is not None
        assert bazi.day_pillar is not None
        assert bazi.hour_pillar is not None
    
    def test_calculate_bazi_with_place(self, sample_birth_datetime):
        """应支持出生地点参数"""
        bazi = calculate_bazi(sample_birth_datetime, Gender.MALE, "北京")
        assert bazi.birth_place == "北京"
    
    def test_calculate_bazi_gender(self, sample_birth_datetime):
        """应正确记录性别"""
        male_bazi = calculate_bazi(sample_birth_datetime, Gender.MALE)
        female_bazi = calculate_bazi(sample_birth_datetime, Gender.FEMALE)
        assert male_bazi.gender == Gender.MALE
        assert female_bazi.gender == Gender.FEMALE
    
    def test_calculate_bazi_datetime_stored(self, sample_birth_datetime):
        """应正确存储出生时间"""
        bazi = calculate_bazi(sample_birth_datetime, Gender.MALE)
        assert bazi.birth_datetime == sample_birth_datetime
