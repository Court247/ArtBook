import firebase_admin
from firebase_admin import credentials, auth
from fastapi import Header, HTTPException

# Initialize Firebase only once
if not firebase_admin._apps:
    cred = credentials.Certificate("artbook-20329-firebase-adminsdk-fbsvc-ddbc5c06ca.json")
    firebase_admin.initialize_app(cred)


def get_token_payload(authorization: str = Header(...)):
    """
    Extracts and verifies the Firebase token from the Authorization header.
    Returns decoded token payload.
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid or missing token format")

    token = authorization.replace("Bearer ", "")
    try:
        decoded = auth.verify_id_token(token)
        return {
            "uid": decoded["uid"],
            "email": decoded.get("email"),
            "admin": decoded.get("admin", False),
            "creator": decoded.get("creator", False),
        }
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid Firebase token")


def require_admin(payload: dict):
    """
    Raises 403 if user does not have admin claim.
    """
    if not payload.get("admin", False):
        raise HTTPException(status_code=403, detail="Admin access required")


def require_creator(payload: dict):
    """
    Raises 403 if user does not have creator claim.
    """
    if not payload.get("creator", False):
        raise HTTPException(status_code=403, detail="Creator access required")


def set_custom_user_claims(uid: str, claims: dict):
    """
    Assigns custom claims to a Firebase user.
    Example: set_custom_user_claims(uid, {"admin": True})
    """
    try:
        auth.set_custom_user_claims(uid, claims)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to set claims: {str(e)}")

def get_user(uid: str):
    """
    Fetch Firebase user and return the user record (with claims).
    """
    return auth.get_user(uid)
