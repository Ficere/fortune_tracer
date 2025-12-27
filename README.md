# 🔮 Fortune Tracer - 生辰八字 AI 智能解读

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

一个现代化的生辰八字命理分析应用，结合传统命理学与 AI 技术，提供专业的八字解读服务。

## ✨ 功能特性

### 🔮 个人八字分析
- **四柱精算** - 年、月、日、时柱准确计算（支持真太阳时）
- **五行分析** - 五行能量分布、日主强弱、喜用神/忌神
- **十神解析** - 比肩、劫财、食神、伤官等十神关系
- **大运流年** - 十年大运排盘、流年运势预测
- **AI 解读** - 基于 GPT 的智能命理解读

### 💑 八字配对分析
- 双人五行互补分析
- 天干合冲（甲己合、甲庚冲等）
- 地支六合、六冲、相刑
- 配对得分与建议

### 📅 择日功能
- 结婚、开业、搬家、出行、签约吉日
- 每日宜忌事项
- 冲煞生肖提醒
- 个性化吉日推荐（基于个人八字）

## 🚀 快速开始

### 环境要求

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) 包管理器（推荐）

### 安装

```bash
# 克隆项目
git clone https://github.com/your-username/fortune-tracer.git
cd fortune-tracer

# 使用 uv 安装依赖
uv sync

# 或使用 pip
pip install -e .
```

### 配置

创建 `.env` 文件配置环境变量：

```bash
# OpenAI API Key（可选，用于 AI 解读）
OPENAI_API_KEY=sk-your-api-key

# API 服务地址（默认 localhost:8000）
API_BASE_URL=http://localhost:8000

# 日志级别
LOG_LEVEL=INFO
```

### 启动应用

#### 方式一：Streamlit 前端（推荐）

```bash
# 直接启动（内置计算）
uv run streamlit run app.py
```

访问 http://localhost:8501

#### 方式二：前后端分离

```bash
# 终端 1：启动后端 API
uv run uvicorn backend.main:app --reload --port 8000

# 终端 2：启动前端
uv run streamlit run app.py
```

- 前端：http://localhost:8501
- API 文档：http://localhost:8000/docs

## 📖 API 文档

### 八字分析

```http
POST /api/bazi/analyze
Content-Type: application/json

{
  "birth_info": {
    "birth_datetime": "1990-01-15T08:30:00",
    "gender": "男",
    "birth_place": "北京"
  },
  "api_key": "sk-xxx"  // 可选
}
```

### 配对分析

```http
POST /api/compatibility/analyze
Content-Type: application/json

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
Content-Type: application/json

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

## 🏗️ 项目结构

```
fortune-tracer/
├── app.py                 # Streamlit 主入口
├── pyproject.toml         # 项目配置
├── README.md
├── .env.example           # 环境变量示例
├── backend/               # FastAPI 后端
│   ├── main.py           # API 入口
│   └── api/
│       ├── routes/       # API 路由
│       └── schemas.py    # 请求/响应模型
├── src/                   # 核心模块
│   ├── core/             # 核心计算
│   │   ├── pillars.py    # 四柱计算
│   │   ├── wuxing.py     # 五行分析
│   │   ├── shishen.py    # 十神分析
│   │   ├── dayun.py      # 大运计算
│   │   ├── solar_time.py # 真太阳时
│   │   ├── jieqi.py      # 节气计算
│   │   ├── compatibility.py  # 配对计算
│   │   ├── date_selection.py # 择日计算
│   │   ├── calendar.py   # 农历转换
│   │   └── constants.py  # 常量表
│   ├── models/           # 数据模型
│   │   ├── bazi_models.py
│   │   ├── compatibility_models.py
│   │   └── date_selection_models.py
│   ├── ai/               # AI 模块
│   │   └── interpreter.py
│   ├── ui/               # UI 页面
│   │   ├── bazi_page.py
│   │   ├── compatibility_page.py
│   │   ├── date_selection_page.py
│   │   └── common.py
│   └── viz/              # 可视化
│       ├── charts.py
│       ├── palace.py
│       ├── compatibility_charts.py
│       └── date_charts.py
└── tests/                # 测试
    ├── test_pillars.py
    ├── test_wuxing.py
    ├── test_api.py
    └── conftest.py
```

## 🧪 测试

```bash
# 运行所有测试
uv run pytest

# 运行带覆盖率报告
uv run pytest --cov=src --cov-report=html

# 运行特定测试
uv run pytest tests/test_pillars.py -v
```

## 📚 命理学基础

### 四柱八字

四柱即年柱、月柱、日柱、时柱，每柱由一个天干和一个地支组成，共八个字。

- **天干**：甲、乙、丙、丁、戊、己、庚、辛、壬、癸
- **地支**：子、丑、寅、卯、辰、巳、午、未、申、酉、戌、亥

### 五行相生相克

- **相生**：木生火、火生土、土生金、金生水、水生木
- **相克**：木克土、土克水、水克火、火克金、金克木

### 十神关系

基于日主（日柱天干）与其他天干的五行生克关系：

| 关系 | 同性 | 异性 |
|------|------|------|
| 同我 | 比肩 | 劫财 |
| 生我 | 偏印 | 正印 |
| 我生 | 食神 | 伤官 |
| 克我 | 七杀 | 正官 |
| 我克 | 偏财 | 正财 |

## ⚠️ 免责声明

本应用仅供娱乐和学习参考，命理分析结果不应作为重大人生决策的唯一依据。请理性看待命理学，保持科学态度。

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📮 联系

如有问题，请提交 [GitHub Issue](https://github.com/your-username/fortune-tracer/issues)。
