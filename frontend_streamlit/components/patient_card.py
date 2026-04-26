
import streamlit as st


def render_patient_card(patient: dict):
    patient_name = patient.get("name", "Unknown Patient")
    patient_id = patient.get("patient_id", "N/A")
    gender = patient.get("gender", "N/A")
    age = patient.get("age", "N/A")
    status = patient.get("status", "Stable")

    if str(status).lower() in ["critical", "high risk"]:
        status_display = "🔴 Critical"
    elif str(status).lower() in ["warning", "moderate"]:
        status_display = "🟡 Warning"
    else:
        status_display = "🟢 Stable"

    with st.container():
        col1, col2 = st.columns([5, 1])
        with col1:
            st.subheader(patient_name)
            st.caption(f"Patient ID: {patient_id}")
        with col2:
            st.markdown(f"**{status_display}**")

        col3, col4, col5 = st.columns(3)
        with col3:
            st.metric("Gender", gender)
        with col4:
            st.metric("Age", age)
        with col5:
            st.metric("Status", status)

        st.divider()
