import base64
from pathlib import Path
import streamlit as st

ROOT_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = ROOT_DIR / "static"


def _font_b64(filename: str) -> str:
    return base64.b64encode((STATIC_DIR / filename).read_bytes()).decode()


def inject_custom_css():
    monocraft_b64 = _font_b64("Monocraft.ttf")

    st.markdown(
        f"""
        <style>
        @font-face {{
            font-family: 'Monocraft';
            src: url('data:font/ttf;base64,{monocraft_b64}') format('truetype');
            font-display: swap;
        }}
        body, html, .stApp, .main, .block-container, .element-container {{
            font-family: 'Segoe UI', Roboto, Arial, sans-serif !important;
            line-height: 1.4 !important;
        }}
        .stApp *:not([class*="material-symbol"]):not([data-testid*="Icon"]):not([data-testid*="icon"]):not([data-baseweb="icon"]):not(svg):not(svg *) {{
            font-family: 'Monocraft', 'Courier New', monospace !important;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )