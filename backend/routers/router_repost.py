from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from backend.models.model_repost import Repost
from backend.models.model_post import Post
from backend.models.model_users import User
from backend.models.model_notifications import Notification
from backend.schemas.schema_repost import RepostCreate, RepostResponse
from utils.firebase_auth import get_current_user
from utils.notifications import create_notification

router = APIRouter(prefix="/reposts", tags=["Reposts"])

@router.post("/", response_model=RepostResponse)
def create_repost(
    data: RepostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    original = db.query(Post).filter(Post.id == data.original_post_id).first()
    if not original:
        raise HTTPException(status_code=404, detail="Original post not found")

    is_quote = bool(data.quote and data.quote.strip())

    if not is_quote:
        existing = db.query(Repost).filter(
            Repost.user_id == current_user.id,
            Repost.original_post_id == data.original_post_id,
            Repost.is_quote == False
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail="Already reposted this post")

    repost = Repost(
        user_id=current_user.id,
        original_post_id=data.original_post_id,
        quote=data.quote,
        is_quote=is_quote
    )
    db.add(repost)
    db.commit()
    db.refresh(repost)

    # ✅ Trigger notification
    create_notification(
        db,
        sender_id=current_user.id,
        recipient_id=original.user_id,
        notif_type="share",
        post_id=original.id,
        message=(
            f"{current_user.display_name or 'Someone'} quoted your post"
            if is_quote else
            f"{current_user.display_name or 'Someone'} reposted your post"
        ),
    )

    return repost

@router.get("/user/{user_id}", response_model=list[RepostResponse])
def get_user_reposts(user_id: int, db: Session = Depends(get_db)):
    """Show all simple reposts for a given user (no quotes)."""
    return (
        db.query(Repost)
        .filter(Repost.user_id == user_id, Repost.is_quote == False)
        .order_by(Repost.created_at.desc())
        .all()
    )


@router.get("/quotes/{user_id}", response_model=list[RepostResponse])
def get_user_quote_reposts(user_id: int, db: Session = Depends(get_db)):
    """Show all quote reposts for a given user."""
    return (
        db.query(Repost)
        .filter(Repost.user_id == user_id, Repost.is_quote == True)
        .order_by(Repost.created_at.desc())
        .all()
    )
