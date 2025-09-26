from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import SessionLocal
from models.users import User
from schemas.user import UserCreate, UserResponse
from utils.firebase_auth import get_token_payload

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# DB session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check for existing email
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Check for existing firebase_uid
    existing_uid = db.query(User).filter(User.firebase_uid == user.firebase_uid).first()
    if existing_uid:
        raise HTTPException(status_code=400, detail="User already exists with this Firebase UID")

    db_user = User(
        firebase_uid=user.firebase_uid,
        email=user.email,
        display_name=user.display_name,
        bio=user.bio or "",
        avatar_url=user.avatar_url or "",
        is_admin=False,
        is_creator=False,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user



@router.get("/me", response_model=UserResponse)
def get_current_user(
    payload: dict = Depends(get_token_payload),
    db: Session = Depends(get_db)
):
    """
    Return the current logged-in user's profile.
    """
    firebase_uid = payload["uid"]
    db_user = db.query(User).filter(User.firebase_uid == firebase_uid).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
