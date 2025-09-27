# routers/admin.py
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from db.database import SessionLocal
from models.users import User, RoleEnum
from schemas.user import UserResponse
from utils.firebase_auth import get_token_payload, require_admin, require_creator, forbid_admin_on_creator_db, forbid_admin_on_admin_db, set_custom_user_claims

router = APIRouter(prefix="/admin", tags=["Admin"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/dashboard")
def admin_dashboard(payload: dict = Depends(get_token_payload), db: Session = Depends(get_db)):
    require_admin(payload)
    # make sure DB reflects that token is admin (optional sync)
    uid = payload.get("uid")
    current_user = db.query(User).filter(User.firebase_uid == uid).first()
    if current_user and current_user.role != RoleEnum.admin.value and not current_user.role == RoleEnum.creator:
        # If token claims show admin but DB doesn't, you might want to sync. Optional.
        current_user.role = RoleEnum.admin
        db.commit()
    return {"message": "Welcome to the admin dashboard."}


@router.get("/users", response_model=list[UserResponse])
def list_all_users(payload: dict = Depends(get_token_payload), db: Session = Depends(get_db)):
    require_admin(payload)
    return db.query(User).all()


@router.delete("/users/{firebase_uid}")
def delete_user_by_id(firebase_uid: str, payload: dict = Depends(get_token_payload), db: Session = Depends(get_db)):
    require_admin(payload)
    user = db.query(User).filter(User.firebase_uid == firebase_uid).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Admins cannot delete creators; admins cannot delete other admins (unless actor is creator)
    forbid_admin_on_creator_db(user)
    forbid_admin_on_admin_db(user, payload)

    db.delete(user)
    db.commit()
    return {"detail": f"User {firebase_uid} deleted"}


@router.post("/promote-user/{firebase_uid}")
def promote_or_demote_user(firebase_uid: str, body: dict = Body(...), payload: dict = Depends(get_token_payload), db: Session = Depends(get_db)):
    """
    Creator only endpoint to promote/demote admins.
    Expected body: {"admin": true} to set admin, false to remove.
    """
    require_creator(payload)

    make_admin = body.get("admin", False)

    user = db.query(User).filter(User.firebase_uid == firebase_uid).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # creators cannot accidentally change other creators
    if user.role == RoleEnum.creator.value and not payload.get("creator", False):
        raise HTTPException(status_code=403, detail="Cannot change creator accounts")

    # set DB role and Firebase custom claim
    if make_admin:
        # do not override creators
        if user.role != RoleEnum.creator.value:
            user.role = RoleEnum.admin.value
        set_custom_user_claims(firebase_uid, {"admin": True})
    else:
        # demote to regular (or choose premium depending on your flow)
        # do not demote creators
        if user.role != RoleEnum.creator.value:
            user.role = RoleEnum.regular.value
        set_custom_user_claims(firebase_uid, {"admin": False})

    db.commit()
    db.refresh(user)

    action = "promoted" if make_admin else "demoted"
    return {"detail": f"User {firebase_uid} successfully {action}."}
