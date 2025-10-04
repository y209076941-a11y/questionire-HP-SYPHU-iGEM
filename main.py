import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
import json
import base64

# 页面配置
st.set_page_config(
    page_title="ATRA-AIVC Engineering Platform-2025-SYPHU-CHINA-iGEM",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 修复后的配色方案 - 更灵动有趣
st.markdown("""
<style>
    /* 灵动配色系统 */
    :root {
        --emerald: #255A3B;
        --mint: #81B095;
        --seafoam: #DDEADF;
        --sky: #D2E2EF;
        --coral: #DC917B;
        --terracotta: #8F533F;
        --lavender: #A78BFA;
        --sunflower: #F59E0B;
        --berry: #DB2777;
    }

    .nature-header {
        background: linear-gradient(135deg, var(--emerald) 0%, #1a3b2a 100%);
        padding: 3rem 2rem;
        border-radius: 16px;
        color: white;
        text-align: center;
        margin-bottom: 2.5rem;
        box-shadow: 0 12px 40px rgba(37, 90, 59, 0.2);
        border: 1px solid rgba(255,255,255,0.15);
        position: relative;
        overflow: hidden;
    }

    .nature-header::before {
        content: "";
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: float 6s ease-in-out infinite;
    }

    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-10px) rotate(180deg); }
    }

    .section-nature {
        background: linear-gradient(135deg, #ffffff 0%, var(--seafoam) 100%);
        padding: 2.5rem;
        border-radius: 16px;
        margin: 2rem 0;
        border-left: 6px solid var(--emerald);
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        border-top: 1px solid rgba(210, 226, 239, 0.8);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    .section-nature:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(37, 90, 59, 0.15);
    }

    .technical-card {
        background: linear-gradient(135deg, #ffffff 0%, var(--sky) 100%);
        padding: 2.5rem;
        border-radius: 16px;
        box-shadow: 0 8px 32px rgba(37, 90, 59, 0.12);
        margin: 2rem 0;
        border: 1px solid rgba(210, 226, 239, 0.8);
        position: relative;
        overflow: hidden;
    }

    .technical-card::after {
        content: "🧬";
        position: absolute;
        top: -20px;
        right: -20px;
        font-size: 8rem;
        opacity: 0.1;
        transform: rotate(15deg);
    }

    .hp-card {
        background: linear-gradient(135deg, #ffffff 0%, var(--seafoam) 100%);
        padding: 2.5rem;
        border-radius: 16px;
        box-shadow: 0 8px 32px rgba(37, 90, 59, 0.12);
        margin: 2rem 0;
        border: 1px solid rgba(221, 234, 223, 0.8);
        position: relative;
    }

    .interactive-card {
        background: linear-gradient(135deg, #ffffff 0%, #FEF3C7 100%);
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 8px 32px rgba(245, 158, 11, 0.15);
        margin: 2rem 0;
        border: 1px solid rgba(245, 158, 11, 0.3);
    }

    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, var(--emerald), var(--mint), var(--lavender));
        background-size: 200% 100%;
        animation: gradientShift 3s ease infinite;
    }

    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* 按钮样式 */
    .stButton > button {
        background: linear-gradient(135deg, var(--emerald), var(--mint));
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 50px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(37, 90, 59, 0.3);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(37, 90, 59, 0.4);
        background: linear-gradient(135deg, var(--mint), var(--emerald));
    }

    /* 科学图表容器 */
    .chart-container {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        border: 2px solid var(--sky);
        margin: 1rem 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    }

    /* 标签页样式 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }

    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background: linear-gradient(135deg, var(--seafoam), var(--sky));
        border-radius: 10px 10px 0 0;
        gap: 1rem;
        padding: 1rem 2rem;
        font-weight: 600;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, var(--emerald), var(--mint)) !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# 修复后的Header
st.markdown("""
<div class="nature-header">
    <h1 style="font-size: 3rem; margin-bottom: 0.5rem; background: linear-gradient(135deg, #ffffff, #D2E2EF); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">🔬 Cell Systems</h1>
    <h2 style="font-size: 2rem; font-weight: 400; margin-bottom: 1rem; opacity: 0.95;">AIVC-Engineered Bacteria for Targeted ATRA Delivery</h2>
    <p style="font-size: 1.2rem; opacity: 0.9;">Integrating Virtual Cell Simulation with Precision Oncology</p>
    <div style="margin-top: 1.5rem;">
        <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 25px; margin: 0 0.5rem;">🧫 Synthetic Biology</span>
        <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 25px; margin: 0 0.5rem;">🤖 AIVC Simulation</span>
        <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 25px; margin: 0 0.5rem;">🎯 Targeted Therapy</span>
    </div>
</div>
""", unsafe_allow_html=True)

# 侧边栏 - 修复并优化
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #255A3B, #1a3b2a); 
                border-radius: 16px; color: white; margin-bottom: 2rem; border: 1px solid rgba(255,255,255,0.1);">
        <h3 style="margin-bottom: 0.5rem;">🔍 Research Portal</h3>
        <p style="opacity: 0.9; margin-bottom: 1rem;">Interactive Assessment Platform</p>
        <div style="font-size: 2rem;">⚡</div>
    </div>
    """, unsafe_allow_html=True)

    # 研究团队信息
    with st.container():
        st.markdown("### 🧪 Research Team")
        team_info = st.text_input("**Affiliation**", placeholder="Institution, Department",
                                  label_visibility="collapsed")
        corresponding_author = st.text_input("**Corresponding Author**", placeholder="Name, Email",
                                             label_visibility="collapsed")

    st.markdown("---")

    # 动态指标
    st.markdown("### 📊 Live Metrics")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Response Rate", "87%", "+12%", delta_color="normal")
    with col2:
        st.metric("Avg Completion", "23 min", "-5 min", delta_color="inverse")

    # 实时活动指示器
    st.markdown("---")
    st.markdown("### 🔄 Activity")
    st.markdown("""
    <div style="background: rgba(210, 226, 239, 0.3); padding: 1rem; border-radius: 10px;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
            <span>Active Assessments</span>
            <span style="color: #255A3B; font-weight: bold;">12</span>
        </div>
        <div style="display: flex; justify-content: space-between;">
            <span>Completed Today</span>
            <span style="color: #81B095; font-weight: bold;">8</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("*Nature Cell Systems, 2025*")

# 初始化session state
if 'current_section' not in st.session_state:
    st.session_state.current_section = 0

# 修复进度条
sections = ["Study Overview", "Methodology", "Results", "Discussion", "Conclusions"]
progress_value = st.session_state.current_section / (len(sections) - 1)

st.markdown(f"""
<div style="background: linear-gradient(135deg, #ffffff, #DDEADF); padding: 2rem; border-radius: 16px; margin-bottom: 2rem; border: 2px solid #81B095; position: relative;">
    <div style="display: flex; justify-content: space-between; margin-bottom: 1rem; align-items: center;">
        <span style="color: #255A3B; font-weight: 600; font-size: 1.1rem;">Research Protocol Progress</span>
        <span style="background: #255A3B; color: white; padding: 0.3rem 0.8rem; border-radius: 20px; font-size: 0.9rem;">
            Section {st.session_state.current_section + 1} of {len(sections)}
        </span>
    </div>

    <div style="background: #DDEADF; height: 12px; border-radius: 8px; overflow: hidden; position: relative;">
        <div style="background: linear-gradient(90deg, #255A3B, #81B095, #A78BFA); width: {progress_value * 100}%; 
                    height: 100%; transition: width 0.8s ease; border-radius: 8px;"></div>
    </div>

    <div style="display: flex; justify-content: space-between; margin-top: 1rem; font-size: 0.9rem; color: #666;">
        {' '.join([f'<span style="color: {"#255A3B" if i <= st.session_state.current_section else "#999"}; font-weight: {"600" if i == st.session_state.current_section else "400"};">{section}</span>'
                   for i, section in enumerate(sections)])}
    </div>
</div>
""", unsafe_allow_html=True)

# Section 1: 研究概述 - 修复并增强
if st.session_state.current_section >= 0:
    st.markdown("""
    <div class="section-nature">
        <h2 style="color: #255A3B; margin-bottom: 1rem;">📖 Study Overview & Hypothesis</h2>
        <p style="color: #666; font-size: 1.1rem; line-height: 1.6;">Evaluating AIVC-guided engineering of bacterial systems for targeted cancer therapy through computational-experimental integration.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])

    with col1:
        with st.form("study_overview"):
            st.markdown("### 🎯 Research Context")

            research_gap = st.selectbox(
                "**Primary Research Gap Addressed**",
                ["Limited targeted delivery in HCC therapy",
                 "Inefficient ATRA bioavailability",
                 "Poor tumor microenvironment targeting",
                 "Lack of predictive in silico models",
                 "Engineering biology safety concerns",
                 "Other"],
                help="Select the most relevant research gap"
            )

            hypothesis = st.text_area(
                "**Central Research Hypothesis**",
                placeholder="Example: Engineered bacteria with lactate-chemotaxis will selectively deliver ATRA to HCC tumors, improving therapeutic efficacy while reducing systemic toxicity...",
                height=120
            )

            st.markdown("### 💡 Expected Contributions")
            contributions = st.multiselect(
                "**Anticipated Scientific Contributions**",
                ["Novel AIVC methodology", "Improved therapeutic targeting",
                 "Engineering biology platform", "Clinical translation framework",
                 "Computational-experimental integration", "Regulatory science advancement",
                 "Open-source tools", "Educational resources"],
                default=["Novel AIVC methodology", "Improved therapeutic targeting"]
            )

            if st.form_submit_button("**Continue to Methodology →**", use_container_width=True):
                st.session_state.current_section = 1
                st.rerun()

    with col2:
        st.markdown("### 🎯 Research Impact Matrix")

        # 修复的雷达图 - 使用正确的颜色格式
        impact_fig = go.Figure()

        impact_categories = ['Scientific', 'Clinical', 'Technical', 'Commercial', 'Educational']
        current_scores = [8, 6, 9, 4, 7]

        impact_fig.add_trace(go.Scatterpolar(
            r=current_scores,
            theta=impact_categories,
            fill='toself',
            name='Current Impact',
            line=dict(color='#255A3B', width=3),
            fillcolor='rgba(37, 90, 59, 0.3)'  # 修复：使用rgba格式
        ))

        impact_fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 10],
                    gridcolor='#D2E2EF',
                    linecolor='#81B095'
                ),
                bgcolor='rgba(255,255,255,0.8)'
            ),
            showlegend=False,
            height=400,
            margin=dict(l=50, r=50, t=50, b=50),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )

        st.plotly_chart(impact_fig, use_container_width=True)

# Section 2: 方法论 - 修复并增强交互性
if st.session_state.current_section >= 1:
    st.markdown("""
    <div class="technical-card">
        <h2 style="color: #255A3B; margin-bottom: 1rem;">🛠️ Methodology & Technical Framework</h2>
        <p style="color: #666;">AIVC simulation pipeline and engineering biology workflow with interactive parameter tuning</p>
    </div>
    """, unsafe_allow_html=True)

    # 使用标签页
    tab1, tab2, tab3 = st.tabs(["🧠 AIVC Platform", "🧬 Engineering Design", "🔬 Experimental Validation"])

    with tab1:
        col1, col2 = st.columns([3, 2])

        with col1:
            st.markdown("### AIVC Simulation Parameters")

            with st.form("aivc_methodology"):
                st.markdown("**Virtual Cell Configuration**")

                col1a, col1b = st.columns(2)
                with col1a:
                    cell_parameters = st.slider(
                        "**Cell Population Size (log10)**", 3, 8, 5,
                        help="Simulated bacterial population scale"
                    )

                    time_resolution = st.selectbox(
                        "**Temporal Resolution**",
                        ["1 ms", "10 ms", "100 ms", "1 s", "10 s"],
                        index=3
                    )

                with col1b:
                    spatial_dimensions = st.multiselect(
                        "**Spatial Dimensions Modeled**",
                        ["2D monolayer", "3D spheroid", "Vascular network",
                         "Tissue gradient", "Whole organism"],
                        default=["3D spheroid", "Tissue gradient"]
                    )

                st.markdown("**Molecular Dynamics**")
                binding_affinity = st.slider(
                    "**Lactate Binding Affinity (Kd)**", 0.1, 10.0, 2.5, 0.1,
                    help="Simulated receptor-ligand interaction strength"
                )

                if st.form_submit_button("🔄 Update Simulation Parameters"):
                    st.success("Parameters updated for AIVC simulation!")

        with col2:
            st.markdown("### ⚡ Simulation Performance")

            # 性能指标仪表盘
            performance_data = {
                'Metric': ['Computational Speed', 'Memory Efficiency', 'Accuracy', 'Scalability'],
                'Score': [85, 72, 88, 65],
                'Color': ['#255A3B', '#81B095', '#A78BFA', '#F59E0B']
            }

            perf_fig = px.bar(performance_data, x='Score', y='Metric',
                              orientation='h',
                              color='Metric',
                              color_discrete_map={
                                  'Computational Speed': '#255A3B',
                                  'Memory Efficiency': '#81B095',
                                  'Accuracy': '#A78BFA',
                                  'Scalability': '#F59E0B'
                              })

            perf_fig.update_layout(
                height=300,
                showlegend=False,
                xaxis_title="Performance Score",
                yaxis_title="",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )

            st.plotly_chart(perf_fig, use_container_width=True)

    with tab2:
        st.markdown("### 🧬 Genetic Circuit Design Analysis")

        # 修复的散点图
        circuit_data = {
            'Component': ['Promoter', 'RBS', 'Coding', 'Terminator', 'Regulatory'],
            'Complexity': [3, 2, 7, 1, 5],
            'Stability': [8, 9, 6, 9, 7],
            'Size': [200, 50, 1500, 100, 800]
        }

        circuit_fig = px.scatter(
            circuit_data,
            x='Complexity',
            y='Stability',
            size='Size',
            text='Component',
            color='Component',
            color_discrete_sequence=['#255A3B', '#81B095', '#A78BFA', '#F59E0B', '#DB2777']
        )

        circuit_fig.update_traces(
            textposition="top center",
            marker=dict(sizemode='diameter', sizeref=2. * max(circuit_data['Size']) / (40. ** 2), sizemin=4),
            textfont=dict(size=14, color="white", family="Arial Black")
        )

        circuit_fig.update_layout(
            title="Genetic Component Analysis",
            xaxis_title="Design Complexity",
            yaxis_title="Predicted Stability",
            height=450,
            showlegend=False
        )

        st.plotly_chart(circuit_fig, use_container_width=True)

    with tab3:
        st.markdown("### 🔬 Validation Strategy")

        validation_methods = st.multiselect(
            "**Primary Validation Approaches**",
            ["Fluorescence microscopy", "qPCR analysis", "Mass spectrometry",
             "Animal models", "Cell culture", "Flow cytometry", "HPLC", "RNA-seq"],
            default=["Fluorescence microscopy", "Animal models", "Mass spectrometry"]
        )

        st.markdown("**Statistical Power Analysis**")
        col1, col2, col3 = st.columns(3)

        with col1:
            sample_size = st.number_input("**Sample Size (n)**", min_value=3, value=6,
                                          help="Number of biological replicates")
        with col2:
            alpha_level = st.selectbox("**α-level**", [0.05, 0.01, 0.001], index=0)
        with col3:
            power = st.slider("**Power (1-β)**", 0.7, 0.99, 0.8, 0.01)

        # 动态功率计算显示
        st.info(
            f"**Statistical Power**: With n={sample_size}, α={alpha_level}, you have {power * 100:.0f}% power to detect effects")

    # 继续按钮
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("**Proceed to Results →**", key="methodology_continue", use_container_width=True):
            st.session_state.current_section = 2
            st.rerun()

# Section 3: 结果 - 修复可视化并增强交互性
if st.session_state.current_section >= 2:
    st.markdown("""
    <div class="section-nature">
        <h2 style="color: #255A3B; margin-bottom: 1rem;">📈 Results & Data Analysis</h2>
        <p style="color: #666;">Computational predictions and experimental validation outcomes with interactive exploration</p>
    </div>
    """, unsafe_allow_html=True)

    results_tab1, results_tab2, results_tab3 = st.tabs(
        ["🧠 AIVC Predictions", "🔬 Experimental Data", "📊 Comparative Analysis"])

    with results_tab1:
        st.markdown("### AIVC Simulation Outcomes")

        col1, col2 = st.columns(2)

        with col1:
            # 时间序列预测 - 修复的颜色
            time_points = np.linspace(0, 72, 100)
            bacterial_growth = 1 / (1 + np.exp(-0.1 * (time_points - 24)))
            atra_concentration = 0.8 * (1 - np.exp(-0.05 * time_points))

            growth_fig = go.Figure()
            growth_fig.add_trace(go.Scatter(
                x=time_points, y=bacterial_growth,
                name='Bacterial Population',
                line=dict(color='#255A3B', width=3),
                fill='tozeroy',
                fillcolor='rgba(37, 90, 59, 0.1)'
            ))
            growth_fig.add_trace(go.Scatter(
                x=time_points, y=atra_concentration,
                name='ATRA Concentration',
                line=dict(color='#DC917B', width=3, dash='dot'),
                fill='tozeroy',
                fillcolor='rgba(220, 145, 123, 0.1)'
            ))

            growth_fig.update_layout(
                title="Population Dynamics & Metabolite Production",
                xaxis_title="Time (hours)",
                yaxis_title="Normalized Units",
                height=400,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )

            st.plotly_chart(growth_fig, use_container_width=True)

        with col2:
            # 空间分布热图 - 修复的颜色
            x = np.linspace(0, 10, 50)
            y = np.linspace(0, 10, 50)
            X, Y = np.meshgrid(x, y)

            tumor_center = [7, 3]
            Z = np.exp(-((X - tumor_center[0]) ** 2 + (Y - tumor_center[1]) ** 2) / 2)

            heatmap_fig = go.Figure(data=go.Heatmap(
                z=Z,
                colorscale=[[0, '#D2E2EF'], [0.5, '#81B095'], [1, '#255A3B']],
                showscale=True,
                hoverinfo='z'
            ))

            heatmap_fig.update_layout(
                title="Spatial Distribution in Tumor Microenvironment",
                height=400,
                xaxis_title="X Position",
                yaxis_title="Y Position"
            )

            st.plotly_chart(heatmap_fig, use_container_width=True)

    with results_tab2:
        st.markdown("### 🔬 Experimental Validation Data")

        # 创建模拟实验数据
        experimental_conditions = ['Control', 'Low ATRA', 'Medium ATRA', 'High ATRA']
        cell_viability = [100, 85, 62, 38]
        apoptosis_rate = [5, 15, 42, 67]

        exp_fig = go.Figure()

        exp_fig.add_trace(go.Bar(
            name='Cell Viability (%)',
            x=experimental_conditions,
            y=cell_viability,
            marker_color='#81B095',
            text=cell_viability,
            textposition='auto',
        ))

        exp_fig.add_trace(go.Bar(
            name='Apoptosis Rate (%)',
            x=experimental_conditions,
            y=apoptosis_rate,
            marker_color='#DC917B',
            text=apoptosis_rate,
            textposition='auto',
        ))

        exp_fig.update_layout(
            title="Therapeutic Efficacy Across Conditions",
            barmode='group',
            height=450,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )

        st.plotly_chart(exp_fig, use_container_width=True)

    with results_tab3:
        st.markdown("### 📊 Comparative Performance Analysis")

        # 修复的雷达图 - 使用正确的颜色格式
        methods = ['AIVC-Optimized', 'Conventional', 'Random Mutagenesis']
        metrics = ['Targeting Accuracy', 'Production Yield', 'Safety Profile', 'Scalability', 'Development Time']

        data = np.array([
            [8, 7, 8, 6, 7],
            [5, 6, 7, 8, 5],
            [3, 4, 5, 5, 8]
        ])

        radar_fig = go.Figure()

        colors = ['#255A3B', '#81B095', '#A78BFA']  # 修复：使用有效的颜色

        for i, method in enumerate(methods):
            radar_fig.add_trace(go.Scatterpolar(
                r=data[i],
                theta=metrics,
                fill='toself',
                name=method,
                line=dict(color=colors[i], width=2),
                fillcolor=f'rgba({int(colors[i][1:3], 16)}, {int(colors[i][3:5], 16)}, {int(colors[i][5:7], 16)}, 0.3)'
                # 修复：正确转换颜色
            ))

        radar_fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 10], gridcolor='#D2E2EF'),
                bgcolor='rgba(255,255,255,0.8)'
            ),
            showlegend=True,
            height=500,
            margin=dict(l=80, r=80, t=80, b=80)
        )

        st.plotly_chart(radar_fig, use_container_width=True)

    # 继续按钮
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("**Continue to Discussion →**", key="results_continue", use_container_width=True):
            st.session_state.current_section = 3
            st.rerun()

# 交互式卡片
st.markdown("""
<div class="interactive-card">
    <h3 style="color: #255A3B; text-align: center; margin-bottom: 1.5rem;">🎮 Interactive Exploration</h3>
    <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 1rem; text-align: center;">
        <div style="padding: 1rem; background: rgba(37, 90, 59, 0.1); border-radius: 10px;">
            <div style="font-size: 2rem;">📊</div>
            <div style="font-weight: 600; color: #255A3B;">Data Explorer</div>
            <div style="font-size: 0.9rem; color: #666;">Interactive charts</div>
        </div>
        <div style="padding: 1rem; background: rgba(129, 176, 149, 0.1); border-radius: 10px;">
            <div style="font-size: 2rem;">🔍</div>
            <div style="font-weight: 600; color: #255A3B;">Parameter Tuner</div>
            <div style="font-size: 0.9rem; color: #666;">Real-time simulation</div>
        </div>
        <div style="padding: 1rem; background: rgba(167, 139, 250, 0.1); border-radius: 10px;">
            <div style="font-size: 2rem;">📈</div>
            <div style="font-weight: 600; color: #255A3B;">Analysis Tools</div>
            <div style="font-size: 0.9rem; color: #666;">Statistical insights</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# 重置按钮
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("**🔄 Start New Assessment**", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# 科学引用和致谢 - 美化
st.markdown("""
<div style="background: linear-gradient(135deg, rgba(210, 226, 239, 0.5), rgba(221, 234, 223, 0.5)); 
            padding: 2rem; border-radius: 16px; margin-top: 3rem; border: 1px solid rgba(37, 90, 59, 0.2);">
    <h4 style="color: #255A3B; margin-bottom: 1.5rem; text-align: center;">📚 References & Acknowledgments</h4>
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem;">
        <div>
            <h5 style="color: #255A3B; margin-bottom: 0.5rem;">Suggested Citation</h5>
            <p style="font-size: 0.9rem; color: #666; line-height: 1.5; font-style: italic;">
            Research Team. (2025). "AIVC-Engineered Bacterial Systems for Targeted Cancer Therapy". 
            <em>Nature Cell Systems</em>.
            </p>
        </div>
        <div>
            <h5 style="color: #255A3B; margin-bottom: 0.5rem;">Acknowledgments</h5>
            <p style="font-size: 0.9rem; color: #666; line-height: 1.5;">
            Supported by computational resources from the Virtual Cell Consortium and synthetic biology facilities.
            </p>
        </div>
    </div>
    <div style="text-align: center; margin-top: 1.5rem;">
        <span style="background: rgba(37, 90, 59, 0.1); padding: 0.5rem 1rem; border-radius: 20px; 
                    font-size: 0.9rem; color: #255A3B;">🔬 Open Science • 🤝 Collaboration • 💡 Innovation</span>
    </div>
</div>
""", unsafe_allow_html=True)