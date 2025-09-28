from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from models.comment import Comment
from models.post import Post
from models.users import User
from schemas.comment import CommentCreate, CommentResponse
from utils.firebase_auth import get_current_user
import uuid

router = APIRouter(prefix="/comments", tags=["Comments"])

# Create a comment
@router.post("/", response_model=CommentResponse)
def create_comment(
    comment: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Ensure the post exists
    post = db.query(Post).filter(Post.id == comment.post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    new_comment = Comment(
        id=str(uuid.uuid4()),
        user_id=current_user.firebase_uid,
        post_id=comment.post_id,
        content=comment.content,
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

# List comments for a post
@router.get("/post/{post_id}", response_model=list[CommentResponse])
def list_comments(post_id: str, db: Session = Depends(get_db)):
    return db.query(Comment).filter(Comment.post_id == post_id).order_by(Comment.created_at.desc()).all()

# Delete a comment
@router.delete("/{comment_id}")
def delete_comment(
    comment_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    # Only allow comment owner or creator/admin to delete
    if comment.user_id != current_user.firebase_uid and current_user.role not in ["creator", "admin"]:
        raise HTTPException(status_code=403, detail="Not authorized to delete this comment")

    db.delete(comment)
    db.commit()
    return {"detail": "Comment deleted"}
