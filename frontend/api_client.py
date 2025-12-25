"""API客户端 - 与后端通信"""
import httpx
from datetime import datetime, date
from typing import Optional
import os

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
TIMEOUT = 30.0


class APIError(Exception):
    """API调用错误"""
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


def _make_request(method: str, endpoint: str, data: dict = None) -> dict:
    """发起API请求"""
    url = f"{API_BASE_URL}{endpoint}"
    try:
        with httpx.Client(timeout=TIMEOUT) as client:
            if method == "GET":
                response = client.get(url)
            else:
                response = client.post(url, json=data)
            
            if response.status_code >= 400:
                detail = response.json().get("detail", "请求失败")
                raise APIError(detail, response.status_code)
            
            return response.json()
    except httpx.ConnectError:
        raise APIError("无法连接到后端服务，请确保后端已启动", 503)
    except httpx.TimeoutException:
        raise APIError("请求超时，请稍后重试", 504)


def analyze_bazi(
    birth_datetime: datetime,
    gender: str,
    birth_place: Optional[str] = None,
    api_key: Optional[str] = None
) -> dict:
    """调用八字分析API"""
    data = {
        "birth_info": {
            "birth_datetime": birth_datetime.isoformat(),
            "gender": gender,
            "birth_place": birth_place
        },
        "api_key": api_key
    }
    return _make_request("POST", "/api/bazi/analyze", data)


def analyze_compatibility(
    person1_datetime: datetime, person1_gender: str, person1_place: Optional[str],
    person2_datetime: datetime, person2_gender: str, person2_place: Optional[str]
) -> dict:
    """调用配对分析API"""
    data = {
        "person1": {
            "birth_datetime": person1_datetime.isoformat(),
            "gender": person1_gender,
            "birth_place": person1_place
        },
        "person2": {
            "birth_datetime": person2_datetime.isoformat(),
            "gender": person2_gender,
            "birth_place": person2_place
        }
    }
    return _make_request("POST", "/api/compatibility/analyze", data)


def analyze_date_selection(
    birth_datetime: datetime,
    gender: str,
    birth_place: Optional[str],
    event_type: str,
    start_date: date,
    search_days: int = 30
) -> dict:
    """调用择日分析API"""
    data = {
        "birth_info": {
            "birth_datetime": birth_datetime.isoformat(),
            "gender": gender,
            "birth_place": birth_place
        },
        "event_type": event_type,
        "start_date": start_date.isoformat(),
        "search_days": search_days
    }
    return _make_request("POST", "/api/date-selection/analyze", data)


def check_health() -> bool:
    """检查后端健康状态"""
    try:
        result = _make_request("GET", "/health")
        return result.get("status") == "healthy"
    except APIError:
        return False

