# routers/follow.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from db.database import get_db
from models.model_follow import Follow
from models.model_users import User
from schemas.schema_follow import FollowCreate, FollowResponse, FollowerFollowingResponse
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

    #Trigger notification
    create_notification(
        db,
        sender_id=current_user.id,
        recipient_id=follow.following_id,
        notif_type="follow",
        message=f"{current_user.display_name or 'Someone'} started following you",
    )

    return db_follow

# -------------------------------------------------
# Unfollow a user
# -------------------------------------------------

@router.delete("/{following_id}", status_code=204)
def unfollow_user(
    following_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    follow = (
        db.query(Follow)
        .filter(Follow.follower_id == current_user.id, Follow.following_id == follow.following_id)
        .first()
    )
    if not follow:
        raise HTTPException(status_code=404, detail="Follow relationship not found")

    db.delete(follow)
    db.commit()

# -------------------------------------------------
# Get followers of a user
# -------------------------------------------------
@router.get("/followers/{user_id}", response_model=List[FollowerFollowingResponse])
def get_followers(user_id: int, db: Session = Depends(get_db)):
    followers = (
        db.query(User.id, User.firebase_uid, User.display_name, User.avatar_url)
        .join(Follow, Follow.follower_id == User.id)
        .filter(Follow.following_id == user_id)
        .all()
    )
    return followers

# -------------------------------------------------
# Get following of a user
# -------------------------------------------------
@router.get("/following/{user_id}", response_model=List[FollowerFollowingResponse])
def get_following(user_id: int, db: Session = Depends(get_db)):
    following = (
        db.query(User.id, User.firebase_uid, User.display_name, User.avatar_url)
        .join(Follow, Follow.following_id == User.id)
        .filter(Follow.follower_id == user_id)
        .all()
    )
    return following



