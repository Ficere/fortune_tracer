"""AI模块单元测试"""
import os
import pytest
from unittest.mock import patch, MagicMock

from src.ai.config import AIConfig, get_ai_config, reset_ai_config
from src.ai.serializer import serialize_bazi_for_ai, serialize_for_prompt
from src.ai.prompts import SYSTEM_PROMPT, build_analysis_prompt
from src.ai.interpreter import interpret_bazi


class TestAIConfig:
    """AI配置测试"""
    
    def setup_method(self):
        reset_ai_config()
    
    def test_default_config(self):
        """测试默认配置"""
        config = AIConfig()
        assert config.model == "gpt-4o-mini"
        assert config.timeout == 30
        assert config.enabled is True
        assert config.is_valid() is False  # 无API Key
    
    def test_config_with_api_key(self):
        """测试设置API Key"""
        config = AIConfig(api_key="test-key")
        assert config.is_valid() is True
    
    def test_with_api_key_method(self):
        """测试with_api_key方法"""
        config = AIConfig(model="gpt-4o", temperature=0.5)
        new_config = config.with_api_key("new-key")
        assert new_config.api_key == "new-key"
        assert new_config.model == "gpt-4o"
        assert new_config.temperature == 0.5
    
    @patch.dict(os.environ, {
        "OPENAI_API_KEY": "env-key",
        "AI_MODEL": "gpt-4o",
        "AI_TIMEOUT": "60"
    })
    def test_from_env(self):
        """测试从环境变量加载配置"""
        config = AIConfig.from_env()
        assert config.api_key == "env-key"
        assert config.model == "gpt-4o"
        assert config.timeout == 60


class TestSerializer:
    """序列化器测试"""
    
    def test_serialize_bazi(self, sample_male_bazi, sample_wuxing):
        """测试八字序列化"""
        data = serialize_bazi_for_ai(sample_male_bazi, sample_wuxing)
        
        assert "basic_info" in data
        assert "pillars" in data
        assert "wuxing_analysis" in data
        
        # 验证基本信息
        assert data["basic_info"]["gender"] == "男"
        
        # 验证四柱
        assert "年柱" in data["pillars"]
        assert "日柱" in data["pillars"]
        
        # 验证五行分析
        assert "day_master" in data["wuxing_analysis"]
        assert "favorable" in data["wuxing_analysis"]
    
    def test_serialize_for_prompt(self, sample_male_bazi, sample_wuxing):
        """测试序列化为提示词格式"""
        data = serialize_bazi_for_ai(sample_male_bazi, sample_wuxing)
        json_str = serialize_for_prompt(data)
        
        assert isinstance(json_str, str)
        assert "basic_info" in json_str
        assert "wuxing_analysis" in json_str


class TestPrompts:
    """提示词测试"""
    
    def test_system_prompt_exists(self):
        """测试系统提示词存在"""
        assert SYSTEM_PROMPT is not None
        assert "命理" in SYSTEM_PROMPT
    
    def test_build_analysis_prompt(self):
        """测试构建分析提示词"""
        test_json = '{"test": "data"}'
        prompt = build_analysis_prompt(test_json)
        
        assert test_json in prompt
        assert "性格" in prompt
        assert "事业" in prompt
        assert "JSON" in prompt


class TestInterpreter:
    """解读器测试"""
    
    def test_default_interpretation(self, sample_male_bazi, sample_wuxing):
        """测试默认解读（无API Key）"""
        result = interpret_bazi(sample_male_bazi, sample_wuxing)
        
        assert result.personality is not None
        assert result.career is not None
        assert result.summary is not None
    
    @patch("src.ai.interpreter.OpenAI")
    def test_ai_interpretation_success(
        self, mock_openai, sample_male_bazi, sample_wuxing
    ):
        """测试AI解读成功"""
        # Mock OpenAI响应
        mock_response = MagicMock()
        mock_response.choices[0].message.content = '''
        {
            "personality": "测试性格",
            "career": "测试事业",
            "love": "测试感情",
            "health": "测试健康",
            "wealth": "测试财运",
            "summary": "测试总结"
        }
        '''
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        result = interpret_bazi(
            sample_male_bazi, sample_wuxing, api_key="test-key"
        )
        
        assert result.personality == "测试性格"
        assert result.summary == "测试总结"
    
    @patch("src.ai.interpreter.OpenAI")
    def test_ai_interpretation_fallback(
        self, mock_openai, sample_male_bazi, sample_wuxing
    ):
        """测试AI调用失败时回退到默认解读"""
        mock_openai.side_effect = Exception("API Error")
        
        result = interpret_bazi(
            sample_male_bazi, sample_wuxing, api_key="test-key"
        )
        
        # 应该返回默认解读而不是抛出异常
        assert result.personality is not None

