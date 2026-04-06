import streamlit as st

def inject_styles():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@600;800&family=Open+Sans:wght@400;600&family=Roboto+Condensed:wght@600&display=swap');

    h1, h2 {
        font-family: 'Montserrat', sans-serif !important;
    }

    h3, h4, h5, h6 {
        font-family: 'Roboto Condensed', sans-serif !important;
    }

    p, [data-testid="stMarkdownContainer"] > p {
        font-family: 'Open Sans', sans-serif !important;
    }

    [data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
        font-family: 'Roboto Condensed', sans-serif !important;
        font-size: 1.05rem !important;
        font-weight: 600 !important;
        color: #f0f2f6 !important;
        margin-bottom: 2px !important;
    }

    [data-testid="stSidebar"] [data-testid="stRadio"] label[data-baseweb="radio"] div {
        color: #caced5 !important;
    }

    [data-testid="stMetric"] {
        background-color: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 15px 20px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.25);
        transition: all 0.3s ease;
    }

    [data-testid="stMetric"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.4);
        background-color: rgba(255, 255, 255, 0.05);
    }

    [data-testid="stMetricLabel"] p {
        font-family: 'Roboto Condensed', sans-serif !important;
        font-size: 0.95rem !important;
        font-weight: 500 !important;
        color: #a0aab8 !important;
    }

    [data-testid="stMetricValue"] > div {
        font-family: 'Montserrat', sans-serif !important;
        font-size: 1.6rem !important;
        font-weight: 700 !important;
        white-space: normal !important;
        line-height: 1.2 !important;
        padding-top: 5px !important;
    }

    [data-testid="stMetricDelta"] {
        margin-top: 5px !important;
    }

    [data-testid="stMetricDelta"] > div {
        background-color: rgba(128, 128, 128, 0.1) !important;
        background-color: color-mix(in srgb, currentColor 15%, transparent) !important;
        border: 1px solid rgba(128, 128, 128, 0.2) !important;
        border-color: color-mix(in srgb, currentColor 30%, transparent) !important;
        padding: 4px 14px !important;
        border-radius: 20px !important;
        font-weight: 700 !important;
        font-size: 0.85rem !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        letter-spacing: 0.5px !important;
    }

    [data-testid="stMetricDelta"] svg {
        display: none !important;
    }

    [data-testid="stDataFrame"] {
        font-family: 'Open Sans', sans-serif !important;
    }
    </style>
    """, unsafe_allow_html=True)
