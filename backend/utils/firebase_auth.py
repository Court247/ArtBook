import firebase_admin
from firebase_admin import credentials, auth
from fastapi import HTTPException

# Initialize once at import
cred = credentials.Certificate("artbook-20329-firebase-adminsdk-fbsvc-ddbc5c06ca.json")
firebase_admin.initialize_app(cred)

def verify_token(id_token: str):
    try:
        decoded = auth.verify_id_token(id_token)
        return {
            "uid": decoded["uid"],
            "email": decoded.get("email"),
            "admin": decoded.get("admin", False)
        }
    except Exception:
        return None

def require_admin(payload: dict):
    if not payload.get("admin", False):
        raise HTTPException(status_code=403, detail="Admin access required")
