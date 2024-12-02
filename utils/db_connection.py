from google.cloud import firestore
import json
import streamlit as st

def get_connection(collection_path="fuel_expenses"):
    config_dict = json.loads(st.secrets["textkey"])
    db = firestore.Client.from_service_account_info(config_dict)
    return db.collection(collection_path)

def get_data(collection: firestore.CollectionReference):
    data = collection.get()
    return [i.to_dict() for i in data]