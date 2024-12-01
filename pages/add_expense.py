import streamlit as st
import pandas as pd
from utils.db_connection import get_connection
from datetime import datetime, timedelta

st.header("Add Refuel Details")
    
conn = get_connection()

with st.container():
    columns = st.columns([5, 2, 2])

    with columns[0]:
        with st.form("refuel_form"):
            date = st.date_input("Date")
            vehicle = st.selectbox("Vehicle Name/ID", ["Grand i10", "Jupiter", "Entorq"], 0)
            fuel_quantity = st.number_input("Fuel Quantity (L)", min_value=0.0, format="%.2f", value=20.00)
            odometer = st.number_input("Current Odometer Reading (km)", min_value=0.0, format="%.0f")
            amount = st.number_input("Amount Paid (&#8377;)", min_value=0.0, format="%.2f")
            is_refuel_indicator_on = st.checkbox("Refuel Indicator On ?", value=True)

            submitted = st.form_submit_button("Add Refuel Details")

            if submitted:
                new_entry = {
                    "Date": str(date),
                    "Vehicle": vehicle,
                    "Fuel Quantity": fuel_quantity,
                    "Odometer": odometer,
                    "Amount": amount
                }

                conn.push(new_entry)
                st.success(f"Details added successfully for {vehicle}!")