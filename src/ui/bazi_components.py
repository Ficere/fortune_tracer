"""八字页面组件 - 辅助渲染函数"""
import streamlit as st


def render_auxiliary_info(auxiliary):
    """渲染辅助宫位信息（命宫、胎元、身宫）"""
    cols = st.columns(3)
    
    gongs = [auxiliary.ming_gong, auxiliary.tai_yuan, auxiliary.shen_gong]
    colors = ["#10b981", "#6366f1", "#f59e0b"]
    icons = ["🏛️", "🌱", "👤"]
    
    for col, gong, color, icon in zip(cols, gongs, colors, icons):
        with col:
            st.markdown(f"""
            <div style='background:linear-gradient(135deg,{color}22,{color}11);
                padding:12px;border-radius:10px;text-align:center;
                border:1px solid {color}44'>
                <div style='font-size:12px;color:#64748b'>
                    {icon} {gong.name}
                </div>
                <div style='font-size:24px;font-weight:bold;color:{color}'>
                    {gong.ganzhi}
                </div>
                <div style='font-size:12px;color:#94a3b8;margin-top:4px'>
                    {gong.description}
                </div>
            </div>
            """, unsafe_allow_html=True)


def render_nayin_info(nayin_list):
    """渲染纳音五行信息"""
    cols = st.columns(4)
    
    # 五行对应颜色
    wuxing_colors = {
        "木": "#22c55e",
        "火": "#ef4444",
        "土": "#d97706",
        "金": "#f59e0b",
        "水": "#3b82f6"
    }
    
    pillar_icons = {"年柱": "🎋", "月柱": "🌙", "日柱": "☀️", "时柱": "🕐"}
    
    for col, info in zip(cols, nayin_list):
        color = wuxing_colors.get(info.wuxing, "#64748b")
        icon = pillar_icons.get(info.pillar_name, "📌")
        
        with col:
            st.markdown(f"""
            <div style='background:linear-gradient(135deg,{color}15,{color}05);
                padding:10px;border-radius:8px;text-align:center;
                border:1px solid {color}33'>
                <div style='font-size:11px;color:#64748b'>
                    {icon} {info.pillar_name} · {info.ganzhi}
                </div>
                <div style='font-size:16px;font-weight:bold;color:{color};
                    margin:4px 0'>
                    {info.nayin}
                </div>
                <div style='display:inline-block;padding:2px 8px;
                    background:{color}22;border-radius:10px;
                    font-size:11px;color:{color}'>
                    {info.wuxing}
                </div>
            </div>
            """, unsafe_allow_html=True)


def render_shensha_info(shensha):
    """渲染神煞信息"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### 🌟 吉神")
        if shensha.ji_shen:
            for ss in shensha.ji_shen:
                st.markdown(f"""
                <div style='display:inline-block;margin:2px;padding:4px 10px;
                    background:#dcfce7;border-radius:15px;font-size:12px;
                    color:#16a34a'>
                    {ss}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.caption("暂无")
    
    with col2:
        st.markdown("##### ⚡ 凶煞")
        if shensha.xiong_sha:
            for ss in shensha.xiong_sha:
                st.markdown(f"""
                <div style='display:inline-block;margin:2px;padding:4px 10px;
                    background:#fef2f2;border-radius:15px;font-size:12px;
                    color:#dc2626'>
                    {ss}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.caption("暂无")
    
    # 总结
    if shensha.summary:
        st.info(f"📌 {shensha.summary}")


def render_dayun_detail(dayun_info):
    """渲染大运详情（增强版）"""
    st.caption(
        f"起运: **{dayun_info.start_age}岁{dayun_info.extra_months}个月** | "
        f"方向: **{dayun_info.direction}**"
    )
    
    cols = st.columns(len(dayun_info.dayun_list))
    for col, dy in zip(cols, dayun_info.dayun_list):
        with col:
            st.markdown(f"""
            <div style='background:linear-gradient(135deg,#6366f1,#8b5cf6);
                padding:8px;border-radius:8px;text-align:center;color:white;
                font-size:12px'>
                <div style='font-size:16px;font-weight:bold'>{dy.ganzhi}</div>
                <div>{dy.start_age}-{dy.end_age}岁</div>
                <div style='opacity:0.8'>{dy.start_year}-{dy.end_year}</div>
            </div>
            """, unsafe_allow_html=True)


def render_shishen_detail(shishen):
    """渲染十神详情（增强版）"""
    cols = st.columns(4)
    for col, info in zip(cols, shishen.shishen_list):
        with col:
            st.markdown(f"""
            <div style='background:#f8fafc;padding:10px;border-radius:8px;
                text-align:center;border:1px solid #e2e8f0'>
                <div style='font-size:12px;color:#64748b'>{info.pillar_name}</div>
                <div style='font-size:16px;font-weight:bold;color:#334155'>
                    {info.tiangan} 
                    <span style='color:#6366f1'>({info.tiangan_shishen})</span>
                </div>
                <div style='font-size:16px;font-weight:bold;color:#334155'>
                    {info.dizhi}
                </div>
                <div style='font-size:10px;color:#94a3b8'>
                    藏: {', '.join(info.dizhi_shishen) or '-'}
                </div>
            </div>
            """, unsafe_allow_html=True)
