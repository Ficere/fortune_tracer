"""UI组件模块"""
from .bazi_page import render_bazi_analysis
from .compatibility_page import render_compatibility_analysis
from .date_selection_page import render_date_selection
from .bonefate_page import render_bonefate_analysis
from .chat_component import render_chat_section
from .ziwei_page import render_ziwei_page

__all__ = [
    "render_bazi_analysis",
    "render_compatibility_analysis",
    "render_date_selection",
    "render_bonefate_analysis",
    "render_chat_section",
    "render_ziwei_page",
]

