from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from backend.models.model_users import User, StatusEnum
from backend.schemas.schema_user import UserCreate, UserUpdate, UserResponse
from utils.firebase_auth import (
    get_token_payload,
    get_current_user,
    require_self_or_admin,
    forbid_admin_on_creator_db,
    forbid_admin_on_admin_db,
)

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Create a user record after Firebase signup"""
    if db.query(User).filter(User.firebase_uid == user.firebase_uid).first():
        raise HTTPException(status_code=400, detail="User already exists")
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        firebase_uid=user.firebase_uid,
        email=user.email,
        display_name=user.display_name,
        bio=user.bio,
        avatar_url=user.avatar_url,
        role=user.role,
        status=StatusEnum.active,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """Get the currently authenticated user"""
    return current_user


@router.put("/{firebase_uid}", response_model=UserResponse)
def update_user(
    firebase_uid: str,
    updates: UserUpdate,
    payload: dict = Depends(get_token_payload),
    db: Session = Depends(get_db),
):
    """Allow self-update or admin update"""
    require_self_or_admin(payload, firebase_uid)

    user = db.query(User).filter(User.firebase_uid == firebase_uid).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    forbid_admin_on_creator_db(user)
    forbid_admin_on_admin_db(user, payload)

    for field, value in updates.dict(exclude_unset=True).items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)
    return user
