"""
Solar Sense — Entry point.
Intelligent MLPE platform for scalable manufacturing and AI-enabled solar infrastructure.
"""
import streamlit as st

# Wide layout, minimal chrome
st.set_page_config(
    page_title="Solar Sense",
    layout="wide",
    initial_sidebar_state="auto",
)

# Optional minimal global CSS for industrial, clean look
st.markdown(
    """
    <style>
    .stApp { max-width: 100%; }
    </style>
    """,
    unsafe_allow_html=True,
)

# Home message; navigation is via Streamlit multi-page (sidebar)
st.markdown("**Solar Sense** — Select a page from the sidebar.")
