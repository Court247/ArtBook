from fastapi import APIRouter, Depends, Header, HTTPException, Body
from utils.firebase_auth import verify_token, require_admin
from sqlalchemy.orm import Session
from db.database import SessionLocal
from models.users import User
from schemas.user import UserResponse
from fastapi import Depends
from models.post import Post
import utils.firebase_auth as firebase_auth
from sqlalchemy.orm import Session
from routers.users import get_token_payload

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter()

def get_token_payload(auth_header: str = Header(...)):
    token = auth_header.replace("Bearer ", "")
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload

@router.get("/dashboard")
def admin_dashboard(payload: dict = Depends(get_token_payload), db: Session = Depends(get_db)):
    require_admin(payload)
    # Set is_admin in the database if the token has admin claim
    uid = payload.get("uid")
    if payload.get("admin", False):
        current_user = db.query(User).filter(User.firebase_uid == uid).first()
        if current_user and not current_user.is_admin:
            current_user.is_admin = True
            db.commit()
    return {"message": "Welcome to the admin dashboard."}

@router.get("/users", response_model=list[UserResponse])
def list_all_users(
    payload: dict = Depends(get_token_payload),
    db: Session = Depends(get_db)
):
    require_admin(payload)
    return db.query(User).all()

@router.delete("/users/{user_id}")
def delete_user_by_id(
    user_id: int,
    payload: dict = Depends(get_token_payload),
    db: Session = Depends(get_db)
):
    require_admin(payload)
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"detail": f"User {user_id} deleted"}

@router.get("/posts", response_model=list[dict])
def get_all_posts(
    payload: dict = Depends(get_token_payload),
    db: Session = Depends(get_db)
):
    require_admin(payload)
    posts = db.query(Post).order_by(Post.created_at.desc()).all()
    return [
        {
            "id": post.id,
            "user_id": post.user_id,
            "caption": post.caption,
            "image_url": post.image_url,
            "created_at": post.created_at,
            "is_flagged": post.is_flagged  # ✅ correct attribute
        }
        for post in posts
    ]

@router.delete("/posts/{post_id}")
def delete_post_by_id(
    post_id: int,
    payload: dict = Depends(get_token_payload),
    db: Session = Depends(get_db)
):
    require_admin(payload)
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(post)
    db.commit()
    return {"detail": f"Post {post_id} deleted"}

@router.get("/flagged-posts")
def get_flagged_posts(payload: dict = Depends(get_token_payload), db: Session = Depends(get_db)):
    require_admin(payload)
    flagged = db.query(Post).filter(Post.is_flagged == True).all()
    return [{"id": p.id, "caption": p.caption, "user_id": p.user_id} for p in flagged]

@router.post("/promote-user/{firebase_uid}")
def promote_or_demote_user(
    firebase_uid: str,
    payload: dict = Depends(get_token_payload),
    db: Session = Depends(get_db),
    body: dict = Body(...)
):
    require_admin(payload)
    make_admin = body.get("admin", False)

    # Set Firebase custom claim
    firebase_auth.set_custom_user_claims(firebase_uid, {"admin": make_admin})

    # Sync local database (if user exists)
    user = db.query(User).filter(User.firebase_uid == firebase_uid).first()
    if user:
        user.is_admin = make_admin
        db.commit()

    action = "promoted" if make_admin else "demoted"
    return {"detail": f"User {firebase_uid} successfully {action}."}