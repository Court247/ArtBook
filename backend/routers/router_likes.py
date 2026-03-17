from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.database import get_db
from models.model_like import Like
from models.model_post import Post
from models.model_repost import Repost
from models.model_users import User

from utils.firebase_auth import get_current_user
from utils.notifications import create_notification

router = APIRouter(
    prefix="/likes",
    tags=["Likes"]
)


# Like and unliking posts
@router.post("/post/{post_id}")
def toggle_like(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Toggle like/unlike on a post"""

    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # 🔍 Check if already liked (POST ONLY)
    existing = db.query(Like).filter(
        Like.post_id == post_id,
        Like.user_id == current_user.id
    ).first()

    # 🔄 Unlike
    if existing:
        db.delete(existing)
        db.commit()
        return {"liked": False}

    # ✅ Like post
    new_like = Like(
        user_id=current_user.id,
        post_id=post_id,
        repost_id=None  # 👈 explicitly NOT a repost like
    )

    db.add(new_like)
    db.commit()
    db.refresh(new_like)

    # 🔔 Notify post owner
    if post.user_id != current_user.id:
        create_notification(
            db,
            sender_id=current_user.id,
            recipient_id=post.user_id,
            notif_type="like_post",
            post_id=post.id,
            message=f"{current_user.display_name or 'Someone'} liked your post",
        )

    return {"liked": True}


# Like and unliking reposts (independent from post likes)
@router.post("/repost/{repost_id}")
def toggle_repost_like(
    repost_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Toggle like/unlike on a repost (independent from post likes)"""

    repost = db.query(Repost).filter(Repost.id == repost_id).first()
    if not repost:
        raise HTTPException(status_code=404, detail="Repost not found")

    # 🔍 Check if already liked (REPOST ONLY)
    existing = db.query(Like).filter(
        Like.repost_id == repost_id,
        Like.user_id == current_user.id
    ).first()

    # 🔄 Unlike
    if existing:
        db.delete(existing)
        db.commit()
        return {"liked": False}

    # ✅ Like repost (NO post_id involved)
    new_like = Like(
        user_id=current_user.id,
        repost_id=repost_id,
        post_id=None  # 👈 explicitly NOT a post like
    )

    db.add(new_like)
    db.commit()
    db.refresh(new_like)

    # 🔔 Notify repost owner ONLY
    if repost.user_id != current_user.id:
        create_notification(
            db,
            sender_id=current_user.id,
            recipient_id=repost.user_id,
            notif_type="like_repost",
            repost_id=repost.id,
            message=f"{current_user.display_name or 'Someone'} liked your repost",
        )

    return {"liked": True}