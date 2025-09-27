# utils/firebase_auth.py
import firebase_admin
from firebase_admin import credentials, auth
from fastapi import Header, HTTPException
from typing import Optional
import os
from models.users import User, StatusEnum


# initialize app (keep your credential file path or env var)
if not firebase_admin._apps:
    cred_path = os.getenv("FIREBASE_CREDENTIALS_JSON", "artbook-20329-firebase-adminsdk-fbsvc-ddbc5c06ca.json")
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)


def get_token_payload(authorization: str = Header(...)):
    """
    Verify Authorization header 'Bearer <token>' and return decoded token payload.
    The decoded token should include any custom claims (admin, creator).
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid or missing token format")

    token = authorization.replace("Bearer ", "")
    try:
        decoded = auth.verify_id_token(token)
        # normalized payload for convenience
        return {
            "uid": decoded["uid"],
            "email": decoded.get("email"),
            # boolean flags that creators/admins can set as custom claims in Firebase
            "admin": decoded.get("admin", False),
            "creator": decoded.get("creator", False)
        }
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid Firebase token")


# permission helpers (based on token claims)
def require_creator(payload: dict):
    if not payload.get("creator", False):
        raise HTTPException(status_code=403, detail="Creator privileges required")


def require_admin(payload: dict):
    # creators are also admins logically
    if not (payload.get("admin", False) or payload.get("creator", False)):
        raise HTTPException(status_code=403, detail="Admin privileges required")


def require_self_or_admin(payload: dict, target_uid: str):
    """
    Allow action if user is modifying their own account OR is admin/creator.
    """
    if payload.get("uid") == target_uid:
        return
    if payload.get("creator", False) or payload.get("admin", False):
        return
    raise HTTPException(status_code=403, detail="Not authorized to modify this user")


def forbid_admin_on_creator_db(target_user):
    """
    Given a target DB user (User instance), prevent admins from modifying creators.
    (Relies on role in DB)
    """
    if getattr(target_user, "role", None) == "creator":
        raise HTTPException(status_code=403, detail="Cannot modify creator account")


def forbid_admin_on_admin_db(target_user, acting_payload):
    """
    Prevent admins (non-creator) from modifying other admins.
    acting_payload is the token payload of the actor.
    """
    if getattr(target_user, "role", None) == "admin" and not acting_payload.get("creator", False):
        raise HTTPException(status_code=403, detail="Admins cannot modify other admins")

def enforce_user_status(user: User):
    if user.status == StatusEnum.deleted:
        raise HTTPException(status_code=403, detail="User account is deleted")
    if user.status == StatusEnum.suspended:
        raise HTTPException(status_code=403, detail="User account is suspended")
    if user.status == StatusEnum.banned:
        raise HTTPException(status_code=403, detail="User account is banned")


def set_custom_user_claims(uid: str, claims: dict):
    """
    Wrap firebase_admin.auth.set_custom_user_claims
    """
    try:
        auth.set_custom_user_claims(uid, claims)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to set Firebase claims: {e}")


def get_user_record(uid: str):
    """Return firebase user record (optional helper)."""
    try:
        return auth.get_user(uid)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Firebase user not found: {e}")
