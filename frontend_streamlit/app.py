import streamlit as st

st.set_page_config(
    page_title="Clinical AI Copilot",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

if "show_features" not in st.session_state:
    st.session_state.show_features = False

st.markdown("""
<style>
.stApp {
    background: linear-gradient(180deg, #020817 0%, #030b1f 40%, #020617 100%);
    color: #f8fafc;
}
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1400px;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #041127 0%, #020817 100%);
    border-right: 1px solid rgba(255,255,255,0.06);
}
[data-testid="stSidebar"] * {
    color: #e5e7eb !important;
}
div[data-testid="stVerticalBlock"] div:has(> div[data-testid="stMarkdownContainer"]) {
    background: transparent;
}
.hero-card {
    background: linear-gradient(135deg, rgba(10,18,40,0.96), rgba(6,10,24,0.92));
    border: 1px solid rgba(124, 58, 237, 0.18);
    border-radius: 28px;
    padding: 2.2rem 2rem;
    box-shadow: 0 10px 30px rgba(0,0,0,0.35);
    margin-bottom: 1.8rem;
}
.hero-title {
    font-size: 3.4rem;
    font-weight: 800;
    color: white;
    line-height: 1.1;
    margin-bottom: 0.8rem;
}
.gradient-text {
    background: linear-gradient(90deg, #8b5cf6, #7c3aed, #38bdf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero-subtitle {
    font-size: 1.08rem;
    color: #cbd5e1;
    line-height: 1.8;
    max-width: 850px;
    margin-bottom: 1.5rem;
}
.pill {
    display: inline-block;
    padding: 0.6rem 1rem;
    border-radius: 999px;
    background: rgba(124, 58, 237, 0.14);
    border: 1px solid rgba(124, 58, 237, 0.35);
    color: #ddd6fe;
    font-size: 0.92rem;
    font-weight: 600;
    margin-bottom: 1rem;
}
div.stButton > button {
    background: rgba(255,255,255,0.03);
    color: #e2e8f0;
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 14px;
    padding: 0.85rem 1.3rem;
    font-weight: 600;
    font-size: 0.95rem;
    height: auto;
}
div.stButton > button:hover {
    border: 1px solid rgba(124, 58, 237, 0.45);
    color: white;
}
.metric-card {
    background: linear-gradient(180deg, rgba(8,15,32,0.95), rgba(4,9,20,0.95));
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 22px;
    padding: 1.2rem 1.1rem;
    box-shadow: 0 8px 20px rgba(0,0,0,0.25);
    height: 100%;
}
.metric-label {
    color: #94a3b8;
    font-size: 0.92rem;
    margin-bottom: 0.4rem;
}
.metric-value {
    color: white;
    font-size: 2rem;
    font-weight: 800;
}
.metric-note {
    color: #a78bfa;
    font-size: 0.9rem;
    margin-top: 0.35rem;
}
.section-title {
    font-size: 1.65rem;
    font-weight: 700;
    color: white;
    margin: 0.5rem 0 1rem 0;
}
.feature-card {
    background: linear-gradient(180deg, rgba(8,15,32,0.95), rgba(4,9,20,0.95));
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 22px;
    padding: 1.3rem;
    min-height: 210px;
    box-shadow: 0 10px 24px rgba(0,0,0,0.28);
    transition: 0.25s ease;
}
.feature-card:hover {
    transform: translateY(-4px);
    border: 1px solid rgba(124, 58, 237, 0.30);
}
.feature-icon {
    font-size: 1.8rem;
    margin-bottom: 0.75rem;
}
.feature-title {
    color: white;
    font-size: 1.15rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
}
.feature-text {
    color: #cbd5e1;
    line-height: 1.65;
    font-size: 0.95rem;
}
.workflow-card {
    background: linear-gradient(135deg, rgba(12,20,42,0.96), rgba(4,9,20,0.96));
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 24px;
    padding: 1.5rem;
    margin-top: 1rem;
}
.step-box {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 18px;
    padding: 1rem;
    height: 100%;
}
.step-number {
    display: inline-block;
    width: 34px;
    height: 34px;
    line-height: 34px;
    text-align: center;
    border-radius: 50%;
    background: linear-gradient(90deg, #7c3aed, #2563eb);
    color: white;
    font-weight: 700;
    margin-bottom: 0.8rem;
}
.step-title {
    color: white;
    font-weight: 700;
    margin-bottom: 0.4rem;
}
.step-text {
    color: #cbd5e1;
    font-size: 0.93rem;
    line-height: 1.6;
}
.bottom-banner {
    margin-top: 1.8rem;
    background: linear-gradient(90deg, rgba(124,58,237,0.15), rgba(37,99,235,0.12));
    border: 1px solid rgba(124,58,237,0.22);
    border-radius: 24px;
    padding: 1.4rem;
    color: #e2e8f0;
}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero-card">
    <div class="pill">Powered by Clinical AI + Multi-File RAG + Human Review</div>
    <div class="hero-title">
        Review Patient Data Faster with <span class="gradient-text">ClinicalAI Copilot</span>
    </div>
    <div class="hero-subtitle">
        A production-ready healthcare AI assistant that helps clinicians upload patient datasets,
        explore longitudinal timelines, generate AI-powered summaries, detect important alerts,
        and ask evidence-based clinical questions from one unified dashboard.
    </div>
</div>
""", unsafe_allow_html=True)

cta1, cta2, _ = st.columns([1.3, 1.1, 4])

with cta1:
    if st.button("Upload Patient Dataset", key="upload_patient_dataset_btn", use_container_width=True):
        st.switch_page("pages/4_Knowledge_Base.py")

with cta2:
    if st.button("Explore Features", key="explore_features_btn", use_container_width=True):
        st.session_state.show_features = True

st.markdown('<div class="section-title">Clinical Workflow Snapshot</div>', unsafe_allow_html=True)

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">Datasets Uploaded</div>
        <div class="metric-value">24</div>
        <div class="metric-note">Multi-format ingestion ready</div>
    </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">Patient Timelines</div>
        <div class="metric-value">128</div>
        <div class="metric-note">Longitudinal review enabled</div>
    </div>
    """, unsafe_allow_html=True)

with m3:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">AI Summaries Generated</div>
        <div class="metric-value">96</div>
        <div class="metric-note">Structured clinical summaries</div>
    </div>
    """, unsafe_allow_html=True)

with m4:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">Active Alerts</div>
        <div class="metric-value">12</div>
        <div class="metric-note">Review flags detected</div>
    </div>
    """, unsafe_allow_html=True)

if st.session_state.show_features:
    st.markdown('<div class="section-title" style="margin-top:1.8rem;">Core Features</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📂</div>
            <div class="feature-title">Upload Patient Dataset</div>
            <div class="feature-text">
                Upload CSV, Excel, JSON, or text-based clinical files and transform fragmented records
                into a structured patient-centric workflow.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📈</div>
            <div class="feature-title">View Patient Timeline</div>
            <div class="feature-text">
                Track labs, vitals, medications, and notes in a longitudinal timeline so clinicians
                can understand changes over time more clearly.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🧠</div>
            <div class="feature-title">Generate AI Summary</div>
            <div class="feature-text">
                Automatically create concise clinical summaries that help reduce chart review time and
                provide a faster overview of patient status.
            </div>
        </div>
        """, unsafe_allow_html=True)

    c4, c5, c6 = st.columns(3)

    with c4:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">❓</div>
            <div class="feature-title">Ask Clinical Question</div>
            <div class="feature-text">
                Ask grounded clinical questions and receive evidence-based answers using RAG-powered
                retrieval from the patient record and knowledge base.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c5:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🚨</div>
            <div class="feature-title">Alerts & Review Flags</div>
            <div class="feature-text">
                Detect abnormal values, high-risk patterns, and important review signals so clinicians
                can focus quickly on what needs attention.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c6:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">👨‍⚕️</div>
            <div class="feature-title">Human-in-the-Loop Review</div>
            <div class="feature-text">
                Keep clinicians in control with review-first workflows that support medical judgment
                rather than replacing it.
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('<div class="section-title" style="margin-top:1.8rem;">How It Works</div>', unsafe_allow_html=True)

st.markdown('<div class="workflow-card">', unsafe_allow_html=True)
w1, w2, w3, w4, w5 = st.columns(5)

with w1:
    st.markdown("""
    <div class="step-box">
        <div class="step-number">1</div>
        <div class="step-title">Upload</div>
        <div class="step-text">
            Import patient datasets from multiple supported formats.
        </div>
    </div>
    """, unsafe_allow_html=True)

with w2:
    st.markdown("""
    <div class="step-box">
        <div class="step-number">2</div>
        <div class="step-title">Process</div>
        <div class="step-text">
            Normalize records and build structured patient context.
        </div>
    </div>
    """, unsafe_allow_html=True)

with w3:
    st.markdown("""
    <div class="step-box">
        <div class="step-number">3</div>
        <div class="step-title">Summarize</div>
        <div class="step-text">
            Generate AI clinical summaries for rapid review.
        </div>
    </div>
    """, unsafe_allow_html=True)

with w4:
    st.markdown("""
    <div class="step-box">
        <div class="step-number">4</div>
        <div class="step-title">Ask</div>
        <div class="step-text">
            Query patient data with evidence-based clinical questions.
        </div>
    </div>
    """, unsafe_allow_html=True)

with w5:
    st.markdown("""
    <div class="step-box">
        <div class="step-number">5</div>
        <div class="step-title">Review</div>
        <div class="step-text">
            Validate alerts and insights with clinician oversight.
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<div class="bottom-banner">
    <b>Clinical AI Copilot</b> is designed for clinical workflow assistance only.
    It helps clinicians review data faster, identify key patterns, and interact with
    patient information more efficiently — while keeping final medical judgment with qualified professionals.
</div>
""", unsafe_allow_html=True)