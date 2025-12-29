"""命理学AI分析提示词系统"""

SYSTEM_PROMPT = """你是一位资深的中国传统命理学专家，精通八字分析、五行学说和运势解读。
你的任务是根据提供的八字数据进行专业、全面的命理分析。

分析原则：
1. 以日主为核心，结合五行生克关系进行解读
2. 喜用神代表有利因素，忌神代表需注意的方面
3. 运势分析要结合年龄阶段给出实际建议
4. 语言专业但通俗易懂，避免过于晦涩的术语
5. 保持客观中立，不做极端预测

请严格按照指定的JSON格式返回分析结果。"""


def build_analysis_prompt(bazi_json: str) -> str:
    """构建八字分析提示词"""
    return f"""请根据以下八字数据进行深度命理分析：

## 八字数据
```json
{bazi_json}
```

## 分析要求
请从以下维度进行专业解读，每个维度150-250字：

1. **性格特点**：基于日主五行和四柱组合分析性格特征
2. **事业运势**：结合喜用神分析适合的行业和发展方向
3. **感情运势**：分析感情模式和婚恋建议
4. **健康建议**：根据五行偏弱方面给出养生建议
5. **财运分析**：分析财运特点和理财建议
6. **综合评价**：整体命局评价和人生建议

## 返回格式
请严格按照以下JSON格式返回：
{{
    "personality": "性格分析内容...",
    "career": "事业分析内容...",
    "love": "感情分析内容...",
    "health": "健康建议内容...",
    "wealth": "财运分析内容...",
    "summary": "综合评价内容..."
}}"""


def build_fortune_prompt(bazi_json: str, target_year: int) -> str:
    """构建流年运势分析提示词"""
    return f"""请根据以下八字数据，分析{target_year}年的详细运势：

## 八字数据
```json
{bazi_json}
```

## 分析要求
请分析{target_year}年的运势，包括：
1. 整体运势评价
2. 事业发展建议
3. 感情状况预测
4. 财运机遇分析
5. 健康注意事项
6. 宜忌事项建议

## 返回格式
{{
    "year": {target_year},
    "overall_score": 70,
    "overall_level": "小吉",
    "career": "事业方面...",
    "love": "感情方面...",
    "wealth": "财运方面...",
    "health": "健康方面...",
    "suitable": ["宜做的事1", "宜做的事2"],
    "unsuitable": ["不宜做的事1", "不宜做的事2"],
    "monthly_highlights": "重点月份提示..."
}}"""


def build_compatibility_prompt(person1_json: str, person2_json: str) -> str:
    """构建配对分析提示词"""
    return f"""请根据以下两人的八字数据进行配对分析：

## 甲方八字
```json
{person1_json}
```

## 乙方八字
```json
{person2_json}
```

## 分析要求
1. 五行互补分析
2. 日主相合程度
3. 性格契合度
4. 潜在问题提示
5. 相处建议

## 返回格式
{{
    "compatibility_score": 75,
    "grade": "良好",
    "wuxing_analysis": "五行互补情况...",
    "personality_match": "性格匹配分析...",
    "potential_issues": ["可能问题1", "可能问题2"],
    "advice": "相处建议...",
    "summary": "综合评价..."
}}"""


# 响应JSON Schema定义（用于验证）
INTERPRETATION_SCHEMA = {
    "type": "object",
    "properties": {
        "personality": {"type": "string"},
        "career": {"type": "string"},
        "love": {"type": "string"},
        "health": {"type": "string"},
        "wealth": {"type": "string"},
        "summary": {"type": "string"},
    },
    "required": ["personality", "career", "love", "health", "wealth", "summary"],
}

