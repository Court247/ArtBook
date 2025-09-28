from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.database import get_db
from models.follow import Follow
from models.users import User
from schemas.follow import FollowCreate, FollowResponse
from typing import List
from utils.firebase_auth import get_current_user

router = APIRouter(
    prefix="/follow",
    tags=["Follow"]
)

# ✅ Follow a user
@router.post("/", response_model=FollowResponse)
def follow_user(
    follow: FollowCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if follow.follower_id != current_user.firebase_uid:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only follow as yourself"
        )

    if follow.follower_id == follow.following_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot follow yourself"
        )

    existing = db.query(Follow).filter_by(
        follower_id=follow.follower_id,
        following_id=follow.following_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already following this user"
        )

    db_follow = Follow(**follow.dict())
    db.add(db_follow)
    db.commit()
    db.refresh(db_follow)
    return db_follow

# ✅ Unfollow a user
@router.delete("/{following_uid}", status_code=status.HTTP_204_NO_CONTENT)
def unfollow_user(
    following_uid: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    follow = db.query(Follow).filter_by(
        follower_id=current_user.firebase_uid,
        following_id=following_uid
    ).first()

    if not follow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Follow relationship not found"
        )

    db.delete(follow)
    db.commit()
    return {"detail": "Unfollowed successfully"}

# ✅ Get a user's following list
@router.get("/following/{firebase_uid}", response_model=List[FollowResponse])
def get_following(firebase_uid: str, db: Session = Depends(get_db)):
    return db.query(Follow).filter_by(follower_id=firebase_uid).all()

# ✅ Get a user's followers list
@router.get("/followers/{firebase_uid}", response_model=List[FollowResponse])
def get_followers(firebase_uid: str, db: Session = Depends(get_db)):
    return db.query(Follow).filter_by(following_id=firebase_uid).all()
