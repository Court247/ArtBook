# routers/users.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import SessionLocal
from models.users import User, RoleEnum, StatusEnum
from schemas.user import UserCreate, UserResponse, UserUpdate
from utils.firebase_auth import (
    get_token_payload,
    require_self_or_admin,
    forbid_admin_on_creator_db,
    forbid_admin_on_admin_db,
)

router = APIRouter(prefix="/users", tags=["Users"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    if db.query(User).filter(User.firebase_uid == user.firebase_uid).first():
        raise HTTPException(status_code=400, detail="User already exists with this Firebase UID")

    new_user = User(
        firebase_uid=user.firebase_uid,
        email=user.email,
        display_name=user.display_name,
        bio=user.bio or "",
        avatar_url=user.avatar_url or "",
        role=user.role.value if hasattr(user.role, "value") else user.role,
        status=StatusEnum.active,  # default
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/me", response_model=UserResponse)
def get_current_user(payload: dict = Depends(get_token_payload), db: Session = Depends(get_db)):
    firebase_uid = payload["uid"]
    db_user = db.query(User).filter(User.firebase_uid == firebase_uid).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if not db_user.is_active():
        raise HTTPException(status_code=403, detail=f"Account {db_user.status}")
    return db_user

@router.put("/{firebase_uid}", response_model=UserResponse)
def update_user(firebase_uid: str, payload_body: UserUpdate, payload: dict = Depends(get_token_payload), db: Session = Depends(get_db)):
    require_self_or_admin(payload, firebase_uid)

    target_user = db.query(User).filter(User.firebase_uid == firebase_uid).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")

    if target_user.is_banned():
        raise HTTPException(status_code=403, detail="This user account is banned")

    forbid_admin_on_creator_db(target_user)
    forbid_admin_on_admin_db(target_user, payload)

    # Update profile fields
    if payload_body.display_name is not None:
        target_user.display_name = payload_body.display_name
    if payload_body.bio is not None:
        target_user.bio = payload_body.bio
    if payload_body.avatar_url is not None:
        target_user.avatar_url = payload_body.avatar_url

    # Only creators can change status
    if payload_body.status is not None:
        if not payload.get("creator", False):
            raise HTTPException(status_code=403, detail="Only creators can change status")
        target_user.status = payload_body.status

    db.commit()
    db.refresh(target_user)
    return target_user
