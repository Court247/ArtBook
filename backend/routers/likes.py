from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from models.like import Like
from models.users import User
from utils.firebase_auth import get_current_user

router = APIRouter(prefix="/likes", tags=["Likes"])


@router.post("/{post_id}")
def toggle_like(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Toggle like/unlike on a post"""
    like = db.query(Like).filter(
        Like.post_id == post_id, Like.user_id == current_user.id
    ).first()

    if like:
        db.delete(like)
        db.commit()
        return {"liked": False}

    new_like = Like(user_id=current_user.id, post_id=post_id)
    db.add(new_like)
    db.commit()
    return {"liked": True}


@router.get("/{post_id}/count")
def get_like_count(post_id: int, db: Session = Depends(get_db)):
    """Get like count"""
    count = db.query(Like).filter(Like.post_id == post_id).count()
    return {"post_id": post_id, "likes": count}
