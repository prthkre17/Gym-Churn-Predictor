import streamlit as st
from styles import inject_styles
from data_loader import load_and_predict
from sidebar import render_sidebar
from views import get_display_df, render_view_header, render_member_table
from analytics import render_bulk_analytics
from member_detail import render_member_detail

st.set_page_config(page_title="GymSense: AI CRM", page_icon="🏋️‍♂️", layout="wide")

inject_styles()

try:
    df_results = load_and_predict()
except Exception as e:
    st.error(f"Error loading files: {e}")
    st.stop()

view_option, filtered_df = render_sidebar(df_results)

display_df = get_display_df(view_option, filtered_df)

render_view_header(view_option, display_df)

render_member_table(display_df)

st.markdown("---")
st.header("📈Overview and Analytics (Bulk Members)")
render_bulk_analytics(display_df, df_results, view_option)

st.markdown("---")
st.header("📈Overview and Analytics (Individual Member)")
render_member_detail(display_df, df_results, view_option)
