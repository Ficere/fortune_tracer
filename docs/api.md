# API 文档

## 启动 API 服务

```bash
uv run uvicorn backend.main:app --reload --port 8000
```

- API 文档：http://localhost:8000/docs
- ReDoc：http://localhost:8000/redoc

## 接口列表

### 八字分析

```http
POST /api/bazi/analyze
```

```json
{
  "birth_info": {
    "birth_datetime": "1990-01-15T08:30:00",
    "gender": "男",
    "birth_place": "北京"
  },
  "api_key": "sk-xxx"
}
```

### 配对分析

```http
POST /api/compatibility/analyze
```

```json
{
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
}
```

### 择日分析

```http
POST /api/date-selection/analyze
```

```json
{
  "birth_info": {
    "birth_datetime": "1990-01-15T08:30:00",
    "gender": "男"
  },
  "event_type": "结婚",
  "start_date": "2024-01-01",
  "search_days": 30
}
```

### 高级分析

| 端点 | 功能 |
|------|------|
| `POST /api/advanced/dayun` | 大运计算 |
| `POST /api/advanced/shishen` | 十神分析 |
| `POST /api/advanced/shensha` | 神煞分析 |
| `POST /api/advanced/nayin` | 纳音五行 |
| `POST /api/advanced/auxiliary` | 命宫胎元身宫 |

## 配置

创建 `.env` 文件：

```bash
OPENAI_API_KEY=sk-your-api-key  # 可选
API_BASE_URL=http://localhost:8000
LOG_LEVEL=INFO
```
