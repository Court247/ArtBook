from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from utils.firebase_auth import get_token_payload
from db.database import SessionLocal
from models.users import User
from schemas.user import UserResponse, UserUpdate, UserCreate

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# single dependency: returns DB user after verifying token (no token->DB role sync)
def get_current_user(
    payload: dict = Depends(get_token_payload),
    db: Session = Depends(get_db)
) -> User:
    user = db.query(User).filter(User.firebase_uid == payload["uid"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Helper: load arbitrary user by id
def get_user_or_404(user_id: int, db: Session):
    target = db.query(User).filter(User.id == user_id).first()
    if not target:
        raise HTTPException(status_code=404, detail="Target user not found")
    return target

# Helper: require creator role
def require_creator(current_user: User = Depends(get_current_user)):
    if not current_user.is_creator:
        raise HTTPException(status_code=403, detail="Creator role required")
    return current_user

@router.get("/me", response_model=UserResponse)
def read_current_user(
    current_user: User = Depends(get_current_user),
):
    # Use DB as source of truth for roles
    response = UserResponse.from_orm(current_user)
    response.is_admin = current_user.is_admin
    response.is_creator = current_user.is_creator
    return response

@router.put("/me", response_model=UserResponse)
def update_user(
    update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Regular users cannot change role fields
    allowed = {"display_name", "bio", "avatar_url"}
    for field, value in update.dict(exclude_unset=True).items():
        if field in allowed:
            setattr(current_user, field, value)
    db.commit()
    db.refresh(current_user)
    return current_user

# Admin/creator endpoint to update any user (admins limited; creators full)
@router.put("/users/{user_id}", response_model=UserResponse)
def update_user_by_admin(
    user_id: int,
    update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    target = get_user_or_404(user_id, db)

    # Creator can edit everyone (including roles)
    if current_user.is_creator:
        allowed = {"display_name", "bio", "avatar_url", "is_admin", "is_creator"}
    else:
        # Non-creators must be admins to use this endpoint
        if not current_user.is_admin:
            raise HTTPException(status_code=403, detail="Admin role required")
        # Admins cannot edit creators or other admins
        if target.is_creator or target.is_admin:
            raise HTTPException(status_code=403, detail="Cannot edit creators or admin users")
        # Admins may edit non-role fields only
        allowed = {"display_name", "bio", "avatar_url"}

    for field, value in update.dict(exclude_unset=True).items():
        if field in allowed:
            setattr(target, field, value)
    db.commit()
    db.refresh(target)
    return target

# Creator-only role management endpoint
@router.put("/users/{user_id}/roles", response_model=UserResponse)
def set_roles_by_creator(
    user_id: int,
    role_update: UserUpdate,
    _: User = Depends(require_creator),
    db: Session = Depends(get_db)
):
    target = get_user_or_404(user_id, db)
    # Only allow role fields here
    for field, value in role_update.dict(exclude_unset=True).items():
        if field in {"is_admin", "is_creator"}:
            setattr(target, field, value)
    db.commit()
    db.refresh(target)
    return target

@router.post("/users", response_model=UserResponse)
def create_user_in_db(
    user_data: UserCreate,
    payload: dict = Depends(get_token_payload),
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(User.firebase_uid == payload["uid"]).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = User(
        firebase_uid=payload["uid"],
        email=user_data.email,
        display_name=user_data.display_name,
        bio=user_data.bio or "",
        avatar_url=user_data.avatar_url or "",
        # Do NOT trust token claims for initial roles; default to False
        is_admin=False,
        created_at=user_data.created_at or datetime.utcnow(),
        is_creator=False
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user