import streamlit as st
import pandas as pd
import plotly.express as px
import calendar

def render_chart_page():
    # --- Page CSS ---
    st.markdown("""
        <style>
            .block-container {padding: 1.5rem 1rem 0 1rem;}
            section[data-testid="stSidebar"] div.stButton > button {
                font-size: 12px !important; padding: 0.1rem 0.25rem !important;
                min-height: 40px !important; border-radius: 6px !important; line-height:1.2;
            }
            section[data-testid="stSidebar"] div.stButton p { font-size: 12px !important; margin:0 !important; }
            [data-testid="stMetric"] { padding: 0.25rem 0.5rem; min-height: 60px; margin:0 !important;}
            [data-testid="stMetricLabel"] { font-size: 14px !important; font-weight: 600 !important; color: #333333; }
            [data-testid="stMetricValue"] { font-size: 16px !important; font-weight: 700 !important; color: #0055aa; }
            div.block-container > div {margin-bottom: 0rem !important;}
        </style>
    """, unsafe_allow_html=True)

    # --- Page Title ---
    st.markdown("<h2 style='text-align:left; font-size:28px;'>📊 Daily Stock Visualization (6)</h2>", unsafe_allow_html=True)
    
    if "daily_stock_data" not in st.session_state:
        st.warning("⚠️ No data found. Please upload files in the Data Loader page first.")
        return

    df_raw = st.session_state["daily_stock_data"].copy()
    df_raw.sortvalue(["Operation Date"])
    chart_df = df_filtered.groupby(["Month","Rcv So Flag"], as_index=False)["Quantity[Unit1]"].sum()
    fig_bar = px.line(
        chart_df,
        x="Operation Date",
        y="Quantity[Unit1]",
        title="Daily stock",
        height=400   # chart height
    )
    fig_bar.update_layout(
        xaxis_title="",
        yaxis_title="Quantity",
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5),
        margin=dict(l=0, r=0, t=50, b=0),  # remove extra top/bottom margin
        legend_title_text=""  # 👈 remove legend title
    )
    st.plotly_chart(fig_bar, use_container_width=True)
    
