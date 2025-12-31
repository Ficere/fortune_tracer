"""城市智能搜索模块

实现模糊匹配功能，提供良好的城市搜索体验
基于 cities_data 模块加载的 JSON 数据
"""
from difflib import SequenceMatcher
from functools import lru_cache
from src.core.utils.cities_data import CityInfo, get_all_cities, get_cities_by_name
from src.core.utils.solar_time import Location


@lru_cache(maxsize=1)
def _get_city_index() -> dict[str, CityInfo]:
    """获取城市名索引（优先市级，其次区县）"""
    index: dict[str, CityInfo] = {}
    cities = get_all_cities()

    # 先添加区县级（会被市级覆盖）
    for city in cities:
        if city.level == "district":
            index[city.name] = city
    # 再添加市级（优先级更高）
    for city in cities:
        if city.level == "city":
            index[city.name] = city
    # 最后添加省级
    for city in cities:
        if city.level == "province":
            index[city.name] = city

    return index


def search_cities(
    query: str,
    limit: int = 10,
    level: str | None = None
) -> list[CityInfo]:
    """
    智能搜索城市

    Args:
        query: 搜索词
        limit: 返回结果数量限制
        level: 限制级别 (province/city/district)，None表示不限

    Returns:
        匹配的城市列表，按相关度排序
    """
    if not query:
        return []

    query = query.strip()
    results: list[tuple[float, CityInfo]] = []
    seen: set[str] = set()

    cities = get_all_cities()
    if level:
        cities = [c for c in cities if c.level == level]

    def add_result(score: float, city: CityInfo):
        key = f"{city.name}_{city.province}_{city.level}"
        if key not in seen:
            seen.add(key)
            results.append((score, city))

    for city in cities:
        name = city.name
        full = city.full_name

        # 1. 精确匹配 (最高优先级)
        if query == name or query == full:
            add_result(1.0, city)
            continue

        # 2. 前缀匹配
        if name.startswith(query) or full.startswith(query):
            add_result(0.9, city)
            continue

        # 3. 包含匹配
        if query in name or query in full:
            add_result(0.8, city)
            continue

        # 4. 模糊匹配 (字符串相似度)
        ratio = SequenceMatcher(None, query, name).ratio()
        if ratio > 0.5:
            add_result(ratio * 0.7, city)

    # 按分数降序，市级优先
    level_priority = {"city": 0, "district": 1, "province": 2}
    results.sort(key=lambda x: (-x[0], level_priority.get(x[1].level, 9)))
    return [city for _, city in results[:limit]]


def get_location_smart(city_name: str) -> Location | None:
    """
    智能获取城市位置信息

    Args:
        city_name: 城市名称

    Returns:
        Location对象，未找到返回None
    """
    # 1. 精确匹配
    index = _get_city_index()
    if city := index.get(city_name):
        return Location(city.name, city.longitude, city.latitude)

    # 2. 模糊搜索取第一个
    matches = search_cities(city_name, limit=1)
    if matches:
        city = matches[0]
        return Location(city.name, city.longitude, city.latitude)

    return None


def get_search_suggestions(query: str) -> list[str]:
    """获取搜索建议（用于UI自动补全）"""
    cities = search_cities(query, limit=8, level="city")
    return [f"{c.name} ({c.province})" for c in cities]


def get_all_city_options() -> list[str]:
    """获取所有市级城市选项（用于下拉框）"""
    from src.core.utils.cities_data import get_cities_by_level
    cities = get_cities_by_level("city")
    return [f"{c.name} ({c.province})" for c in cities]


def parse_city_option(option: str) -> str:
    """从选项字符串中解析城市名"""
    if "(" in option:
        return option.split("(")[0].strip()
    return option.strip()

