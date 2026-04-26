import streamlit as st


def render_metric_card(title: str, value: str, subtitle: str = "", color: str = "purple"):
    color_map = {
        "purple": "🟣",
        "teal": "🔵",
        "green": "🟢",
        "amber": "🟡",
        "red": "🔴",
    }
    icon = color_map.get(color, "🟣")
    st.metric(
        label=f"{icon} {title}",
        value=value,
        help=subtitle if subtitle else None,
    )