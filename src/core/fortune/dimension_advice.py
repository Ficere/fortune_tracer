"""七维度运势建议生成"""


def get_career_advice(score: float) -> list[str]:
    """事业学业建议"""
    if score >= 75:
        return ["适合推进重要项目", "可安排商务谈判", "主动展示工作成果"]
    if score >= 60:
        return ["按计划推进工作", "做好本职任务", "避免与上司争执"]
    return ["低调行事为佳", "避免重大决策", "多做少说"]


def get_wealth_advice(score: float) -> list[str]:
    """财富运势建议"""
    if score >= 75:
        return ["可考虑小额投资", "适合洽谈合作", "有望获得额外收入"]
    if score >= 60:
        return ["收支基本平衡", "避免大宗消费", "理性购物"]
    return ["避免借贷", "谨慎投资", "守财为上"]


def get_love_advice(score: float) -> list[str]:
    """感情人际建议"""
    if score >= 75:
        return ["适合表白约会", "感情沟通顺畅", "多陪伴家人朋友"]
    if score >= 60:
        return ["维持现状为佳", "多些理解包容", "避免情绪化"]
    return ["控制情绪", "减少争执", "给彼此空间"]


def get_health_advice(score: float) -> list[str]:
    """健康体能建议"""
    if score >= 75:
        return ["适合运动锻炼", "精力充沛可多安排活动", "身心状态良好"]
    if score >= 60:
        return ["保持规律作息", "饮食清淡为主", "适度休息"]
    return ["注意休息", "避免剧烈运动", "警惕意外伤害"]


def get_emotion_advice(score: float) -> list[str]:
    """心态情绪建议"""
    if score >= 75:
        return ["思路清晰适合决策", "心态积极进取", "把握良好状态"]
    if score >= 60:
        return ["保持平常心", "不急不躁", "理性面对问题"]
    return ["避免冲动决定", "多做深呼吸", "推迟重要决策"]


def get_family_advice(score: float) -> list[str]:
    """家庭生活建议"""
    if score >= 75:
        return ["适合家庭聚会", "可处理家务事宜", "亲情关系升温"]
    if score >= 60:
        return ["保持家庭和谐", "多些沟通交流", "避免争吵"]
    return ["减少家庭摩擦", "控制脾气", "给家人空间"]


def get_opportunity_advice(score: float) -> list[str]:
    """机遇贵人建议"""
    if score >= 75:
        return ["主动拓展人脉", "把握突然机会", "贵人会主动出现"]
    if score >= 60:
        return ["维持现有关系", "关注身边机会", "适度社交"]
    return ["暂不宜冒险", "稳定为主", "等待更好时机"]


# 维度建议函数映射
ADVICE_FUNCS = {
    "career": get_career_advice,
    "wealth": get_wealth_advice,
    "love": get_love_advice,
    "health": get_health_advice,
    "emotion": get_emotion_advice,
    "family": get_family_advice,
    "opportunity": get_opportunity_advice,
}

