import streamlit as st


def initialize_state():
    defaults = {
        "selected_patient_id": None,
        "show_tips": True,
        "compact_mode": False,
        "dark_mode": True,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value