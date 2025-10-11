# routers/likes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from models.like import Like
from models.post import Post
from models.users import User
from utils.firebase_auth import get_current_user
from utils.notifications import create_notification

router = APIRouter(prefix="/likes", tags=["Likes"])

@router.post("/{post_id}")
def toggle_like(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Toggle like/unlike on a post"""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    existing = db.query(Like).filter(
        Like.post_id == post_id, Like.user_id == current_user.id
    ).first()

    if existing:
        db.delete(existing)
        db.commit()
        return {"liked": False}

    new_like = Like(user_id=current_user.id, post_id=post_id)
    db.add(new_like)
    db.commit()
    db.refresh(new_like)

    # ✅ Trigger notification
    create_notification(
        db,
        sender_id=current_user.id,
        recipient_id=post.user_id,
        notif_type="like",
        post_id=post.id,
        message=f"{current_user.display_name or 'Someone'} liked your post",
    )

    return {"liked": True}
