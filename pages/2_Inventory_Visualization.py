import streamlit as st
from load_inventory_sample_data import init_session_state
from inventory_chart_page import render_chart_page

st.set_page_config(page_title="Inventory Visualization", layout="wide")

# --- Initialize session state with cached data ---
init_session_state()

# --- Render the chart page ---
render_chart_page()
