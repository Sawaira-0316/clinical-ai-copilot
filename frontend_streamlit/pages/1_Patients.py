import streamlit as st
from components.patient_card import render_patient_card
from utils.helpers import load_css
from utils.state import initialize_state
from services.patients_service import get_patients

st.set_page_config(page_title="Patients", page_icon="👥", layout="wide")

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
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

initialize_state()
load_css()

st.markdown('<div class="page-title">Patients</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="page-subtitle">Browse patients, search records, and open a patient for detailed review.</div>',
    unsafe_allow_html=True,
)

search = st.text_input("🔍 Search patients by name")

all_patients = get_patients()

if search:
    patients = [p for p in all_patients if search.lower() in p.get("name", "").lower()]
else:
    patients = all_patients

if not patients:
    st.warning("No patients found.")
else:
    for patient in patients:
        render_patient_card(patient)
        col1, col2 = st.columns([1, 5])
        with col1:
            if st.button("📋 Open Details", key=f"open_{patient['patient_id']}"):
                st.session_state["selected_patient_id"] = patient["patient_id"]
                st.switch_page("pages/2_Patient_Detail.py")