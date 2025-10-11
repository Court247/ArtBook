from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from models.comment_like import CommentLike
from models.comment import Comment
from models.users import User
from schemas.comment_likes import CommentLikeCreate, CommentLikeResponse
from utils.firebase_auth import get_current_user
from utils.notifications import create_notification

router = APIRouter(prefix="/comment-likes", tags=["Comment Likes"])

@router.post("/", response_model=CommentLikeResponse)
def toggle_comment_like(
    data: CommentLikeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Like or unlike a comment"""
    comment = db.query(Comment).filter(Comment.id == data.comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    existing = (
        db.query(CommentLike)
        .filter(
            CommentLike.comment_id == data.comment_id,
            CommentLike.user_id == current_user.id,
        )
        .first()
    )

    if existing:
        db.delete(existing)
        db.commit()
        return {"detail": "Comment unliked"}

    new_like = CommentLike(user_id=current_user.id, comment_id=data.comment_id)
    db.add(new_like)
    db.commit()
    db.refresh(new_like)

    create_notification(
        db,
        sender_id=current_user.id,
        recipient_id=comment.user_id,
        notif_type="like",
        comment_id=comment.id,
        message=f"{current_user.display_name or 'Someone'} liked your comment",
    )

    return new_like

@router.get("/count/{comment_id}")
def get_comment_like_count(comment_id: int, db: Session = Depends(get_db)):
    """Count likes for a specific comment"""
    count = db.query(CommentLike).filter(CommentLike.comment_id == comment_id).count()
    return {"comment_id": comment_id, "likes": count}
