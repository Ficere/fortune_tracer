"""中国城市经纬度数据库

基于 src/assets/latlng.json 加载全国省市区经纬度数据
支持省级、市级、区县级地理位置查询
"""
import json
from functools import lru_cache
from pathlib import Path
from typing import NamedTuple


class CityInfo(NamedTuple):
    """城市/区县信息"""
    name: str           # 名称（不含后缀）
    province: str       # 省份
    longitude: float    # 经度
    latitude: float     # 纬度
    level: str          # 级别: province/city/district
    full_name: str      # 完整名称（含后缀）


_DATA_FILE = Path(__file__).parent.parent.parent / "assets" / "latlng.json"


def _normalize_name(name: str) -> str:
    """移除地名后缀，获取核心名称"""
    suffixes = ["省", "市", "区", "县", "自治区", "自治州", "自治县", "特别行政区"]
    for suffix in suffixes:
        if name.endswith(suffix) and len(name) > len(suffix):
            return name[:-len(suffix)]
    return name


def _parse_location_data(data: dict) -> list[CityInfo]:
    """解析JSON数据，提取所有地理位置"""
    results: list[CityInfo] = []

    for province in data.get("children", []):
        prov_name = province.get("name", "")
        prov_norm = _normalize_name(prov_name)

        # 添加省级
        if "lat" in province and "lng" in province:
            results.append(CityInfo(
                name=prov_norm,
                province=prov_norm,
                longitude=float(province["lat"]),  # JSON中lat是经度
                latitude=float(province["lng"]),   # JSON中lng是纬度
                level="province",
                full_name=prov_name
            ))

        # 遍历市级
        for city in province.get("children", []):
            city_name = city.get("name", "")
            city_norm = _normalize_name(city_name)

            if "lat" in city and "lng" in city:
                results.append(CityInfo(
                    name=city_norm,
                    province=prov_norm,
                    longitude=float(city["lat"]),
                    latitude=float(city["lng"]),
                    level="city",
                    full_name=city_name
                ))

            # 遍历区县级
            for district in city.get("children", []):
                dist_name = district.get("name", "")
                dist_norm = _normalize_name(dist_name)

                if "lat" in district and "lng" in district:
                    results.append(CityInfo(
                        name=dist_norm,
                        province=prov_norm,
                        longitude=float(district["lat"]),
                        latitude=float(district["lng"]),
                        level="district",
                        full_name=dist_name
                    ))

    return results


@lru_cache(maxsize=1)
def _load_cities() -> list[CityInfo]:
    """加载并缓存所有城市数据"""
    with open(_DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return _parse_location_data(data)


@lru_cache(maxsize=1)
def _build_name_index() -> dict[str, list[CityInfo]]:
    """构建名称索引（支持同名城市）"""
    cities = _load_cities()
    index: dict[str, list[CityInfo]] = {}
    for city in cities:
        if city.name not in index:
            index[city.name] = []
        index[city.name].append(city)
    return index


def get_all_cities() -> list[CityInfo]:
    """获取所有城市列表"""
    return _load_cities()


def get_cities_by_level(level: str) -> list[CityInfo]:
    """按级别获取城市列表 (province/city/district)"""
    return [c for c in _load_cities() if c.level == level]


def get_city_names() -> list[str]:
    """获取所有城市名称（去重）"""
    return list(_build_name_index().keys())


def get_provinces() -> list[str]:
    """获取所有省份名称"""
    return list(set(c.province for c in _load_cities() if c.level == "province"))


def get_cities_by_name(name: str) -> list[CityInfo]:
    """根据名称获取城市列表（可能有同名）"""
    return _build_name_index().get(name, [])