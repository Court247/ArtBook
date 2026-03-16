from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from backend.models.model_comment import Comment
from backend.models.model_post import Post
from backend.models.model_repost import Repost  # ✅ NEW
from backend.models.model_users import User, RoleEnum
from backend.schemas.schema_comment import CommentCreate, CommentResponse
from utils.firebase_auth import get_current_user
from utils.notifications import create_notification

router = APIRouter(prefix="/comments", tags=["Comments"])


@router.post("/", response_model=CommentResponse)
def create_comment(
    comment: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Add a comment to a post OR a repost (repost derives original post_id)."""

    repost = None
    post_id = comment.post_id
    repost_id = comment.repost_id

    # If repost_id is provided, derive post_id from repost.original_post_id
    if repost_id is not None:
        repost = db.query(Repost).filter(Repost.id == repost_id).first()
        if not repost:
            raise HTTPException(status_code=404, detail="Repost not found")
        post_id = repost.original_post_id

    if post_id is None:
        raise HTTPException(status_code=422, detail="post_id or repost_id is required")

    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    new_comment = Comment(
        user_id=current_user.id,
        post_id=post_id,
        repost_id=repost_id,
        content=comment.content,
    )

    # ✅ Trigger notification
    recipient_id = repost.user_id if repost else post.user_id
    if recipient_id != current_user.id:
        create_notification(
            db,
            sender_id=current_user.id,
            recipient_id=recipient_id,
            notif_type="comment",
            post_id=post.id,
            message=(
                f"{current_user.display_name or 'Someone'} commented on your repost"
                if repost else
                f"{current_user.display_name or 'Someone'} commented on your post"
            ),
        )

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment


@router.get("/post/{post_id}", response_model=list[CommentResponse])
def list_comments(post_id: int, db: Session = Depends(get_db)):
    """List comments for a post"""
    return (
        db.query(Comment)
        .filter(Comment.post_id == post_id)
        .order_by(Comment.created_at.desc())
        .all()
    )


@router.get("/repost/{repost_id}", response_model=list[CommentResponse])  # ✅ NEW
def list_repost_comments(repost_id: int, db: Session = Depends(get_db)):
    """List comments specifically attached to a repost"""
    return (
        db.query(Comment)
        .filter(Comment.repost_id == repost_id)
        .order_by(Comment.created_at.desc())
        .all()
    )


@router.delete("/{comment_id}")
def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete a comment (own or admin/creator)"""
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if comment.user_id != current_user.id and current_user.role not in [RoleEnum.creator, RoleEnum.admin]:
        raise HTTPException(status_code=403, detail="Not authorized")
    db.delete(comment)
    db.commit()
    return {"detail": "Comment deleted"}