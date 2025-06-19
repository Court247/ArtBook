from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session
from utils.firebase_auth import verify_token
from db.database import SessionLocal
from models.users import User
from schemas.user import UserResponse, UserUpdate
from utils.firebase_auth import verify_token

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(auth_header: str = Header(...), db: Session = Depends(get_db)) -> User:
    token = auth_header.replace("Bearer ", "")
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid Firebase token")
    
    user = db.query(User).filter(User.firebase_uid == payload["uid"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def read_current_user(
    current_user: User = Depends(get_current_user),
    auth_header: str = Header(...),
):
    token = auth_header.replace("Bearer ", "")
    payload = verify_token(token)
    is_admin = payload.get("admin", False)

    response = UserResponse.from_orm(current_user)
    response.is_admin = is_admin
    return response

@router.get("/me", response_model=UserResponse)
def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/me", response_model=UserResponse)
def update_user(update: UserUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    for field, value in update.dict(exclude_unset=True).items():
        setattr(current_user, field, value)
    db.commit()
    db.refresh(current_user)
    return current_user
