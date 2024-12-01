import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime, timedelta

def get_connection():
    if not firebase_admin._apps:
        cred = credentials.Certificate(r".firebase\fuel-expense-tracker-9ba72-firebase-adminsdk-nq3yw-e9ebc3ef53.json")
        firebase_admin.initialize_app(
            cred,
            {
                'databaseURL': 'https://fuel-expense-tracker-9ba72-default-rtdb.firebaseio.com/'
            }
        )
    return db.reference()

def get_data(conn: db.Reference):
    return conn.get()