import streamlit as st
import pandas as pd


def render_dark_table(title: str, df: pd.DataFrame):
    st.markdown(
        f"""
        <div class="section-block">
            <div style="font-size:22px; font-weight:800; color:#f5f7ff; margin-bottom:10px;">
                {title}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if df is None or df.empty:
        st.info(f"No data available for {title}.")
        return

    st.dataframe(df, use_container_width=True, hide_index=True)


def render_key_value_block(title: str, data: dict):
    st.markdown(
        f"""
        <div class="table-shell" style="margin-top:16px;">
            <div style="font-size:20px; font-weight:800; color:#f5f7ff; margin-bottom:14px;">{title}</div>
        """,
        unsafe_allow_html=True,
    )

    for key, value in data.items():
        st.markdown(
            f"""
            <div style="
                display:flex;
                justify-content:space-between;
                padding:10px 0;
                border-bottom:1px solid rgba(255,255,255,0.06);
            ">
                <div style="color:#9ca3c9; font-weight:600;">{key}</div>
                <div style="color:#f5f7ff;">{value}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)