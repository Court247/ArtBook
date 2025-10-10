from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from models.post import Post
from models.post_flag import PostFlag
from models.users import User
from schemas.post import PostCreate, PostResponse
from utils.firebase_auth import get_current_user

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.post("/", response_model=PostResponse)
def create_post(
    post_data: PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new post"""
    post = Post(
        user_id=current_user.id,
        content=post_data.content,
        media_url=post_data.media_url,
        visibility=post_data.visibility,
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


@router.get("/", response_model=list[PostResponse])
def get_recent_posts(db: Session = Depends(get_db)):
    """Get latest public posts"""
    return db.query(Post).order_by(Post.created_at.desc()).limit(20).all()


@router.get("/user/{user_id}", response_model=list[PostResponse])
def get_user_posts(user_id: int, db: Session = Depends(get_db)):
    """List posts by a user"""
    return db.query(Post).filter(Post.user_id == user_id).order_by(Post.created_at.desc()).all()


@router.delete("/{post_id}")
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete your own post"""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this post")
    db.delete(post)
    db.commit()
    return {"detail": "Post deleted"}


@router.post("/{post_id}/flag")
def flag_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Flag a post for moderation"""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    existing_flag = db.query(PostFlag).filter(
        PostFlag.post_id == post_id, PostFlag.reported_by == current_user.id
    ).first()
    if existing_flag:
        raise HTTPException(status_code=400, detail="You already reported this post")

    flag = PostFlag(post_id=post_id, reported_by=current_user.id)
    db.add(flag)
    db.commit()
    db.refresh(flag)
    return {"detail": "Post flagged successfully"}
