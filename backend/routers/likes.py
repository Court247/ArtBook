from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from models.like import Like
from models.users import User
from utils.firebase_auth import get_current_user

router = APIRouter(
    prefix="/likes",
    tags=["Likes"]
)

# ✅ Toggle like on a post
@router.post("/posts/{post_id}")
def toggle_like(
    post_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    like = db.query(Like).filter(
        Like.post_id == post_id,
        Like.user_id == current_user.firebase_uid
    ).first()

    if like:
        db.delete(like)
        db.commit()
        return {"liked": False}
    else:
        new_like = Like(
            user_id=current_user.firebase_uid,
            post_id=post_id
        )
        db.add(new_like)
        db.commit()
        db.refresh(new_like)
        return {"liked": True}

# ✅ Get like count for a post
@router.get("/posts/{post_id}/count")
def like_count(post_id: str, db: Session = Depends(get_db)):
    return {
        "post_id": post_id,
        "likes": db.query(Like).filter(Like.post_id == post_id).count()
    }
