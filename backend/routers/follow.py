# routers/follow.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from db.database import get_db
from models.follow import Follow
from models.users import User
from schemas.follow import FollowCreate, FollowResponse, FollowerFollowingResponse
from utils.firebase_auth import get_current_user

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
    # prevent self-follow
    if follow.following_id == current_user.id:
        raise HTTPException(status_code=400, detail="You cannot follow yourself")

    # target user must exist
    target = db.query(User.id).filter(User.id == follow.following_id).first()
    if not target:
        raise HTTPException(status_code=404, detail="User to follow not found")

    # unique (follower_id, following_id)
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
    return db_follow


# -------------------------------------------------
# Unfollow a user
# -------------------------------------------------
@router.delete("/{following_id}")
def unfollow_user(
    following_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    rel = (
        db.query(Follow)
        .filter(Follow.follower_id == current_user.id, Follow.following_id == following_id)
        .first()
    )
    if not rel:
        raise HTTPException(status_code=404, detail="Follow relationship not found")

    db.delete(rel)
    db.commit()
    return {"detail": "Unfollowed successfully"}


# -------------------------------------------------
# Users THIS user follows  (→ list of User summaries)
# -------------------------------------------------
@router.get("/following/{user_id}", response_model=List[FollowerFollowingResponse])
def get_following(user_id: int, db: Session = Depends(get_db)):
    # optional: 404 if base user doesn't exist
    if not db.query(User.id).filter(User.id == user_id).first():
        raise HTTPException(status_code=404, detail="User not found")

    users_following = (
        db.query(User)
        .join(Follow, Follow.following_id == User.id)
        .filter(Follow.follower_id == user_id)
        .order_by(Follow.created_at.desc())
        .all()
    )

    return [
        FollowerFollowingResponse(
            id=u.id,
            firebase_uid=u.firebase_uid,
            display_name=u.display_name or "",
            avatar_url=u.avatar_url or "",
        )
        for u in users_following
    ]


# -------------------------------------------------
# Followers OF this user  (→ list of User summaries)
# -------------------------------------------------
@router.get("/followers/{user_id}", response_model=List[FollowerFollowingResponse])
def get_followers(user_id: int, db: Session = Depends(get_db)):
    if not db.query(User.id).filter(User.id == user_id).first():
        raise HTTPException(status_code=404, detail="User not found")

    user_followers = (
        db.query(User)
        .join(Follow, Follow.follower_id == User.id)
        .filter(Follow.following_id == user_id)
        .order_by(Follow.created_at.desc())
        .all()
    )

    return [
        FollowerFollowingResponse(
            id=u.id,
            firebase_uid=u.firebase_uid,
            display_name=u.display_name or "",
            avatar_url=u.avatar_url or "",
        )
        for u in user_followers
    ]
