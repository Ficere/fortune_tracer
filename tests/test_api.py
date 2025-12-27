"""API 端点测试"""
import pytest
from fastapi.testclient import TestClient
from datetime import datetime, date
from backend.main import app


@pytest.fixture
def client():
    """创建测试客户端"""
    return TestClient(app)


class TestHealthEndpoint:
    """健康检查端点测试"""
    
    def test_health_check(self, client):
        """健康检查应返回 healthy"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
    
    def test_root_endpoint(self, client):
        """根路径应返回 API 信息"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "name" in data
        assert "version" in data


class TestBaziEndpoint:
    """八字分析 API 测试"""
    
    def test_bazi_analyze_success(self, client):
        """八字分析应成功"""
        response = client.post("/api/bazi/analyze", json={
            "birth_info": {
                "birth_datetime": "1990-01-15T08:30:00",
                "gender": "男",
                "birth_place": "北京"
            }
        })
        assert response.status_code == 200
        data = response.json()
        assert "bazi" in data
        assert "wuxing" in data
    
    def test_bazi_analyze_female(self, client):
        """女性八字分析"""
        response = client.post("/api/bazi/analyze", json={
            "birth_info": {
                "birth_datetime": "1992-06-20T14:00:00",
                "gender": "女"
            }
        })
        assert response.status_code == 200
    
    def test_bazi_analyze_without_place(self, client):
        """无出生地点也应成功"""
        response = client.post("/api/bazi/analyze", json={
            "birth_info": {
                "birth_datetime": "1985-03-08T06:00:00",
                "gender": "男"
            }
        })
        assert response.status_code == 200
    
    def test_bazi_analyze_invalid_gender(self, client):
        """无效性别应返回错误"""
        response = client.post("/api/bazi/analyze", json={
            "birth_info": {
                "birth_datetime": "1990-01-15T08:30:00",
                "gender": "未知"
            }
        })
        assert response.status_code == 422  # Validation error
    
    def test_bazi_analyze_with_api_key(self, client):
        """支持 API Key 参数"""
        response = client.post("/api/bazi/analyze", json={
            "birth_info": {
                "birth_datetime": "1990-01-15T08:30:00",
                "gender": "男"
            },
            "api_key": "sk-test-key"
        })
        # 即使 API key 无效也应返回结果（使用默认解读）
        assert response.status_code == 200


class TestCompatibilityEndpoint:
    """配对分析 API 测试"""
    
    def test_compatibility_analyze_success(self, client):
        """配对分析应成功"""
        response = client.post("/api/compatibility/analyze", json={
            "person1": {
                "birth_datetime": "1990-01-15T08:30:00",
                "gender": "男",
                "birth_place": "北京"
            },
            "person2": {
                "birth_datetime": "1992-06-20T14:00:00",
                "gender": "女",
                "birth_place": "上海"
            }
        })
        assert response.status_code == 200
        data = response.json()
        assert "total_score" in data
        assert "grade" in data
        assert "advice" in data
    
    def test_compatibility_score_range(self, client):
        """配对得分应在有效范围内"""
        response = client.post("/api/compatibility/analyze", json={
            "person1": {
                "birth_datetime": "1990-01-15T08:30:00",
                "gender": "男"
            },
            "person2": {
                "birth_datetime": "1992-06-20T14:00:00",
                "gender": "女"
            }
        })
        data = response.json()
        assert 0 <= data["total_score"] <= 100


class TestDateSelectionEndpoint:
    """择日分析 API 测试"""
    
    def test_date_selection_success(self, client):
        """择日分析应成功"""
        response = client.post("/api/date-selection/analyze", json={
            "birth_info": {
                "birth_datetime": "1990-01-15T08:30:00",
                "gender": "男"
            },
            "event_type": "结婚",
            "start_date": date.today().isoformat(),
            "search_days": 30
        })
        assert response.status_code == 200
        data = response.json()
        assert "event_type" in data
        assert "recommended_dates" in data
        assert "summary" in data
    
    @pytest.mark.parametrize("event", ["结婚", "开业", "搬家", "出行", "签约"])
    def test_date_selection_all_events(self, client, event):
        """应支持所有事件类型"""
        response = client.post("/api/date-selection/analyze", json={
            "birth_info": {
                "birth_datetime": "1990-01-15T08:30:00",
                "gender": "男"
            },
            "event_type": event,
            "search_days": 15
        })
        assert response.status_code == 200
    
    def test_date_selection_search_days_range(self, client):
        """搜索天数应在有效范围内"""
        # 超出范围应报错
        response = client.post("/api/date-selection/analyze", json={
            "birth_info": {
                "birth_datetime": "1990-01-15T08:30:00",
                "gender": "男"
            },
            "event_type": "结婚",
            "search_days": 100  # 超过最大值 90
        })
        assert response.status_code == 422
