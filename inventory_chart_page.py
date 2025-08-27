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
    if selected_month_num:
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
        df_filtered["Day"] = pd.to_datetime(df_filtered["Operation Date"]).dt.day
        total_days = pd.Series(range(1,32))
        chart_df = df_filtered.groupby(["Day","Rcv So Flag"], as_index=False)["Quantity[Unit1]"].sum()
        all_days_flags = pd.MultiIndex.from_product([total_days, chart_df["Rcv So Flag"].unique()], names=["Day","Rcv So Flag"])
        chart_df = chart_df.set_index(["Day","Rcv So Flag"]).reindex(all_days_flags, fill_value=0).reset_index()
        chart_df["x_label"] = chart_df["Day"].apply(day_suffix)
        chart_title = f"📊 Daily Stock in {selected_year}-{calendar.month_abbr[selected_month_num]}"
    elif selected_year != "ALL":
        chart_df = df_filtered.groupby(["Operation Date","Rcv So Flag"], as_index=False)["Quantity[Unit1]"].sum()
        all_months_flags = pd.MultiIndex.from_product([months, chart_df["Rcv So Flag"].unique()], names=["Month","Rcv So Flag"])
        chart_df = chart_df.set_index(["Operation Date","Rcv So Flag"]).reindex(all_months_flags, fill_value=0).reset_index()
        chart_df["x_label"] = chart_df["Month"].apply(lambda m: calendar.month_abbr[m])
        chart_title = f"📊 Monthly Stock in {selected_year}"   
    else:
        chart_df = df_filtered.groupby(["Operation Date", "Rcv So Flag"], as_index=False)["Quantity[Unit1]"].sum()
        chart_df["x_label"] = chart_df["Operation Date"].astype(str)
        chart_title = "📊 Stock by Year"

    fig_line = px.line(
        chart_df,
        x="x_label",
        y="Quantity[Unit1]",
        title=chart_title,
        height=400   # chart height
    )
    fig_line.update_layout(
        xaxis_title="",
        yaxis_title="Quantity",
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5),
        margin=dict(l=0, r=0, t=50, b=0),  # remove extra top/bottom margin
        legend_title_text=""  # 👈 remove legend title
    )
    
    
    st.plotly_chart(fig_line, use_container_width=True)
