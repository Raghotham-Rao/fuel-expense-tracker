import streamlit as st
import pandas as pd
from utils.db_connection import get_connection, get_data
from datetime import datetime, timedelta
from hashlib import md5

st.header("Add Refuel Details")
    
conn = get_connection()


with st.container():
    columns = st.columns([5, 2, 2])
    if st.session_state.get('login_status'):
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
                        "date": str(date),
                        "vehicle": vehicle,
                        "quantity": fuel_quantity,
                        "odometer_reading": odometer,
                        "amount": amount,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "is_refuel_indicator_on": is_refuel_indicator_on
                    }

                    conn.add(new_entry)
                    st.success(f"Details added successfully for {vehicle}!")
    else:
        with columns[0].form("refuel_form"):
            mpin = st.text_input("Enter Login PIN")
            mpin_submitted = st.form_submit_button("Login")
            if mpin_submitted:
                encrypted_mpin = md5(mpin.encode()).hexdigest()
                login_conn = get_connection('login')
                mpins = get_data(login_conn)
                if any([i["mpin"] == encrypted_mpin for i in mpins]):
                    st.session_state['login_status'] = True
                    st.login_expiry = datetime.now() + timedelta(minutes=5)
                    st.toast("Welcome!")
                    st.rerun()
                else:
                    st.error("Wrong PIN")