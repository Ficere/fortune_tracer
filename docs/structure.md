# 项目结构

```
fortune-tracer/
├── app.py                 # Streamlit 主入口
├── pyproject.toml         # 项目配置
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
│   │   ├── shensha.py    # 神煞分析
│   │   ├── nayin.py      # 纳音计算
│   │   ├── auxiliary.py  # 命宫胎元身宫
│   │   ├── liunian.py    # 流年分析
│   │   ├── solar_time.py # 真太阳时
│   │   ├── jieqi.py      # 节气计算
│   │   ├── compatibility.py  # 配对计算
│   │   └── date_selection.py # 择日计算
│   ├── models/           # Pydantic 数据模型
│   ├── ai/               # AI 解读模块
│   ├── ui/               # Streamlit 页面
│   └── viz/              # Plotly 可视化
├── tests/                # 测试（覆盖率 96%）
└── docs/                 # 文档
```

## 测试

```bash
# 运行测试
uv run pytest

# 带覆盖率
uv run pytest --cov=src --cov-report=html
```
