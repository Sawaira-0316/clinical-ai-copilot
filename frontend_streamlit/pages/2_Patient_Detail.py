import streamlit as st
import pandas as pd
from components.patient_card import render_patient_card
from components.metric_card import render_metric_card
from components.tables import render_dark_table
from utils.helpers import load_css
from utils.state import initialize_state
from services.patients_service import get_patient_by_id
from services.timeline_service import get_patient_timeline
from services.notes_service import get_patient_notes
from services.labs_service import get_patient_labs
from services.vitals_service import get_patient_vitals
from services.medications_service import get_patient_medications
from services.summary_service import get_patient_summary
from services.alerts_service import get_patient_alerts
from components.metric_card import render_metric_card

st.set_page_config(page_title="Patient Detail", page_icon="🧾", layout="wide")

st.markdown("""
<style>
/* Global app background */
.stApp {
    background: linear-gradient(180deg, #020817 0%, #030b1f 40%, #020617 100%);
    color: #f8fafc;
}

/* Main block */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1400px;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #041127 0%, #020817 100%);
    border-right: 1px solid rgba(255,255,255,0.06);
}

[data-testid="stSidebar"] * {
    color: #e5e7eb !important;
}

/* Remove default white backgrounds */
div[data-testid="stVerticalBlock"] div:has(> div[data-testid="stMarkdownContainer"]) {
    background: transparent;
}

/* Hide default Streamlit chrome */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
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

patient = get_patient_by_id(patient_id)

st.markdown('<div class="page-title">Patient Detail</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="page-subtitle">Comprehensive patient review with summaries, alerts, timeline, notes, labs, vitals, and medications.</div>',
    unsafe_allow_html=True,
)

top1, top2 = st.columns([1.4, 1])

with top1:
    st.markdown(f"### Current Patient: {patient_id}")

with top2:
    if st.button("Ask AI About This Patient", use_container_width=True):
        st.switch_page("pages/3_Patient_QA.py")

if patient:
    render_patient_card(patient)
else:
    st.warning("Patient not found.")
    st.stop()

summary = get_patient_summary(patient_id)
alerts = get_patient_alerts(patient_id)
timeline = get_patient_timeline(patient_id)
notes = get_patient_notes(patient_id)
labs = get_patient_labs(patient_id)
vitals = get_patient_vitals(patient_id)
meds = get_patient_medications(patient_id)

m1, m2, m3 = st.columns(3)
with m1:
    render_metric_card("Timeline Events", str(len(timeline)), "Chronological patient events", "purple")
with m2:
    render_metric_card("Lab Records", str(len(labs)), "Available lab entries", "teal")
with m3:
    render_metric_card("Active Alerts", str(len(alerts)), "Review required items", "amber")

st.markdown("### AI Summary")
st.markdown(
    f"""
    <div class="validation-card">
        <div style="color:#c9d0ff; line-height:1.9;">{summary.get('summary', 'No summary available.')}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("### Alerts")
if alerts:
    for alert in alerts:
        level = alert.get("level", "info").lower()
        color = "#22d3ee"
        if level == "warning":
            color = "#f59e0b"
        elif level == "critical":
            color = "#ef4444"

        st.markdown(
            f"""
            <div style="
                background: rgba(255,255,255,0.03);
                border:1px solid rgba(255,255,255,0.06);
                border-left:4px solid {color};
                border-radius:14px;
                padding:14px 16px;
                margin-bottom:10px;
                color:#f5f7ff;
            ">
                <strong>{level.title()}</strong> — {alert.get("message", "")}
            </div>
            """,
            unsafe_allow_html=True,
        )
else:
    st.info("No alerts available.")

render_dark_table("Timeline", pd.DataFrame(timeline))
render_dark_table("Clinical Notes", pd.DataFrame(notes))
render_dark_table("Labs", pd.DataFrame(labs))
render_dark_table("Vitals", pd.DataFrame(vitals))
render_dark_table("Medications", pd.DataFrame(meds))

import streamlit as st


def render_patient_card(patient: dict):
    patient_name = patient.get("name", "Unknown Patient")
    patient_id = patient.get("patient_id", "N/A")
    gender = patient.get("gender", "N/A")
    age = patient.get("age", "N/A")
    status = patient.get("status", "Stable")

    status_color = "#10b981"
    if str(status).lower() in ["critical", "high risk"]:
        status_color = "#ef4444"
    elif str(status).lower() in ["warning", "moderate"]:
        status_color = "#f59e0b"

    st.markdown(
        f"""
        <div class="patient-shell">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
                <div>
                    <div style="font-size:20px; font-weight:800; color:#f5f7ff;">{patient_name}</div>
                    <div style="font-size:13px; color:#9ca3c9; margin-top:4px;">Patient ID: {patient_id}</div>
                </div>
                <div style="background:{status_color}22; color:{status_color}; border:1px solid {status_color}55; padding:6px 14px; border-radius:999px; font-size:12px; font-weight:800;">
                    {status}
                </div>
            </div>
            <div style="display:flex; gap:24px; color:#c9d0ff; font-size:14px;">
                <div><strong style="color:#a78bfa;">Gender:</strong> {gender}</div>
                <div><strong style="color:#a78bfa;">Age:</strong> {age}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )