import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta
import json
import base64
import time

# 页面配置
st.set_page_config(
    page_title="SYPHU-CHINA iGEM - Inclusive Clinical Research",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 扩展的多语言支持
LANGUAGES = {
    "en": "English",
    "zh": "中文"
}

TEXTS = {
    "en": {
        # Header and General
        "title": "🌍 SYPHU-CHINA iGEM Inclusive Research Platform",
        "subtitle": "Diverse Participant Engagement for Global Health Innovation",
        "global_participation": "Global Participation",
        "accessibility_design": "Accessibility Designed",
        "diversity_inclusion": "Diversity & Inclusion",
        "data_protection": "Data Protection",
        "scientific_research": "Scientific Research",
        "team": "SYPHU-CHINA iGEM Team 2025",
        "data_promise_title": "🔒 Our Data Usage Promise",
        "data_promise": "We sincerely promise that all data collected through this platform will be used exclusively for the iGEM synthetic biology competition and related scientific research purposes.",
        "inclusive_research": "Inclusive Research Commitment",
        "diversity_statement": "We believe that medical research should represent all people.",

        # Navigation
        "progress": "Progress",
        "complete": "Complete",
        "next": "Next →",
        "previous": "← Previous",
        "submit": "Submit",
        "save": "Save Progress",
        "required": "Required *",

        # Steps
        "basic_info": "Basic Information",
        "medical_history": "Medical History",
        "symptoms": "Symptoms Assessment",
        "treatment": "Treatment Information",
        "research": "Research Participation",
        "completion": "Completion",
        "dashboard": "Live Dashboard",
        "analytics": "Data Analytics",
        "export": "Export Data",
        "consent": "Informed Consent",
        "demographics": "Demographic Details",
        "accessibility": "Accessibility Needs",

        # Form Labels - Basic Info
        "questionnaire_id": "Questionnaire ID",
        "survey_date": "Survey Date",
        "survey_method": "Survey Method",
        "gender": "Gender Identity",
        "birth_date": "Date of Birth",
        "height": "Height (cm)",
        "weight": "Weight (kg)",
        "education_level": "Highest Education",
        "occupation": "Employment Status",
        "income_level": "Annual Household Income",
        "ethnicity": "Ethnicity",
        "residence_type": "Residence Type",
        "region": "Region",

        # Options - Basic Info
        "survey_methods": ["Clinic Paper", "Ward Paper", "WeChat QR", "Phone", "Video Conference", "Other"],
        "genders": ["Male", "Female", "Non-binary", "Transgender", "Prefer not to say", "Other"],
        "education_levels": ["Primary School", "Middle School", "High School", "College", "Bachelor", "Master", "PhD",
                             "Other"],
        "occupations": ["Employed", "Retired", "Student", "Unemployed", "Homemaker", "Disabled", "Other"],
        "income_levels": ["Under 50k", "50k-100k", "100k-200k", "200k-500k", "500k-1M", "Over 1M", "Prefer not to say"],
        "ethnicities": ["Han", "Mongolian", "Hui", "Tibetan", "Uyghur", "Miao", "Other Minority"],
        "residence_types": ["Urban", "Town", "Rural", "Pastoral", "Other"],
        "regions": ["East China", "South China", "North China", "Central China", "Southwest", "Northwest", "Northeast",
                    "Hong Kong/Macao/Taiwan", "Overseas"],

        # Accessibility
        "accessibility_needs": "Accessibility Support Needs",
        "communication_preference": "Preferred Communication Methods",
        "accessibility_options": ["Visual Assistance", "Hearing Assistance", "Mobility Assistance", "Cognitive Support",
                                  "Language Translation", "Other", "No Needs"],
        "communication_options": ["Text", "Voice", "Video", "Face-to-face", "Email", "Phone", "Other"],

        # Medical History
        "diagnosis_date": "Diagnosis Date",
        "tumor_stage": "Tumor Stage",
        "diagnosis_location": "Diagnosis Hospital Type",
        "hepatitis_b": "Hepatitis B Infection",
        "hepatitis_c": "Hepatitis C Infection",
        "other_liver_disease": "Other Liver Diseases",
        "treatment_experience": "Previous Treatment Experience",
        "current_treatment": "Currently Receiving Treatment",

        # Medical Options
        "tumor_stages": ["Stage I", "Stage II", "Stage III", "Stage IV", "Unknown", "Initial Diagnosis"],
        "hospital_types": ["Tertiary Hospital", "Cancer Specialist Hospital", "City-level Hospital", "County Hospital",
                           "Private Hospital", "Overseas Hospital"],
        "yes_no_unknown": ["Yes", "No", "Unknown"],
        "liver_diseases": ["Fatty Liver", "Cirrhosis", "Autoimmune Liver Disease", "Alcoholic Liver Disease", "None",
                           "Other"],
        "treatments": ["Surgery", "Liver Transplant", "TACE", "Ablation Therapy", "Targeted Therapy", "Immunotherapy",
                       "Chemotherapy", "Radiotherapy", "Traditional Medicine", "Supportive Care", "No Treatment"],

        # Buttons and Messages
        "start_questionnaire": "Start Questionnaire →",
        "continue": "Continue",
        "thank_you": "Thank you for completing the questionnaire!",
        "consent_required": "Please agree to all terms to continue",
        "all_consent_required": "Please agree to all terms to submit the questionnaire"
    },
    "zh": {
        # Header and General
        "title": "🌍 SYPHU-CHINA iGEM 包容性研究平台",
        "subtitle": "多元化参与者参与，推动全球健康创新",
        "global_participation": "全球参与",
        "accessibility_design": "无障碍设计",
        "diversity_inclusion": "多元包容",
        "data_protection": "数据保护",
        "scientific_research": "科学研究",
        "team": "SYPHU-CHINA iGEM 团队 2025",
        "data_promise_title": "🔒 我们的数据使用承诺",
        "data_promise": "我们真诚承诺，通过本平台收集的所有数据将仅用于iGEM合成生物学竞赛及相关科学研究目的。",
        "inclusive_research": "包容性研究承诺",
        "diversity_statement": "我们相信医学研究应该代表所有人。",

        # Navigation
        "progress": "进度",
        "complete": "完成",
        "next": "下一步 →",
        "previous": "← 上一步",
        "submit": "提交",
        "save": "保存进度",
        "required": "必填 *",

        # Steps
        "basic_info": "基本信息",
        "medical_history": "疾病历史",
        "symptoms": "症状评估",
        "treatment": "治疗信息",
        "research": "研究参与",
        "completion": "完成问卷",
        "dashboard": "实时仪表盘",
        "analytics": "数据分析",
        "export": "导出数据",
        "consent": "知情同意",
        "demographics": "人口统计详情",
        "accessibility": "无障碍需求",

        # Form Labels - Basic Info
        "questionnaire_id": "问卷编号",
        "survey_date": "调查日期",
        "survey_method": "调查方式",
        "gender": "性别认同",
        "birth_date": "出生日期",
        "height": "身高 (cm)",
        "weight": "体重 (kg)",
        "education_level": "最高教育程度",
        "occupation": "职业状况",
        "income_level": "家庭年收入",
        "ethnicity": "民族",
        "residence_type": "居住类型",
        "region": "常住地区",

        # Options - Basic Info
        "survey_methods": ["门诊纸质", "病房纸质", "微信二维码", "电话", "视频会议", "其他"],
        "genders": ["男性", "女性", "非二元性别", "跨性别", "不愿透露", "其他"],
        "education_levels": ["小学", "初中", "高中", "大专", "本科", "硕士", "博士", "其他"],
        "occupations": ["在职", "退休", "学生", "失业", "家庭主妇/主夫", "残疾", "其他"],
        "income_levels": ["5万以下", "5-10万", "10-20万", "20-50万", "50-100万", "100万以上", "不愿透露"],
        "ethnicities": ["汉族", "蒙古族", "回族", "藏族", "维吾尔族", "苗族", "其他少数民族"],
        "residence_types": ["城市", "乡镇", "农村", "牧区", "其他"],
        "regions": ["华东", "华南", "华北", "华中", "西南", "西北", "东北", "港澳台", "海外"],

        # Accessibility
        "accessibility_needs": "无障碍支持需求",
        "communication_preference": "偏好的沟通方式",
        "accessibility_options": ["视觉辅助", "听觉辅助", "移动辅助", "认知支持", "语言翻译", "其他", "无需求"],
        "communication_options": ["文字", "语音", "视频", "面对面", "电子邮件", "电话", "其他"],

        # Medical History
        "diagnosis_date": "确诊日期",
        "tumor_stage": "肿瘤分期",
        "diagnosis_location": "确诊医院类型",
        "hepatitis_b": "乙肝感染",
        "hepatitis_c": "丙肝感染",
        "other_liver_disease": "其他肝脏疾病",
        "treatment_experience": "既往治疗经历",
        "current_treatment": "是否正在接受治疗",

        # Medical Options
        "tumor_stages": ["I期", "II期", "III期", "IV期", "不确定", "初次诊断"],
        "hospital_types": ["三甲医院", "肿瘤专科医院", "地市级医院", "县级医院", "私立医院", "海外医院"],
        "yes_no_unknown": ["是", "否", "不确定"],
        "liver_diseases": ["脂肪肝", "肝硬化", "自身免疫性肝病", "酒精性肝病", "无", "其他"],
        "treatments": ["手术切除", "肝移植", "TACE", "消融治疗", "靶向治疗", "免疫治疗", "化疗", "放疗", "中医治疗",
                       "支持治疗", "未治疗"],

        # Buttons and Messages
        "start_questionnaire": "开始问卷 →",
        "continue": "继续",
        "thank_you": "感谢您完成问卷！",
        "consent_required": "请同意所有条款以继续",
        "all_consent_required": "请确认所有条款以提交问卷"
    }
}

# 初始化session state
if 'language' not in st.session_state:
    st.session_state.language = "zh"
if 'current_step' not in st.session_state:
    st.session_state.current_step = 0
if 'form_data' not in st.session_state:
    st.session_state.form_data = {}
if 'consent_given' not in st.session_state:
    st.session_state.consent_given = False
if 'participants_data' not in st.session_state:
    # 模拟数据用于演示
    st.session_state.participants_data = pd.DataFrame({
        'id': range(1, 101),
        'region': np.random.choice(TEXTS['zh']['regions'], 100),
        'gender': np.random.choice(TEXTS['zh']['genders'], 100),
        'age': np.random.randint(18, 80, 100),
        'tumor_stage': np.random.choice(TEXTS['zh']['tumor_stages'], 100),
        'completion_date': [datetime.now() - timedelta(days=x) for x in np.random.randint(1, 30, 100).tolist()]    })

# 动态CSS样式
st.markdown("""
<style>
    /* 包容性设计配色 */
    :root {
        --primary-blue: #1f77b4;
        --primary-green: #2ca02c;
        --primary-orange: #ff7f0e;
        --primary-red: #d62728;
        --primary-purple: #9467bd;
        --accessibility-yellow: #ffd700;
        --inclusion-teal: #17becf;
        --diversity-pink: #e377c2;
    }

    .inclusive-header {
        background: linear-gradient(135deg, var(--primary-blue), var(--inclusion-teal), var(--primary-green));
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
        padding: 3rem 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        position: relative;
        overflow: hidden;
    }

    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* 修复徽章样式 */
    .diversity-badge {
        background: linear-gradient(135deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4, #feca57);
        background-size: 400% 400%;
        animation: gradientShift 8s ease infinite;
        color: white;
        padding: 0.8rem 1.5rem;
        border-radius: 25px;
        font-size: 0.9rem;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        margin: 0.3rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        border: 2px solid rgba(255,255,255,0.3);
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
        min-width: 120px;
        justify-content: center;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }

    .diversity-badge:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
    }

    .badge-container {
        display: flex;
        justify-content: center;
        gap: 0.8rem;
        margin-top: 1.5rem;
        flex-wrap: wrap;
        padding: 1rem;
    }

    .promise-banner {
        background: linear-gradient(135deg, var(--primary-green), var(--inclusion-teal));
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border-left: 6px solid var(--accessibility-yellow);
        box-shadow: 0 8px 25px rgba(44, 160, 44, 0.2);
    }

    .inclusive-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        padding: 2.5rem;
        border-radius: 20px;
        margin: 1.5rem 0;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        border: 2px solid transparent;
        background-clip: padding-box;
        position: relative;
        transition: all 0.3s ease;
    }

    .inclusive-card::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        border-radius: 20px;
        padding: 2px;
        background: linear-gradient(135deg, var(--primary-blue), var(--primary-green), var(--primary-orange));
        -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
        -webkit-mask-composite: xor;
        mask-composite: exclude;
        z-index: -1;
    }

    .inclusive-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.15);
    }

    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, var(--primary-blue), var(--inclusion-teal), var(--primary-green));
        background-size: 200% 100%;
        animation: gradientShift 3s ease infinite;
    }

    .stButton > button {
        background: linear-gradient(135deg, var(--primary-blue), var(--primary-green));
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 50px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(31, 119, 180, 0.4);
    }

    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(31, 119, 180, 0.6);
    }
</style>
""", unsafe_allow_html=True)

# 语言切换器
col1, col2, col3 = st.columns([3, 1, 1])
with col3:
    language = st.radio(
        "🌐",
        ["中文", "English"],
        horizontal=True,
        index=0 if st.session_state.language == "zh" else 1,
        label_visibility="collapsed",
        key="language_selector"
    )
    # 当语言切换时，更新session state
    new_language = "zh" if language == "中文" else "en"
    if new_language != st.session_state.language:
        st.session_state.language = new_language
        st.rerun()

texts = TEXTS[st.session_state.language]

# 修复后的包容性Header
st.markdown(f"""
<div class="inclusive-header">
    <h1 style="font-size: 3rem; margin-bottom: 0.5rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">{texts['title']}</h1>
    <h2 style="font-size: 1.5rem; font-weight: 300; margin-bottom: 1rem; opacity: 0.9;">{texts['subtitle']}</h2>
</div>
""", unsafe_allow_html=True)

# 修复后的徽章容器
st.markdown(f"""
<div class="badge-container">
    <div class="diversity-badge">🌍 {texts['global_participation']}</div>
    <div class="diversity-badge">♿ {texts['accessibility_design']}</div>
    <div class="diversity-badge">🌈 {texts['diversity_inclusion']}</div>
    <div class="diversity-badge">🔒 {texts['data_protection']}</div>
    <div class="diversity-badge">🎯 {texts['scientific_research']}</div>
</div>
""", unsafe_allow_html=True)

# 数据使用承诺横幅
st.markdown(f"""
<div class="promise-banner">
    <h3 style="margin: 0 0 1rem 0; display: flex; align-items: center; gap: 0.5rem;">
        <span>🤝</span> {texts['data_promise_title']}
    </h3>
    <p style="margin: 0; font-size: 1rem; line-height: 1.6;">{texts['data_promise']}</p>
</div>
""", unsafe_allow_html=True)

# 主内容区域
tab1, tab2, tab3 = st.tabs(["📝 " + texts['basic_info'], "📊 " + texts['dashboard'], "🔍 Research Transparency"])

with tab1:
    # 进度指示器
    steps = [texts['basic_info'], texts['medical_history'], texts['symptoms'],
             texts['treatment'], texts['research'], texts['completion']]

    progress_percent = (st.session_state.current_step / (len(steps) - 1)) * 100 if len(steps) > 1 else 0

    progress_html = f"""
    <div style="background: rgba(248, 249, 250, 0.8); padding: 2rem; border-radius: 15px; margin-bottom: 2rem; backdrop-filter: blur(10px);">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
            <span style="color: #1f77b4; font-weight: 600; font-size: 1.1rem;">{texts['progress']}</span>
            <span style="background: #1f77b4; color: white; padding: 0.3rem 1rem; border-radius: 20px; font-size: 0.9rem;">
                {st.session_state.current_step + 1} / {len(steps)}
            </span>
        </div>

        <div style="background: #e9ecef; height: 12px; border-radius: 8px; overflow: hidden; position: relative;">
            <div style="background: linear-gradient(90deg, #1f77b4, #2ca02c, #ff7f0e); 
                        width: {progress_percent}%; 
                        height: 100%; transition: width 0.8s ease; border-radius: 8px;"></div>
        </div>

        <div style="display: flex; justify-content: space-between; margin-top: 1rem; font-size: 0.9rem;">
            {''.join([f'<span style="color: {"#1f77b4" if i <= st.session_state.current_step else "#999"}; font-weight: {"600" if i == st.session_state.current_step else "400"}; text-align: center; flex: 1;">{step}</span>' for i, step in enumerate(steps)])}
        </div>
    </div>
    """
    st.markdown(progress_html, unsafe_allow_html=True)

    # 步骤1: 知情同意
    if st.session_state.current_step == 0:
        st.markdown(f"""
        <div class="inclusive-card">
            <h2 style="color: #1f77b4; margin-bottom: 1.5rem;">🤝 {texts['consent']}</h2>
            <p style="color: #666; margin-bottom: 2rem;">{texts['inclusive_research']}</p>
        </div>
        """, unsafe_allow_html=True)

        with st.form("informed_consent"):
            st.markdown("### 📋 Research Participation Agreement")

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("""
                #### Research Purpose
                - Advance scientific research in liver cancer treatment
                - Provide real-world data for iGEM competition
                - Promote global innovation in healthcare

                #### Your Rights
                - Right to withdraw from the study at any time
                - Right to access your personal data
                - Right to ask questions and raise concerns
                """)

            with col2:
                st.markdown("""
                #### Data Protection
                - All data will be anonymized
                - Data used only for scientific research
                - Strict data security measures

                #### Benefits & Risks
                - Contribute to medical advancement
                - May not receive direct medical benefits
                - Privacy risks minimized
                """)

            # 包容性承诺
            st.markdown("---")
            st.markdown("### 🌈 Our Inclusive Commitment")
            st.markdown(texts['diversity_statement'])

            # 同意选项
            st.markdown("---")
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                consent_1 = st.checkbox("**I understand the research purpose and process**", value=False)
                consent_2 = st.checkbox("**I agree to participate in this research**", value=False)
                consent_3 = st.checkbox("**I understand the data usage promise**", value=False)
                consent_4 = st.checkbox("**I confirm I am 18 years or older**", value=False)

            if st.form_submit_button(f"**{texts['start_questionnaire']}**"):
                if all([consent_1, consent_2, consent_3, consent_4]):
                    st.session_state.consent_given = True
                    st.session_state.current_step = 1
                    st.rerun()
                else:
                    st.error(texts['consent_required'])

    # 步骤2: 扩展的基本信息
    elif st.session_state.current_step == 1:
        st.markdown(f"""
        <div class="inclusive-card">
            <h2 style="color: #1f77b4; margin-bottom: 1.5rem;">👥 {texts['demographics']}</h2>
            <p style="color: #666; margin-bottom: 2rem;">We value everyone's unique experiences and backgrounds</p>
        </div>
        """, unsafe_allow_html=True)

        with st.form("extended_demographics"):
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("📋 Basic Identity Information")
                questionnaire_id = st.text_input(f"{texts['questionnaire_id']} *", placeholder="A001")
                survey_date = st.date_input(f"{texts['survey_date']} *", datetime.now())
                survey_method = st.selectbox(f"{texts['survey_method']} *", texts['survey_methods'])

                # 扩展的人口统计信息
                st.subheader("👤 Identity Characteristics")
                gender = st.selectbox(f"{texts['gender']} *", texts['genders'])
                birth_date = st.date_input(f"{texts['birth_date']} *", datetime(1980, 1, 1))

                # 计算年龄
                age = datetime.now().year - birth_date.year
                st.info(f"**Age**: {age} years")

            with col2:
                st.subheader("🏠 Socioeconomic Background")
                education_level = st.selectbox(texts['education_level'], texts['education_levels'])
                occupation = st.selectbox(texts['occupation'], texts['occupations'])
                income_level = st.selectbox(texts['income_level'], texts['income_levels'])

                st.subheader("🌍 Cultural Background")
                ethnicity = st.selectbox(texts['ethnicity'], texts['ethnicities'])
                residence_type = st.selectbox(texts['residence_type'], texts['residence_types'])
                region = st.selectbox(f"{texts['region']} *", texts['regions'])

            # 无障碍需求部分
            st.markdown("---")
            st.markdown(f"### ♿ {texts['accessibility']}")
            col3, col4 = st.columns(2)

            with col3:
                accessibility_needs = st.multiselect(
                    texts['accessibility_needs'],
                    texts['accessibility_options']
                )

            with col4:
                preferred_communication = st.multiselect(
                    texts['communication_preference'],
                    texts['communication_options']
                )

            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                if st.form_submit_button(f"**{texts['next']}**"):
                    if questionnaire_id:
                        st.session_state.form_data.update({
                            'questionnaire_id': questionnaire_id,
                            'demographics': {
                                'gender': gender,
                                'birth_date': str(birth_date),
                                'education': education_level,
                                'occupation': occupation,
                                'income': income_level,
                                'ethnicity': ethnicity,
                                'residence': residence_type,
                                'region': region,
                                'accessibility_needs': accessibility_needs,
                                'communication_preference': preferred_communication
                            }
                        })
                        st.session_state.current_step = 2
                        st.rerun()
                    else:
                        st.error("Please enter a Questionnaire ID")

    # 步骤3: 扩展的医疗信息
    elif st.session_state.current_step == 2:
        st.markdown(f"""
        <div class="inclusive-card">
            <h2 style="color: #1f77b4; margin-bottom: 1.5rem;">🏥 {texts['medical_history']}</h2>
            <p style="color: #666; margin-bottom: 2rem;">Comprehensive health status assessment</p>
        </div>
        """, unsafe_allow_html=True)

        with st.form("extended_medical_history"):
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("🩺 Liver Cancer Diagnosis Information")
                diagnosis_date = st.date_input(f"{texts['diagnosis_date']} *", datetime.now())
                tumor_stage = st.selectbox(f"{texts['tumor_stage']} *", texts['tumor_stages'])
                diagnosis_location = st.selectbox(texts['diagnosis_location'], texts['hospital_types'])

                st.subheader("🦠 Hepatitis and Liver Health")
                has_hepatitis_b = st.radio(f"{texts['hepatitis_b']} *", texts['yes_no_unknown'])
                if has_hepatitis_b == texts['yes_no_unknown'][0]:  # "Yes"
                    hbv_treatment = st.radio("HBV Antiviral Treatment", texts['yes_no_unknown'])
                    hbv_duration = st.number_input("Years of HBV History", min_value=0, max_value=50, value=5)

                has_hepatitis_c = st.radio(f"{texts['hepatitis_c']} *", texts['yes_no_unknown'])
                other_liver_disease = st.multiselect(texts['other_liver_disease'], texts['liver_diseases'])

            with col2:
                st.subheader("💊 Treatment Experience")
                treatment_experience = st.multiselect(
                    f"{texts['treatment_experience']} *",
                    texts['treatments']
                )

                st.subheader("🔬 Current Treatment Status")
                current_treatment = st.radio(f"{texts['current_treatment']} *", texts['yes_no_unknown'])
                if current_treatment == texts['yes_no_unknown'][0]:  # "Yes"
                    treatment_types = st.multiselect("Current Treatment Methods",
                                                     ["Targeted Drugs", "Immunotherapy", "Chemotherapy", "Radiation",
                                                      "Interventional", "Other"])
                    treatment_duration = st.number_input("Current Treatment Duration (months)", min_value=1,
                                                         max_value=120, value=6)
                    monthly_cost = st.selectbox("Monthly Treatment Cost",
                                                ["Under 10k", "10k-30k", "30k-50k", "50k-100k", "Over 100k",
                                                 "Insurance Covered"])

            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                if st.form_submit_button(f"**{texts['next']}**"):
                    st.session_state.current_step = 3
                    st.rerun()

    # 步骤4: 症状评估（简化版）
    elif st.session_state.current_step == 3:
        st.markdown(f"""
        <div class="inclusive-card">
            <h2 style="color: #1f77b4; margin-bottom: 1.5rem;">📊 {texts['symptoms']}</h2>
            <p style="color: #666; margin-bottom: 2rem;">Please rate your symptoms over the past week</p>
        </div>
        """, unsafe_allow_html=True)

        with st.form("symptoms_assessment"):
            st.subheader("🩺 Symptom Severity (1-10 scale)")

            col1, col2 = st.columns(2)

            with col1:
                fatigue = st.slider("Fatigue", 1, 10, 5)
                pain = st.slider("Pain", 1, 10, 3)
                nausea = st.slider("Nausea", 1, 10, 2)

            with col2:
                appetite = st.slider("Appetite Loss", 1, 10, 4)
                sleep = st.slider("Sleep Disturbance", 1, 10, 3)
                mobility = st.slider("Mobility Issues", 1, 10, 2)

            st.subheader("📝 Additional Symptoms")
            additional_symptoms = st.multiselect(
                "Select any additional symptoms you've experienced:",
                ["Weight Loss", "Fever", "Jaundice", "Abdominal Swelling", "Shortness of Breath", "Other"]
            )

            other_symptoms = st.text_area("Please describe any other symptoms:")

            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                if st.form_submit_button(f"**{texts['next']}**"):
                    st.session_state.form_data['symptoms'] = {
                        'fatigue': fatigue,
                        'pain': pain,
                        'nausea': nausea,
                        'appetite': appetite,
                        'sleep': sleep,
                        'mobility': mobility,
                        'additional_symptoms': additional_symptoms,
                        'other_symptoms': other_symptoms
                    }
                    st.session_state.current_step = 4
                    st.rerun()

    # 步骤5: 研究参与
    elif st.session_state.current_step == 4:
        st.markdown(f"""
        <div class="inclusive-card">
            <h2 style="color: #1f77b4; margin-bottom: 1.5rem;">🔬 {texts['research']}</h2>
            <p style="color: #666; margin-bottom: 2rem;">Your contribution to scientific advancement</p>
        </div>
        """, unsafe_allow_html=True)

        with st.form("research_participation"):
            st.subheader("📋 Future Research Opportunities")

            col1, col2 = st.columns(2)

            with col1:
                future_contact = st.radio(
                    "Would you be willing to be contacted for future research studies?",
                    ["Yes", "No", "Maybe"]
                )

                sample_collection = st.radio(
                    "Would you consider providing biological samples (e.g., blood, tissue) for research?",
                    ["Yes", "No", "Need more information"]
                )

            with col2:
                data_sharing = st.radio(
                    "Would you allow your anonymized data to be shared with other researchers?",
                    ["Yes, fully anonymized", "Yes, with restrictions", "No"]
                )

                follow_up = st.radio(
                    "Would you participate in follow-up surveys?",
                    ["Yes", "No", "Depends on timing"]
                )

            suggestions = st.text_area("Any suggestions for improving our research or this platform:")

            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                if st.form_submit_button(f"**{texts['next']}**"):
                    st.session_state.form_data['research'] = {
                        'future_contact': future_contact,
                        'sample_collection': sample_collection,
                        'data_sharing': data_sharing,
                        'follow_up': follow_up,
                        'suggestions': suggestions
                    }
                    st.session_state.current_step = 5
                    st.rerun()

    # 步骤6: 完成
    elif st.session_state.current_step == 5:
        st.markdown(f"""
        <div class="inclusive-card">
            <h2 style="color: #1f77b4; margin-bottom: 1.5rem;">🎉 {texts['completion']}</h2>
            <p style="color: #666; margin-bottom: 2rem;">Thank you for your valuable contribution to research</p>
        </div>
        """, unsafe_allow_html=True)

        st.success("### ✅ " + texts['thank_you'])

        # 显示提交的数据摘要
        st.subheader("📋 Your Submitted Information")

        if 'demographics' in st.session_state.form_data:
            with st.expander("Demographic Information"):
                st.json(st.session_state.form_data['demographics'])

        if 'symptoms' in st.session_state.form_data:
            with st.expander("Symptoms Assessment"):
                st.json(st.session_state.form_data['symptoms'])

        if 'research' in st.session_state.form_data:
            with st.expander("Research Preferences"):
                st.json(st.session_state.form_data['research'])

        # 提交按钮
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button(f"**{texts['submit']}**", type="primary", use_container_width=True):
                # 在实际应用中，这里会将数据保存到数据库
                st.balloons()
                st.success("### 🎉 Your response has been recorded!")
                st.info("Your data will contribute to important research in liver cancer treatment.")

                # 重置表单
                time.sleep(2)
                st.session_state.current_step = 0
                st.session_state.form_data = {}
                st.rerun()

    # 导航按钮（除了第一步和最后一步）
    if st.session_state.current_step > 0 and st.session_state.current_step < 5:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            if st.button(f"**{texts['previous']}**", use_container_width=True):
                st.session_state.current_step -= 1
                st.rerun()

with tab2:
    # 实时仪表盘
    st.markdown(f"""
    <div class="inclusive-card">
        <h2 style="color: #1f77b4; margin-bottom: 1.5rem;">📊 {texts['dashboard']}</h2>
        <p style="color: #666; margin-bottom: 2rem;">Real-time data visualization and research metrics</p>
    </div>
    """, unsafe_allow_html=True)

    # 实时指标
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Participants", "156", "+12")
    with col2:
        st.metric("Completion Rate", "92%", "+3%")
    with col3:
        st.metric("Active Today", "23", "+5")
    with col4:
        st.metric("Ethnic Diversity", "8+", "ethnicities")

    # 数据可视化
    st.subheader("📈 Participation Analytics")

    col1, col2 = st.columns(2)

    with col1:
        # 地区分布图
        region_counts = st.session_state.participants_data['region'].value_counts()
        fig1 = px.pie(
            values=region_counts.values,
            names=region_counts.index,
            title="Regional Distribution of Participants"
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        # 肿瘤分期分布
        stage_counts = st.session_state.participants_data['tumor_stage'].value_counts()
        fig2 = px.bar(
            x=stage_counts.index,
            y=stage_counts.values,
            title="Tumor Stage Distribution",
            labels={'x': 'Tumor Stage', 'y': 'Count'}
        )
        st.plotly_chart(fig2, use_container_width=True)

    # 时间趋势图
    st.subheader("📅 Participation Over Time")
    daily_counts = st.session_state.participants_data.groupby(
        st.session_state.participants_data['completion_date'].dt.date
    ).size().reset_index(name='count')

    fig3 = px.line(
        daily_counts,
        x='completion_date',
        y='count',
        title="Daily Participation Trend"
    )
    st.plotly_chart(fig3, use_container_width=True)

with tab3:
    # 研究透明度
    st.markdown(f"""
    <div class="inclusive-card">
        <h2 style="color: #1f77b4; margin-bottom: 1.5rem;">🔍 Research Transparency</h2>
        <p style="color: #666; margin-bottom: 2rem;">Open and transparent research data management</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Data Usage Statistics")
        st.metric("Data Points Collected", "15,642")
        st.metric("Research Questions Answered", "42")
        st.metric("Publications Supported", "3")

    with col2:
        st.subheader("🔒 Privacy & Ethics")
        st.info("""
        - All data is fully anonymized
        - IRB approval: SYPHU-2025-IGEM-001
        - Regular security audits conducted
        - Compliance with GDPR and local regulations
        """)

    st.subheader("📋 Data Export Options")

    export_format = st.selectbox("Select export format:", ["CSV", "JSON", "Excel"])

    if st.button("Generate Export"):
        with st.spinner("Preparing your data export..."):
            time.sleep(2)
            st.success("Export ready! This would download the data in production.")

# 页脚
st.markdown("---")
footer_col1, footer_col2 = st.columns([3, 1])

with footer_col1:
    st.markdown(f"""
    <div style="text-align: center; color: #666; padding: 2rem;">
        <h4 style="color: #1f77b4;">{texts['team']}</h4>
        <p><strong>Inclusive Research Commitment:</strong> We are committed to enabling everyone to participate in scientific research, regardless of age, gender, ethnicity, ability, or background.</p>
        <div class="badge-container" style="margin: 1rem 0;">
            <div class="diversity-badge" style="background: linear-gradient(135deg, #ff6b6b, #ee5a24);">🔬 Scientific Research</div>
            <div class="diversity-badge" style="background: linear-gradient(135deg, #4ecdc4, #00b894);">🤝 Ethical Compliance</div>
            <div class="diversity-badge" style="background: linear-gradient(135deg, #45b7d1, #0984e3);">🌍 Global Collaboration</div>
        </div>
    </div>
    """, unsafe_allow_html=True)