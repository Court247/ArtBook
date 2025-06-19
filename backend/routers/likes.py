from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import SessionLocal
from models.like import Like
from routers.users import get_current_user, get_db
from models.users import User

router = APIRouter()

@router.post("/posts/{post_id}/like")
def toggle_like(post_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    like = db.query(Like).filter(Like.post_id == post_id, Like.user_id == current_user.id).first()
    if like:
        db.delete(like)
        db.commit()
        return {"liked": False}
    else:
        new_like = Like(post_id=post_id, user_id=current_user.id)
        db.add(new_like)
        db.commit()
        return {"liked": True}

@router.get("/posts/{post_id}/likes")
def like_count(post_id: int, db: Session = Depends(get_db)):
    return {"likes": db.query(Like).filter(Like.post_id == post_id).count()}
