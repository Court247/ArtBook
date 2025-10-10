# utils/firebase_auth.py
import os
import firebase_admin
from firebase_admin import credentials, auth
from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from db.database import get_db
from models.users import User, StatusEnum, RoleEnum


# -------------------------------------------------------------------
# Firebase Admin Initialization (one-time, supports env + emulator)
# -------------------------------------------------------------------
def _init_firebase_if_needed() -> None:
    if firebase_admin._apps:
        return

    # Emulator support (no credentials required)
    emulator_host = os.getenv("FIREBASE_AUTH_EMULATOR_HOST")
    if emulator_host:
        firebase_admin.initialize_app(options={"projectId": os.getenv("FIREBASE_PROJECT_ID", "demo-project")})
        return

    # Service account path (prefer explicit env)
    cred_path = (
        os.getenv("FIREBASE_CREDENTIALS_JSON")
        or os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    )
    if not cred_path or not os.path.exists(cred_path):
        raise RuntimeError(
            "Firebase credentials not found. "
            "Set FIREBASE_CREDENTIALS_JSON or GOOGLE_APPLICATION_CREDENTIALS to a valid service account JSON."
        )

    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)


_init_firebase_if_needed()


# -------------------------------------------------------------------
# Token / Auth helpers
# -------------------------------------------------------------------
def _extract_bearer_token(authorization: Optional[str]) -> str:
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Authorization header"
        )
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Authorization format; expected 'Bearer <token>'"
        )
    return authorization.split(" ", 1)[1].strip()


def get_token_payload(authorization: Optional[str] = Header(default=None)):
    """
    Verify 'Authorization: Bearer <Firebase_ID_Token>' and return a normalized payload.
    Custom claims like 'admin' and 'creator' are included if set.
    """
    token = _extract_bearer_token(authorization)
    try:
        decoded = auth.verify_id_token(token)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired Firebase token")

    # Normalize the shape your routers expect
    return {
        "uid": decoded.get("uid"),
        "email": decoded.get("email"),
        "admin": bool(decoded.get("admin", False)),
        "creator": bool(decoded.get("creator", False)),
    }


def get_current_user(
    payload: dict = Depends(get_token_payload),
    db: Session = Depends(get_db),
) -> User:
    """
    Resolve the logged-in User model by firebase_uid (unique), then enforce status.
    """
    uid = payload.get("uid")
    if not uid:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload (missing uid)")

    user = db.query(User).filter(User.firebase_uid == uid).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found in database")

    _enforce_user_status(user)
    return user


# -------------------------------------------------------------------
# Role/Status enforcement and admin/creator gating
# -------------------------------------------------------------------
def _enforce_user_status(user: User) -> None:
    if user.status == StatusEnum.deleted:
        raise HTTPException(status_code=403, detail="User account is deleted")
    if user.status == StatusEnum.suspended:
        raise HTTPException(status_code=403, detail="User account is suspended")
    if user.status == StatusEnum.banned:
        raise HTTPException(status_code=403, detail="User account is banned")


def require_creator(payload: dict) -> None:
    if not bool(payload.get("creator", False)):
        raise HTTPException(status_code=403, detail="Creator privileges required")


def require_admin(payload: dict) -> None:
    # Creators imply admin
    if not (bool(payload.get("admin", False)) or bool(payload.get("creator", False))):
        raise HTTPException(status_code=403, detail="Admin privileges required")


def require_self_or_admin(payload: dict, target_uid: str) -> None:
    """
    Allow if operating on own account, or if admin/creator.
    """
    if payload.get("uid") == target_uid:
        return
    if payload.get("creator", False) or payload.get("admin", False):
        return
    raise HTTPException(status_code=403, detail="Not authorized to modify this user")


def forbid_admin_on_creator_db(target_user: User) -> None:
    """
    Prevent a non-creator admin from modifying a creator account.
    """
    # Depending on how SQLAlchemy Enum is configured, role may be RoleEnum or str.
    role_value = target_user.role.value if isinstance(target_user.role, RoleEnum) else target_user.role
    if role_value == RoleEnum.creator.value:
        raise HTTPException(status_code=403, detail="Cannot modify creator account")


def forbid_admin_on_admin_db(target_user: User, acting_payload: dict) -> None:
    """
    Prevent an admin (non-creator) from modifying another admin.
    """
    role_value = target_user.role.value if isinstance(target_user.role, RoleEnum) else target_user.role
    if role_value == RoleEnum.admin.value and not acting_payload.get("creator", False):
        raise HTTPException(status_code=403, detail="Admins cannot modify other admins")


# -------------------------------------------------------------------
# Optional Firebase helpers used elsewhere
# -------------------------------------------------------------------
def set_custom_user_claims(uid: str, claims: dict) -> None:
    try:
        auth.set_custom_user_claims(uid, claims)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to set Firebase claims: {e}")


def get_user_record(uid: str):
    try:
        return auth.get_user(uid)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Firebase user not found: {e}")
