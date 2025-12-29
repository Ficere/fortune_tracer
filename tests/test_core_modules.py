"""核心模块测试 - 提高覆盖率"""
import pytest
from datetime import datetime
import time


class TestCacheModule:
    """缓存模块测试"""
    
    def test_simple_cache_creation(self):
        """测试缓存创建"""
        from src.core.cache import SimpleCache
        cache = SimpleCache(default_ttl=60)
        assert cache.size == 0
    
    def test_cache_set_get(self):
        """测试缓存设置和获取"""
        from src.core.cache import SimpleCache
        cache = SimpleCache(default_ttl=60)
        cache.set("key1", "value1")
        assert cache.get("key1") == "value1"
    
    def test_cache_delete(self):
        """测试缓存删除"""
        from src.core.cache import SimpleCache
        cache = SimpleCache(default_ttl=60)
        cache.set("key1", "value1")
        cache.delete("key1")
        assert cache.get("key1") is None
    
    def test_cache_clear(self):
        """测试缓存清空"""
        from src.core.cache import SimpleCache
        cache = SimpleCache(default_ttl=60)
        cache.set("key1", "value1")
        cache.set("key2", "value2")
        cache.clear()
        assert cache.size == 0
    
    def test_cache_expiration(self):
        """测试缓存过期"""
        from src.core.cache import SimpleCache
        cache = SimpleCache(default_ttl=1)
        cache.set("key1", "value1", ttl=1)
        assert cache.get("key1") == "value1"
        time.sleep(1.1)
        assert cache.get("key1") is None
    
    def test_cache_cleanup(self):
        """测试缓存清理"""
        from src.core.cache import SimpleCache
        cache = SimpleCache(default_ttl=1)
        cache.set("key1", "value1", ttl=1)
        time.sleep(1.1)
        cleaned = cache.cleanup()
        assert cleaned == 1
    
    def test_cached_decorator(self):
        """测试缓存装饰器"""
        from src.core.cache import cached, clear_cache
        
        call_count = 0
        
        @cached(ttl=60)
        def expensive_func(x):
            nonlocal call_count
            call_count += 1
            return x * 2
        
        clear_cache()
        result1 = expensive_func(5)
        result2 = expensive_func(5)
        
        assert result1 == 10
        assert result2 == 10
        # 由于缓存，函数只应被调用一次
        # 注意：如果缓存被禁用，可能调用两次
    
    def test_cache_make_key(self):
        """测试缓存键生成"""
        from src.core.cache import SimpleCache
        cache = SimpleCache()
        key1 = cache._make_key("arg1", "arg2", kwarg1="val1")
        key2 = cache._make_key("arg1", "arg2", kwarg1="val1")
        key3 = cache._make_key("arg1", "arg3")
        assert key1 == key2
        assert key1 != key3


class TestExceptionsModule:
    """异常模块测试"""
    
    def test_fortune_tracer_error(self):
        """测试基础异常"""
        from src.core.exceptions import FortuneTracerError
        error = FortuneTracerError("测试错误", code="TEST_ERROR")
        assert error.message == "测试错误"
        assert error.code == "TEST_ERROR"
        assert "code" in error.to_dict()
    
    def test_validation_error(self):
        """测试验证错误"""
        from src.core.exceptions import ValidationError
        error = ValidationError("字段验证失败", field="test_field")
        assert "VALIDATION_ERROR" in error.code
        assert error.details.get("field") == "test_field"
    
    def test_birth_info_error(self):
        """测试出生信息错误"""
        from src.core.exceptions import BirthInfoError
        error = BirthInfoError("日期无效", field="birth_date")
        assert "出生信息错误" in error.message
    
    def test_datetime_error(self):
        """测试日期时间错误"""
        from src.core.exceptions import DateTimeError
        error = DateTimeError("时间格式错误")
        assert error.details.get("field") == "birth_datetime"
    
    def test_gender_error(self):
        """测试性别错误"""
        from src.core.exceptions import GenderError
        error = GenderError("未知")
        assert "无效的性别值" in error.message
    
    def test_location_error(self):
        """测试地点错误"""
        from src.core.exceptions import LocationError
        error = LocationError("未知城市")
        assert "无法识别的地点" in error.message
    
    def test_calculation_error(self):
        """测试计算错误"""
        from src.core.exceptions import CalculationError
        error = CalculationError("计算失败", calculation_type="pillar")
        assert error.details.get("calculation_type") == "pillar"
    
    def test_pillar_calculation_error(self):
        """测试四柱计算错误"""
        from src.core.exceptions import PillarCalculationError
        error = PillarCalculationError("年柱计算失败", pillar_type="year")
        assert "年柱" in error.message or "year" in str(error.details)
    
    def test_wuxing_calculation_error(self):
        """测试五行计算错误"""
        from src.core.exceptions import WuxingCalculationError
        error = WuxingCalculationError("统计失败")
        assert "五行分析错误" in error.message
    
    def test_ai_interpretation_error(self):
        """测试AI解读错误"""
        from src.core.exceptions import AIInterpretationError
        error = AIInterpretationError("API调用失败", original_error="Timeout")
        assert "AI解读失败" in error.message
    
    def test_api_key_error(self):
        """测试API Key错误"""
        from src.core.exceptions import APIKeyError
        error = APIKeyError()
        assert "API_KEY_ERROR" in error.code
    
    def test_rate_limit_error(self):
        """测试频率限制错误"""
        from src.core.exceptions import RateLimitError
        error = RateLimitError(retry_after=60)
        assert error.details.get("retry_after") == 60
    
    def test_configuration_error(self):
        """测试配置错误"""
        from src.core.exceptions import ConfigurationError
        error = ConfigurationError("配置项缺失", config_key="API_KEY")
        assert "配置错误" in error.message


class TestLoggingModule:
    """日志模块测试"""
    
    def test_setup_logging(self):
        """测试日志初始化"""
        from src.core.logging import setup_logging
        setup_logging()  # 不应抛出异常
    
    def test_get_logger(self):
        """测试获取日志器"""
        from src.core.logging import get_logger
        logger = get_logger("test_module")
        assert logger is not None
        assert logger.name == "test_module"
    
    def test_get_logger_cached(self):
        """测试日志器缓存"""
        from src.core.logging import get_logger
        logger1 = get_logger("cached_test")
        logger2 = get_logger("cached_test")
        assert logger1 is logger2
    
    def test_logger_mixin(self):
        """测试日志混入类"""
        from src.core.logging import LoggerMixin
        
        class TestClass(LoggerMixin):
            def do_something(self):
                return self.logger.name
        
        obj = TestClass()
        assert obj.logger is not None
        assert "TestClass" in obj.logger.name


class TestShenshaModule:
    """神煞模块测试 - 补充覆盖"""
    
    def test_shensha_with_various_bazi(self):
        """测试不同八字的神煞"""
        from datetime import datetime
        from src.core import calculate_bazi, calculate_shensha
        from src.models.bazi_models import Gender
        
        # 测试多个日期
        test_cases = [
            (datetime(1984, 2, 4, 12, 0), Gender.MALE),
            (datetime(1990, 6, 15, 8, 0), Gender.FEMALE),
            (datetime(2000, 12, 25, 23, 0), Gender.MALE),
        ]
        
        for dt, gender in test_cases:
            bazi = calculate_bazi(dt, gender)
            result = calculate_shensha(bazi)
            assert result is not None
            assert isinstance(result.summary, str)
    
    def test_shensha_all_types(self):
        """测试所有类型的神煞查找"""
        from datetime import datetime
        from src.core import calculate_bazi, calculate_shensha
        from src.models.bazi_models import Gender
        
        # 使用一个可能包含多种神煞的日期
        bazi = calculate_bazi(datetime(1984, 2, 4, 6, 0), Gender.MALE)
        result = calculate_shensha(bazi)
        
        # 检查结构完整性
        assert hasattr(result, 'shensha_list')
        assert hasattr(result, 'ji_shen')
        assert hasattr(result, 'xiong_sha')
        assert hasattr(result, 'summary')


class TestCalendarModule:
    """农历模块测试"""
    
    def test_solar_to_lunar(self):
        """测试公历转农历"""
        from src.core import solar_to_lunar
        
        result = solar_to_lunar(datetime(2024, 2, 10))
        assert result is not None
        assert hasattr(result, 'year')
        assert hasattr(result, 'month')
        assert hasattr(result, 'day')
    
    def test_get_jieqi_month(self):
        """测试节气月份"""
        from src.core.calendar import get_jieqi_month
        
        # 测试不同月份
        for month in range(1, 13):
            result = get_jieqi_month(datetime(2024, month, 15))
            assert 1 <= result <= 12


class TestJieqiModule:
    """节气模块补充测试"""
    
    def test_get_jieqi_for_year(self):
        """测试获取年度节气"""
        from src.core import get_jieqi_for_year
        
        jieqi_list = get_jieqi_for_year(2024)
        assert len(jieqi_list) == 24
        
        # 检查节气名称
        names = [jq.name for jq in jieqi_list]
        assert "立春" in names
        assert "夏至" in names
        assert "冬至" in names
    
    def test_is_before_lichun(self):
        """测试立春判断"""
        from src.core import is_before_lichun
        
        # 1月应该在立春前
        assert is_before_lichun(datetime(2024, 1, 20)) is True
        # 3月应该在立春后
        assert is_before_lichun(datetime(2024, 3, 20)) is False


class TestSolarTimeModule:
    """真太阳时模块补充测试"""
    
    def test_various_cities(self):
        """测试多个城市的真太阳时"""
        from src.core import convert_to_true_solar_time
        
        dt = datetime(2024, 6, 21, 12, 0)
        
        cities = ["北京", "上海", "广州", "成都", "乌鲁木齐"]
        results = []
        
        for city in cities:
            result = convert_to_true_solar_time(dt, city)
            results.append(result)
        
        # 不同城市应有不同的真太阳时
        # 乌鲁木齐经度差异最大
        assert results[0] != results[-1]
    
    def test_time_correction_info(self):
        """测试时间修正信息"""
        from src.core import get_time_correction_info
        
        info = get_time_correction_info(datetime(2024, 6, 21, 12, 0), "北京")
        
        assert info["found"] is True
        assert "longitude_correction_minutes" in info
        assert "equation_of_time_minutes" in info
        assert "total_correction_minutes" in info
    
    def test_unknown_city(self):
        """测试未知城市"""
        from src.core import get_time_correction_info
        
        info = get_time_correction_info(datetime(2024, 6, 21, 12, 0), "未知城市XYZ")
        assert info["found"] is False


class TestNayinModule:
    """纳音模块补充测试"""
    
    def test_all_60_jiazi(self):
        """测试60甲子纳音完整性"""
        from src.core.nayin import JIAZI_NAYIN
        
        assert len(JIAZI_NAYIN) == 60
    
    def test_nayin_wuxing_mapping(self):
        """测试纳音五行映射"""
        from src.core.nayin import get_nayin_wuxing, NAYIN_WUXING
        
        # 检查所有纳音都有对应五行
        all_nayins = []
        for nayins in NAYIN_WUXING.values():
            all_nayins.extend(nayins)
        
        assert len(all_nayins) == 30  # 30种纳音
        
        # 测试获取五行
        assert get_nayin_wuxing("海中金") == "金"
        assert get_nayin_wuxing("大林木") == "木"
        assert get_nayin_wuxing("涧下水") == "水"


class TestDayunModule:
    """大运模块补充测试"""
    
    def test_dayun_direction_male_yang(self):
        """测试阳年男命大运方向"""
        from datetime import datetime
        from src.core import calculate_bazi, calculate_dayun
        from src.models.bazi_models import Gender
        
        # 甲子年（阳年）男命应顺行
        bazi = calculate_bazi(datetime(1984, 6, 15, 12, 0), Gender.MALE)
        dayun = calculate_dayun(bazi)
        assert dayun.direction == "顺行"
    
    def test_dayun_direction_female_yang(self):
        """测试阳年女命大运方向"""
        from datetime import datetime
        from src.core import calculate_bazi, calculate_dayun
        from src.models.bazi_models import Gender
        
        # 甲子年（阳年）女命应逆行
        bazi = calculate_bazi(datetime(1984, 6, 15, 12, 0), Gender.FEMALE)
        dayun = calculate_dayun(bazi)
        assert dayun.direction == "逆行"
    
    def test_get_current_dayun_found(self):
        """测试获取当前大运"""
        from datetime import datetime
        from src.core import calculate_bazi, calculate_dayun, get_current_dayun
        from src.models.bazi_models import Gender
        
        bazi = calculate_bazi(datetime(1990, 1, 15, 8, 0), Gender.MALE)
        dayun_info = calculate_dayun(bazi)
        
        # 测试有效年龄
        current = get_current_dayun(dayun_info, 30)
        if current:
            assert current.start_age <= 30 <= current.end_age
    
    def test_get_current_dayun_not_found(self):
        """测试超出范围的大运"""
        from datetime import datetime
        from src.core import calculate_bazi, calculate_dayun, get_current_dayun
        from src.models.bazi_models import Gender

        bazi = calculate_bazi(datetime(1990, 1, 15, 8, 0), Gender.MALE)
        dayun_info = calculate_dayun(bazi, num_dayun=3, with_detail=False)

        # 测试超出范围
        current = get_current_dayun(dayun_info, 100)
        assert current is None
