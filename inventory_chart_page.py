import streamlit as st
import pandas as pd
import plotly.express as px
import calendar

def day_suffix(d):
    if 11 <= d <= 13:
        return f"{d}th"
    last_digit = d % 10
    if last_digit == 1:
        return f"{d}st"
    elif last_digit == 2:
        return f"{d}nd"
    elif last_digit == 3:
        return f"{d}rd"
    else:
        return f"{d}th"

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

    df_raw["Year"] = df_raw["Operation Date"].dt.year
    df_raw["Month"] = df_raw["Operation Date"].dt.month
    
    # --- Sidebar filters ---
    years_list = sorted(df_raw["Year"].dropna().unique())
    selected_year = st.sidebar.selectbox("Select Year", ["ALL"] + list(years_list), index=0)

    months = list(range(1,13))
    selected_month = st.sidebar.radio("Select Month (optional)", ["All"] + [calendar.month_abbr[m] for m in months], index=0)
    selected_month_num = list(calendar.month_abbr).index(selected_month) if selected_month != "All" else None

    items = st.multiselect("Item Code", df_raw["Item Code"].unique())

    # --- Apply filters ---
    df_filtered = df_raw.copy()
    if selected_year != "ALL":
        df_filtered = df_filtered[df_filtered["Year"] == selected_year]      
    if selected_month_num:  # only filter if a real month is selected
        df_filtered = df_filtered[df_filtered["Month"] == selected_month_num]        
    if items:
        df_filtered = df_filtered[df_filtered["Item Code"].isin(items)]
    if df_filtered.empty:
        st.warning("⚠️ No data after filtering.")
        return

    # ==========================================================
    # 📊 CHART
    # ==========================================================
    if selected_month_num:
        # --- Daily chart for selected year+month ---
        chart_df = df_filtered.groupby(["Operation Date","Rcv So Flag"], as_index=False)["Quantity[Unit1]"].sum()
    
        chart_df["x_value"] = chart_df["Operation Date"]  # always provide real date
        chart_df["x_label"] = chart_df["Operation Date"].dt.day.apply(day_suffix)
    
        chart_title = f"📊 Daily Stock in {selected_year}-{calendar.month_abbr[selected_month_num]}"
    
    elif selected_year != "ALL":
        # --- Daily chart for the whole year ---
        chart_df = df_filtered.groupby(["Operation Date","Rcv So Flag"], as_index=False)["Quantity[Unit1]"].sum()
    
        chart_df["x_value"] = chart_df["Operation Date"]
        chart_df["x_label"] = chart_df["Operation Date"].dt.strftime("%b")
    
        chart_title = f"📊 Daily Stock in {selected_year}"
    
    else:
        # --- Full history across all years ---
        chart_df = df_filtered.groupby(["Operation Date", "Rcv So Flag"], as_index=False)["Quantity[Unit1]"].sum()
        chart_df["x_value"] = chart_df["Operation Date"]
        chart_df["x_label"] = chart_df["Operation Date"].astype(str)
    
        chart_title = "📊 Stock by Year"

    fig_line = px.line(
        chart_df,
        x="x_value",   # always exists
        y="Quantity[Unit1]",
        color="Rcv So Flag",
        title=chart_title
    )

    # Show monthly ticks only
    fig_line.update_xaxes(
        dtick="M1",                # one tick per month
        tickformat="%b",           # show short month name
        ticklabelmode="period"     # align label at start of month
    )
    
    st.plotly_chart(fig_line, use_container_width=True)
