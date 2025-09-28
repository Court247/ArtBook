from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from db.database import get_db
from models.users import User
from models.post import Post
from models.follow import Follow
from models.like import Like
from utils.firebase_auth import get_current_user
from schemas.post import FeedPostResponse, FeedComment, FeedUser
from models.comment import Comment

router = APIRouter(
    prefix="/home",
    tags=["Home"]
)

@router.get("/feed", response_model=list[FeedPostResponse])
def get_feed(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    posts = db.query(Post).order_by(Post.created_at.desc()).limit(20).all()
    feed = []

    for post in posts:
        likes_count = db.query(func.count(Like.id)).filter(Like.post_id == post.id).scalar()
        comments_count = db.query(func.count(Comment.id)).filter(Comment.post_id == post.id).scalar()

        liked_by_user = (
            db.query(Like)
            .filter(Like.post_id == post.id, Like.user_id == current_user.firebase_uid)
            .first()
            is not None
        )

        comments = (
            db.query(Comment)
            .filter(Comment.post_id == post.id)
            .order_by(Comment.created_at.desc())
            .limit(3)
            .all()
        )

        recent_comments = []
        for c in comments:
            comment_user = db.query(User).filter(User.firebase_uid == c.user_id).first()
            if comment_user:
                recent_comments.append(
                    FeedComment(
                        id=c.id,
                        content=c.content,
                        created_at=c.created_at,
                        user=FeedUser(
                            firebase_uid=comment_user.firebase_uid,
                            display_name=comment_user.display_name,
                            avatar_url=comment_user.avatar_url
                        )
                    )
                )

        author = db.query(User).filter(User.firebase_uid == post.user_id).first()
        if not author:
            raise HTTPException(status_code=404, detail="Author not found")

        feed.append(
            FeedPostResponse(
                id=post.id,
                caption=getattr(post, "caption", None),
                image_url=getattr(post, "image_url", None),
                created_at=post.created_at,
                author=FeedUser(
                    firebase_uid=author.firebase_uid,
                    display_name=author.display_name,
                    avatar_url=author.avatar_url
                ),
                likes_count=likes_count,
                comments_count=comments_count,
                liked_by_current_user=liked_by_user,
                recent_comments=recent_comments
            )
        )

    return feed


@router.get("/trending")
def get_trending(db: Session = Depends(get_db)):
    posts = (
        db.query(Post, func.count(Like.id).label("likes"))
        .join(Like, Like.post_id == Post.id, isouter=True)
        .group_by(Post.id)
        .order_by(func.count(Like.id).desc())
        .limit(20)
        .all()
    )
    return [{"post": post, "likes": likes} for post, likes in posts]


@router.get("/recommended")
def get_recommended(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    followed_ids = db.query(Follow.following_id).filter(Follow.follower_id == current_user.firebase_uid)
    users = (
        db.query(User)
        .filter(User.firebase_uid.notin_(followed_ids))
        .filter(User.firebase_uid != current_user.firebase_uid)
        .order_by(func.random())
        .limit(10)
        .all()
    )
    return users


@router.get("/activity")
def get_activity(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    likes = (
        db.query(Like)
        .join(Post, Like.post_id == Post.id)
        .filter(Post.user_id == current_user.firebase_uid)
        .order_by(Like.created_at.desc())
        .limit(20)
        .all()
    )

    followers = (
        db.query(Follow)
        .filter(Follow.following_id == current_user.firebase_uid)
        .order_by(Follow.created_at.desc())
        .limit(20)
        .all()
    )
    return {"likes": likes, "followers": followers}


@router.get("/stats")
def get_stats(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    post_count = db.query(func.count(Post.id)).filter(Post.user_id == current_user.firebase_uid).scalar()
    follower_count = db.query(func.count(Follow.id)).filter(Follow.following_id == current_user.firebase_uid).scalar()
    following_count = db.query(func.count(Follow.id)).filter(Follow.follower_id == current_user.firebase_uid).scalar()
    like_count = (
        db.query(func.count(Like.id))
        .join(Post, Like.post_id == Post.id)
        .filter(Post.user_id == current_user.firebase_uid)
        .scalar()
    )
    return {
        "posts": post_count,
        "followers": follower_count,
        "following": following_count,
        "likes": like_count,
    }
