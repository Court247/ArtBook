# routers/follow.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from db.database import get_db
from models.follow import Follow
from models.users import User
from schemas.follow import FollowCreate, FollowResponse, FollowerFollowingResponse
from utils.firebase_auth import get_current_user
from utils.notifications import create_notification

router = APIRouter(prefix="/follow", tags=["Follow"])

# -------------------------------------------------
# Follow a user
# -------------------------------------------------
@router.post("/", response_model=FollowResponse)
def follow_user(
    follow: FollowCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if follow.following_id == current_user.id:
        raise HTTPException(status_code=400, detail="You cannot follow yourself")

    target = db.query(User).filter(User.id == follow.following_id).first()
    if not target:
        raise HTTPException(status_code=404, detail="User to follow not found")

    existing = (
        db.query(Follow)
        .filter(Follow.follower_id == current_user.id, Follow.following_id == follow.following_id)
        .first()
    )
    if existing:
        raise HTTPException(status_code=400, detail="Already following this user")

    db_follow = Follow(follower_id=current_user.id, following_id=follow.following_id)
    db.add(db_follow)
    db.commit()
    db.refresh(db_follow)

    # ✅ Trigger notification
    create_notification(
        db,
        sender_id=current_user.id,
        recipient_id=follow.following_id,
        notif_type="follow",
        message=f"{current_user.display_name or 'Someone'} started following you",
    )

    return db_follow
