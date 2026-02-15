# routers/admin.py
from fastapi import APIRouter, Depends, HTTPException, Body, status
from sqlalchemy.orm import Session
from db.database import get_db
from backend.models.model_users import User, RoleEnum, StatusEnum
from backend.models.model_post_flag import PostFlag
from utils.firebase_auth import (
    get_token_payload,
    require_admin,
    require_creator,
    forbid_admin_on_creator_db,
    forbid_admin_on_admin_db,
    set_custom_user_claims,
)

router = APIRouter(prefix="/admin", tags=["Admin & Moderation"])


# -----------------------------
#  Core Admin Utilities
# -----------------------------

## Pulls up the admin dashboard. For only admin accounts. 
@router.get("/dashboard")
def admin_dashboard(payload: dict = Depends(get_token_payload), db: Session = Depends(get_db)):
    require_admin(payload)
    uid = payload.get("uid")
    current_user = db.query(User).filter(User.firebase_uid == uid).first()
    if current_user and current_user.role not in [RoleEnum.admin, RoleEnum.creator]:
        current_user.role = RoleEnum.admin
        db.commit()
    return {"message": "Welcome to the admin dashboard."}

# Allows the Admin to find a specific user. 
@router.get("/users", response_model=list)
def list_all_users(payload: dict = Depends(get_token_payload), db: Session = Depends(get_db)):
    require_admin(payload)
    users = db.query(User).order_by(User.created_at.desc()).all()
    return [{"id": u.id, "email": u.email, "display_name": u.display_name, "role": u.role, "status": u.status} for u in users]

# Allows admin to delete user account
@router.delete("/users/{firebase_uid}")
def delete_user(firebase_uid: str, payload: dict = Depends(get_token_payload), db: Session = Depends(get_db)):
    require_admin(payload)
    user = db.query(User).filter(User.firebase_uid == firebase_uid).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    forbid_admin_on_creator_db(user)
    forbid_admin_on_admin_db(user, payload)

    db.delete(user)
    db.commit()
    return {"detail": f"User {firebase_uid} deleted"}

# Allows creator to promote or demote users to/from admin status
@router.post("/promote-user/{firebase_uid}")
def promote_or_demote_user(
    firebase_uid: str,
    body: dict = Body(...),
    payload: dict = Depends(get_token_payload),
    db: Session = Depends(get_db),
):
    """
    Creator-only endpoint to promote/demote admins.
    Expected body: {"admin": true} to promote, false to demote.
    """
    require_creator(payload)
    make_admin = bool(body.get("admin", False))

    user = db.query(User).filter(User.firebase_uid == firebase_uid).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.role == RoleEnum.creator and not payload.get("creator", False):
        raise HTTPException(status_code=403, detail="Cannot modify creator accounts")

    if make_admin:
        if user.role != RoleEnum.creator:
            user.role = RoleEnum.admin
        set_custom_user_claims(firebase_uid, {"admin": True})
    else:
        if user.role != RoleEnum.creator:
            user.role = RoleEnum.regular
        set_custom_user_claims(firebase_uid, {"admin": False})

    db.commit()
    db.refresh(user)
    return {"detail": f"User {firebase_uid} {'promoted' if make_admin else 'demoted'} successfully."}


# -----------------------------
#  Moderation: Post Flags
# -----------------------------

# Allows admin to look at reported flags. 
@router.get("/flags/pending")
def get_pending_flags(payload: dict = Depends(get_token_payload), db: Session = Depends(get_db)):
    """List all unreviewed post reports"""
    require_admin(payload)
    flags = (
        db.query(PostFlag)
        .filter(PostFlag.reviewed == False)
        .order_by(PostFlag.created_at.desc())
        .all()
    )
    return [
        {
            "id": f.id,
            "post_id": f.post_id,
            "reported_by": f.reported_by,
            "reason": f.reason,
            "created_at": f.created_at,
        }
        for f in flags
    ]

# Admins mark flags as reviewed
@router.post("/flags/{flag_id}/review")
def mark_flag_reviewed(
    flag_id: int,
    payload: dict = Depends(get_token_payload),
    db: Session = Depends(get_db),
):
    """Mark a reported post as reviewed"""
    require_admin(payload)
    flag = db.query(PostFlag).filter(PostFlag.id == flag_id).first()
    if not flag:
        raise HTTPException(status_code=404, detail="Flag not found")

    flag.reviewed = True
    db.commit()
    return {"detail": f"Flag {flag_id} marked as reviewed."}

#Allows admin to delete flags
@router.delete("/flags/{flag_id}")
def delete_flag(
    flag_id: int,
    payload: dict = Depends(get_token_payload),
    db: Session = Depends(get_db),
):
    """Delete a flag entirely (creator privilege)"""
    require_creator(payload)
    flag = db.query(PostFlag).filter(PostFlag.id == flag_id).first()
    if not flag:
        raise HTTPException(status_code=404, detail="Flag not found")
    db.delete(flag)
    db.commit()
    return {"detail": f"Flag {flag_id} deleted."}


# -----------------------------
#  Moderation: User Control
# -----------------------------

#Admin can suspend users
@router.patch("/users/{user_id}/suspend")
def suspend_user(
    user_id: int,
    body: dict = Body(...),
    payload: dict = Depends(get_token_payload),
    db: Session = Depends(get_db),
):
    """Suspend or ban a user account"""
    require_admin(payload)
    action = body.get("action", "suspend")  # suspend | ban

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    forbid_admin_on_creator_db(user)
    forbid_admin_on_admin_db(user, payload)

    if action == "ban":
        user.status = StatusEnum.banned
    else:
        user.status = StatusEnum.suspended

    db.commit()
    db.refresh(user)
    return {"detail": f"User {user.display_name or user.email} {action}ed."}

#Admin can restore users from banned or suspended status.
@router.patch("/users/{user_id}/restore")
def restore_user(
    user_id: int,
    payload: dict = Depends(get_token_payload),
    db: Session = Depends(get_db),
):
    """Reactivate a suspended or banned user"""
    require_admin(payload)
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.status = StatusEnum.active
    db.commit()
    return {"detail": f"User {user.display_name or user.email} restored to active status."}
