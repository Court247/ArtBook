from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import SessionLocal
from models.post import Post
from schemas.post import PostCreate, PostResponse
from routers.users import get_current_user, get_db
from models.users import User

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.post("/create", response_model=PostResponse)
def create_post(data: PostCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    post = Post(user_id=current_user.firebase_uid, caption=data.caption, image_url=data.image_url)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

@router.get("/feed", response_model=list[PostResponse])
def get_feed(db: Session = Depends(get_db)):
    return db.query(Post).order_by(Post.created_at.desc()).limit(20).all()

@router.get("/user/{user_id}", response_model=list[PostResponse])
def get_user_posts(user_id: int, db: Session = Depends(get_db)):
    return db.query(Post).filter(Post.user_id == user_id).order_by(Post.created_at.desc()).all()

@router.delete("/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post or post.user_id != current_user.firebase_uid:
        raise HTTPException(status_code=403, detail="Unauthorized or not found")
    db.delete(post)
    db.commit()
    return {"detail": "Post deleted"}

@router.post("/{post_id}/flag")
def flag_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    post.is_flagged = True
    db.commit()
    return {"detail": "Post has been flagged for review"}