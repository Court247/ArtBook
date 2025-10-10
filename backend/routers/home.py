# routers/home.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from db.database import get_db
from models.users import User
from models.post import Post
from models.follow import Follow
from models.like import Like
from models.comment import Comment
from utils.firebase_auth import get_current_user
from schemas.post import FeedPostResponse, FeedComment, FeedUser

router = APIRouter(prefix="/home", tags=["Home / Feed"])


# -------------------------------------------------
# Main Feed
# -------------------------------------------------
@router.get("/feed", response_model=list[FeedPostResponse])
def get_feed(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Show a feed of recent public and followed-user posts.
    """
    # Get IDs of people the current user follows
    followed_ids = (
        db.query(Follow.following_id)
        .filter(Follow.follower_id == current_user.id)
        .subquery()
    )

    # Query posts (either public or by followed users)
    posts = (
        db.query(Post)
        .filter(
            (Post.visibility == "public")
            | (Post.user_id.in_(followed_ids))
        )
        .order_by(Post.created_at.desc())
        .limit(25)
        .all()
    )

    feed = []
    for post in posts:
        # Count likes and comments
        likes_count = db.query(func.count(Like.id)).filter(Like.post_id == post.id).scalar()
        comments_count = db.query(func.count(Comment.id)).filter(Comment.post_id == post.id).scalar()

        # Has current user liked this?
        liked_by_user = (
            db.query(Like)
            .filter(Like.post_id == post.id, Like.user_id == current_user.id)
            .first()
            is not None
        )

        # Most recent 3 comments
        recent_comments_raw = (
            db.query(Comment)
            .filter(Comment.post_id == post.id)
            .order_by(Comment.created_at.desc())
            .limit(3)
            .all()
        )

        recent_comments = []
        for c in recent_comments_raw:
            comment_user = db.query(User).filter(User.id == c.user_id).first()
            if comment_user:
                recent_comments.append(
                    FeedComment(
                        id=c.id,
                        content=c.content,
                        created_at=c.created_at,
                        user=FeedUser(
                            firebase_uid=comment_user.firebase_uid,
                            display_name=comment_user.display_name,
                            avatar_url=comment_user.avatar_url,
                        ),
                    )
                )

        # Post author
        author = db.query(User).filter(User.id == post.user_id).first()
        if not author:
            continue

        feed.append(
            FeedPostResponse(
                id=post.id,
                content=post.content,
                media_url=post.media_url,
                visibility=post.visibility,
                created_at=post.created_at,
                author=FeedUser(
                    firebase_uid=author.firebase_uid,
                    display_name=author.display_name,
                    avatar_url=author.avatar_url,
                ),
                likes_count=likes_count,
                comments_count=comments_count,
                liked_by_current_user=liked_by_user,
                recent_comments=recent_comments,
            )
        )

    return feed


# -------------------------------------------------
# Trending Posts
# -------------------------------------------------
@router.get("/trending")
def get_trending(db: Session = Depends(get_db)):
    """
    Show trending posts ranked by total likes.
    """
    trending = (
        db.query(Post, func.count(Like.id).label("likes"))
        .join(Like, Like.post_id == Post.id, isouter=True)
        .group_by(Post.id)
        .order_by(func.count(Like.id).desc())
        .limit(20)
        .all()
    )

    return [
        {
            "post_id": post.id,
            "user_id": post.user_id,
            "content": post.content,
            "media_url": post.media_url,
            "visibility": post.visibility,
            "likes": likes,
            "created_at": post.created_at,
        }
        for post, likes in trending
    ]


# -------------------------------------------------
# Recommended Users
# -------------------------------------------------
@router.get("/recommended")
def get_recommended(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Recommend random users not yet followed by current user.
    """
    followed_subq = db.query(Follow.following_id).filter(Follow.follower_id == current_user.id)
    recommendations = (
        db.query(User)
        .filter(User.id.notin_(followed_subq))
        .filter(User.id != current_user.id)
        .order_by(func.rand())
        .limit(10)
        .all()
    )

    return [
        {
            "id": u.id,
            "firebase_uid": u.firebase_uid,
            "display_name": u.display_name,
            "avatar_url": u.avatar_url,
        }
        for u in recommendations
    ]


# -------------------------------------------------
# Activity (likes + followers)
# -------------------------------------------------
@router.get("/activity")
def get_activity(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get recent activity for the current user (likes & followers).
    """
    recent_likes = (
        db.query(Like)
        .join(Post, Like.post_id == Post.id)
        .filter(Post.user_id == current_user.id)
        .order_by(Like.created_at.desc())
        .limit(15)
        .all()
    )

    recent_followers = (
        db.query(Follow)
        .filter(Follow.following_id == current_user.id)
        .order_by(Follow.created_at.desc())
        .limit(15)
        .all()
    )

    return {
        "likes": [
            {"user_id": l.user_id, "post_id": l.post_id, "created_at": l.created_at}
            for l in recent_likes
        ],
        "followers": [
            {"follower_id": f.follower_id, "created_at": f.created_at}
            for f in recent_followers
        ],
    }


# -------------------------------------------------
# Personal Stats
# -------------------------------------------------
@router.get("/stats")
def get_user_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get current user's counts of posts, followers, following, and likes.
    """
    post_count = db.query(func.count(Post.id)).filter(Post.user_id == current_user.id).scalar()
    follower_count = db.query(func.count(Follow.id)).filter(Follow.following_id == current_user.id).scalar()
    following_count = db.query(func.count(Follow.id)).filter(Follow.follower_id == current_user.id).scalar()
    like_count = (
        db.query(func.count(Like.id))
        .join(Post, Like.post_id == Post.id)
        .filter(Post.user_id == current_user.id)
        .scalar()
    )

    return {
        "posts": post_count,
        "followers": follower_count,
        "following": following_count,
        "likes": like_count,
    }
