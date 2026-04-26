import streamlit as st
from pathlib import Path


def load_css():
    css_path = Path(__file__).resolve().parent.parent / "styles" / "custom.css"
    if css_path.exists():
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def render_page_header(title: str, subtitle: str, badge: str = ""):
    badge_html = f'<div class="custom-badge">{badge}</div>' if badge else ""
    st.markdown(
        f"""
        <div class="hero-section">
            {badge_html}
            <div class="gradient-title">{title}</div>
            <div class="subtitle">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )