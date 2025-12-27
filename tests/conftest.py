"""Pytest 配置和共享 fixtures"""
import pytest
from datetime import datetime
from src.models.bazi_models import Gender, BaziChart
from src.core import calculate_bazi, analyze_wuxing


@pytest.fixture
def sample_birth_datetime():
    """示例出生时间：1990年1月15日 8:30"""
    return datetime(1990, 1, 15, 8, 30)


@pytest.fixture
def sample_male_bazi(sample_birth_datetime):
    """示例男性八字"""
    return calculate_bazi(sample_birth_datetime, Gender.MALE)


@pytest.fixture
def sample_female_bazi():
    """示例女性八字：1992年6月20日 14:00"""
    return calculate_bazi(datetime(1992, 6, 20, 14, 0), Gender.FEMALE)


@pytest.fixture
def sample_wuxing(sample_male_bazi):
    """示例五行分析"""
    return analyze_wuxing(sample_male_bazi)


@pytest.fixture
def known_bazi_cases():
    """已知八字案例（用于验证计算准确性）"""
    return [
        # (出生时间, 期望年柱, 期望月柱, 期望日柱, 期望时柱)
        (datetime(1984, 2, 4, 12, 0), "甲子", "丙寅", "甲子", "庚午"),  # 立春后
        (datetime(1984, 2, 3, 12, 0), "癸亥", "乙丑", "癸亥", "戊午"),  # 立春前
        (datetime(2000, 1, 1, 0, 0), "己卯", "丙子", "戊戌", "壬子"),
        (datetime(2024, 12, 25, 18, 0), "甲辰", "丙子", "甲午", "癸酉"),
    ]
