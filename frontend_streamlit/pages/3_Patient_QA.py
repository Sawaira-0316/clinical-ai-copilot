import streamlit as st
from utils.helpers import load_css
from utils.state import initialize_state
from services.qa_service import ask_patient_question

st.set_page_config(page_title="Patient Q&A", page_icon="💬", layout="wide")

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
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.page-title {
    font-size: 2.2rem;
    font-weight: 800;
    color: #ffffff;
    margin-bottom: 0.35rem;
}
.page-subtitle {
    color: #cbd5e1;
    font-size: 1rem;
    margin-bottom: 1.5rem;
}
.badge {
    display: inline-block;
    padding: 0.4rem 1rem;
    border-radius: 999px;
    background: rgba(124, 58, 237, 0.14);
    border: 1px solid rgba(124, 58, 237, 0.35);
    color: #ddd6fe;
    font-size: 0.9rem;
    font-weight: 600;
    margin-bottom: 1.5rem;
}
.validation-card {
    background: linear-gradient(180deg, rgba(8,15,32,0.95), rgba(4,9,20,0.95));
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 18px;
    padding: 1.3rem 1.5rem;
    margin-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)

initialize_state()
load_css()

patient_id = st.session_state.get("selected_patient_id")

if not patient_id:
    st.warning("Please select a patient first.")
    if st.button("Go to Patients"):
        st.switch_page("pages/1_Patients.py")
    st.stop()

st.markdown('<div class="page-title">Patient Q&amp;A</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="page-subtitle">Ask grounded questions from uploaded patient records.</div>',
    unsafe_allow_html=True,
)

st.markdown(f'<div class="badge">Current Patient: {patient_id}</div>', unsafe_allow_html=True)

question = st.text_area(
    "Enter your clinical question",
    placeholder="Example: Summarize this patient's recent labs and mention any abnormalities.",
    height=140,
)

if "qa_history" not in st.session_state:
    st.session_state["qa_history"] = []

if st.button("Ask AI"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("🤖 AI Agent is thinking..."):
            result = ask_patient_question(patient_id, question)

        answer = result.get("answer", "No answer returned.")
        confidence = result.get("confidence", 0.0)
        sources = result.get("sources", [])

        st.session_state["qa_history"].insert(0, {
            "question": question,
            "answer": answer,
            "confidence": confidence,
            "sources": sources,
        })

if st.session_state["qa_history"]:
    for item in st.session_state["qa_history"]:
        st.markdown(
            f"""
            <div class="validation-card" style="margin-bottom:14px;">
                <div style="font-weight:800; color:#f5f7ff; margin-bottom:10px;">Question</div>
                <div style="color:#c9d0ff; margin-bottom:16px;">{item['question']}</div>
                <div style="font-weight:800; color:#f5f7ff; margin-bottom:10px;">Answer</div>
                <div style="color:#c9d0ff; line-height:1.9;">{item['answer']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if item.get("confidence"):
            st.progress(float(item["confidence"]))
            sources_text = ", ".join(item.get("sources", [])) or "Patient EHR"
            st.caption(f"🎯 Confidence: {float(item['confidence'])*100:.0f}% | 📚 Sources: {sources_text}")
        st.divider()