"""运势详细解读 UI 组件"""
import streamlit as st
from src.models.bazi_models import DaYunInfo, YearFortune


def render_dayun_detail_panel(
    dayun_info: DaYunInfo, fortunes: list[YearFortune] | None = None
):
    """渲染大运详细解读面板（可展开），支持年度细分"""
    st.markdown(f"**大运方向**: {dayun_info.direction} | **起运年龄**: {dayun_info.start_age}岁")

    for i, dayun in enumerate(dayun_info.dayun_list):
        detail = dayun.detail
        emoji = detail.emoji if detail else "📅"
        level = detail.level if detail else "平"

        with st.expander(
            f"{emoji} **{dayun.ganzhi}** ({dayun.start_age}-{dayun.end_age}岁) - {level}",
            expanded=(i == 0)
        ):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**干支**: {dayun.ganzhi} ({dayun.wuxing})")
                st.markdown(f"**年份**: {dayun.start_year}-{dayun.end_year}")
                if detail:
                    st.markdown(f"**运势评分**: {detail.score:.0f}/100")
                    st.markdown(f"**人生阶段**: {detail.stage}")

            with col2:
                if detail:
                    st.markdown(f"**天干分析**: {detail.gan_relation}")
                    st.markdown(f"**地支分析**: {detail.zhi_relation}")

            if detail:
                st.divider()
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.markdown("**💼 事业**")
                    for advice in detail.career[:2]:
                        st.caption(f"• {advice}")
                with col2:
                    st.markdown("**💕 感情**")
                    for advice in detail.love[:2]:
                        st.caption(f"• {advice}")
                with col3:
                    st.markdown("**💰 财运**")
                    for advice in detail.wealth[:2]:
                        st.caption(f"• {advice}")
                with col4:
                    st.markdown("**🏥 健康**")
                    st.caption(f"• {detail.health}")

                st.info(detail.summary)

            # 年度细分：显示该大运期间每一年的运势
            if fortunes:
                _render_dayun_yearly_detail(dayun, fortunes)


def _render_dayun_yearly_detail(dayun, fortunes: list[YearFortune]):
    """渲染大运期间每年的运势细分"""
    # 找出该大运期间的流年
    yearly_fortunes = [
        f for f in fortunes
        if dayun.start_age <= f.age <= dayun.end_age
    ]

    if not yearly_fortunes:
        return

    st.divider()
    st.markdown("##### 📅 年度运势细分")

    # 使用紧凑的表格形式展示
    cols = st.columns(min(5, len(yearly_fortunes)))
    for idx, fortune in enumerate(yearly_fortunes[:10]):
        col_idx = idx % min(5, len(yearly_fortunes))
        with cols[col_idx]:
            detail = fortune.detail
            emoji = detail.emoji if detail else "😐"
            level = detail.level if detail else "平"

            # 紧凑卡片
            bg_color = _get_level_color(level)
            st.markdown(f"""
            <div style='background:{bg_color};padding:6px;border-radius:6px;
                text-align:center;margin-bottom:8px;font-size:12px'>
                <div style='font-weight:bold'>{fortune.year}</div>
                <div>{fortune.age}岁 {emoji}</div>
                <div style='font-size:10px'>{fortune.ganzhi}</div>
                <div style='font-size:11px'>{fortune.score:.0f}分</div>
            </div>
            """, unsafe_allow_html=True)

    # 如果超过5年，显示第二行
    if len(yearly_fortunes) > 5:
        cols2 = st.columns(min(5, len(yearly_fortunes) - 5))
        for idx, fortune in enumerate(yearly_fortunes[5:10]):
            with cols2[idx]:
                detail = fortune.detail
                emoji = detail.emoji if detail else "😐"
                level = detail.level if detail else "平"
                bg_color = _get_level_color(level)
                st.markdown(f"""
                <div style='background:{bg_color};padding:6px;border-radius:6px;
                    text-align:center;margin-bottom:8px;font-size:12px'>
                    <div style='font-weight:bold'>{fortune.year}</div>
                    <div>{fortune.age}岁 {emoji}</div>
                    <div style='font-size:10px'>{fortune.ganzhi}</div>
                    <div style='font-size:11px'>{fortune.score:.0f}分</div>
                </div>
                """, unsafe_allow_html=True)


def _get_level_color(level: str) -> str:
    """获取等级对应的背景色"""
    colors = {
        "大吉": "#dcfce7", "吉": "#bbf7d0", "小吉": "#d1fae5",
        "平": "#fef9c3",
        "小凶": "#fed7aa", "凶": "#fecaca", "大凶": "#fca5a5"
    }
    return colors.get(level, "#f1f5f9")


def render_fortune_year_selector(fortunes: list[YearFortune]):
    """渲染流年选择器和详细解读"""
    if not fortunes:
        return
    
    # 创建年龄范围选择
    ages = [f.age for f in fortunes]
    min_age, max_age = min(ages), max(ages)
    
    selected_age = st.slider(
        "选择年龄查看详细运势",
        min_value=min_age, max_value=max_age, value=30
    )
    
    # 找到对应年份
    fortune = next((f for f in fortunes if f.age == selected_age), None)
    if not fortune:
        return
    
    st.markdown(f"### {fortune.year}年 ({fortune.description})")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("运势评分", f"{fortune.score:.0f}", delta=None)
    with col2:
        if fortune.detail:
            st.metric("运势等级", f"{fortune.detail.emoji} {fortune.detail.level}")
    with col3:
        st.metric("五行", fortune.wuxing)
    
    if fortune.detail:
        detail = fortune.detail
        st.markdown(f"**五行影响**: {detail.wuxing_effect}")
        
        if detail.ganzhi_relations:
            st.markdown(f"**与命局关系**: {', '.join(detail.ganzhi_relations)}")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 各方面运势")
            st.markdown(f"- 💼 **事业**: {detail.career}")
            st.markdown(f"- 💕 **感情**: {detail.love}")
            st.markdown(f"- 💰 **财运**: {detail.wealth}")
            st.markdown(f"- 🏥 **健康**: {detail.health}")
        
        with col2:
            st.markdown("#### 宜忌事项")
            if detail.suitable:
                st.success(f"✅ 宜: {', '.join(detail.suitable)}")
            if detail.unsuitable:
                st.error(f"❌ 忌: {', '.join(detail.unsuitable)}")


def render_fortune_decade_summary(fortunes: list[YearFortune]):
    """渲染十年运势摘要"""
    if len(fortunes) < 10:
        return
    
    st.markdown("### 📊 十年运势概览")
    
    # 按十年分组
    decades = []
    for i in range(0, min(90, len(fortunes)), 10):
        decade_fortunes = fortunes[i:i+10]
        if decade_fortunes:
            avg_score = sum(f.score for f in decade_fortunes) / len(decade_fortunes)
            best = max(decade_fortunes, key=lambda f: f.score)
            worst = min(decade_fortunes, key=lambda f: f.score)
            decades.append({
                "range": f"{i}-{i+9}岁",
                "avg": avg_score,
                "best": best,
                "worst": worst
            })
    
    cols = st.columns(min(5, len(decades)))
    for i, decade in enumerate(decades[:5]):
        with cols[i]:
            emoji = "🌟" if decade["avg"] >= 70 else "😐" if decade["avg"] >= 55 else "⚠️"
            st.markdown(f"**{decade['range']}**")
            st.metric(emoji, f"{decade['avg']:.0f}分")
            st.caption(f"最佳: {decade['best'].age}岁")

