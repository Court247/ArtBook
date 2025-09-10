import firebase_admin
from firebase_admin import credentials, auth, initialize_app
from fastapi import Header, HTTPException

# Initialize once at import
cred = credentials.Certificate("artbook-20329-firebase-adminsdk-fbsvc-ddbc5c06ca.json")
firebase_admin.initialize_app(cred)

def get_token_payload(auth_header: str = Header(...)):
    """
    Extracts and verifies the Firebase token from the Authorization header.
    Returns decoded token payload.
    """
    if not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid or missing token format")
    token = auth_header.replace("Bearer ", "")
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid Firebase token")
    return payload

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
