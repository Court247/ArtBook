import firebase_admin
from firebase_admin import credentials, auth

cred = credentials.Certificate("firebase-service-account.json")
firebase_admin.initialize_app(cred)

def verify_token(id_token: str):
    try:
        decoded = auth.verify_id_token(id_token)
        return decoded
    except Exception:
        return None
