import streamlit as st
import pandas as pd
from utils.db_connection import get_data, get_connection
from utils.components import *
import plotly.express as px
from datetime import datetime, timedelta
import numpy as np

st.set_page_config(page_title="Fuel Expense Tracker", layout="wide", initial_sidebar_state="expanded")

# Initialize session state for data storage
if "fuel_data" not in st.session_state:
    st.session_state.fuel_data = pd.DataFrame(columns=["Date", "Vehicle", "Fuel Quantity (L)", "Odometer (km)", "Amount ($)", "Mileage (km/L)"])

conn = get_connection()
data = get_data(conn)

df = pd.DataFrame(data).sort_values("date")

df["refuel_qty_till_date"] = df["quantity"].cumsum()
mileage_df = df[df["is_refuel_indicator_on"]].copy()
mileage_df['mileage'] = mileage_df['odometer_reading'].diff(1) / mileage_df['refuel_qty_till_date'].diff(1)
mileage_df['days_to_refill'] = pd.to_datetime(mileage_df['timestamp']).diff(1).dt.days

header_cols = st.columns([6, 2])
header_cols[0].title(":fuelpump: Fuel Expense Tracker")
header_cols[1].selectbox('Vehicle', df['vehicle'].unique().tolist())

st.markdown('---')

with st.container():
    columns = st.columns([5, 2])

    with columns[0]:
        monthly_stats_fig = get_monthly_stats_fig(df)
        st.plotly_chart(monthly_stats_fig)

    with columns[1]:
        display_metrics_box(df['amount'].sum().astype(int), "Total Expenditure till date", unit='&#8377;', prefix_unit=True)
        display_metrics_box(df.shape[0], "No. of times Refueled")
        display_metrics_box(df[pd.to_datetime(df['date']).dt.month == datetime.now().month]['amount'].sum(), "Current Month", unit='&#8377;', prefix_unit=True)
        display_metrics_box(mileage_df['mileage'].mean().round(2), "Average Mileage", unit='<span style="font-size: 14px">kmpl</span>')
        display_metrics_box(mileage_df['days_to_refill'].mean().round(2), "Average Days for refuel", unit='<span style="font-size: 14px">days</span>')
        display_metrics_box(df["odometer_reading"].max().astype(int), "Last Refueled at", unit='<span style="font-size: 14px"> km</span>', heading_level=1)