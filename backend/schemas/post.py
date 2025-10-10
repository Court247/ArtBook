from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Literal
from .user import UserPublic


# ---------- Minimal user info used in feed or nested data ----------
class FeedUser(BaseModel):
    id: int                      # ✅ auto-increment primary key
    firebase_uid: str
    display_name: str
    avatar_url: Optional[str] = None

    class Config:
        from_attributes = True


# ---------- Minimal comment info shown in feed ----------
class FeedComment(BaseModel):
    id: int
    content: str
    created_at: datetime
    user: FeedUser               # ✅ now includes user's int ID

    class Config:
        from_attributes = True


# ---------- Full post entry used in home feed ----------
class FeedPostResponse(BaseModel):
    id: int
    content: str
    media_url: Optional[str]
    visibility: str
    created_at: datetime
    author: FeedUser             # ✅ nested user with int ID
    likes_count: int
    comments_count: int
    liked_by_current_user: bool
    recent_comments: List[FeedComment] = []

    class Config:
        from_attributes = True

# ---------- Base ----------
class PostBase(BaseModel):
    content: str
    media_url: Optional[str] = None
    visibility: Literal["public", "private", "followers"] = "public"


# ---------- Create / Update ----------
class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    content: Optional[str] = None
    media_url: Optional[str] = None
    visibility: Optional[Literal["public", "private", "followers"]] = None


# ---------- Response ----------
class PostResponse(BaseModel):
    id: int
    user_id: int
    content: str
    media_url: Optional[str]
    visibility: str
    created_at: datetime

    class Config:
        from_attributes = True


# ---------- Feed / Expanded ----------
class FeedComment(BaseModel):
    id: int
    content: str
    created_at: datetime
    user: UserPublic

    class Config:
        from_attributes = True


class FeedPostResponse(BaseModel):
    id: int
    content: str
    media_url: Optional[str]
    visibility: str
    created_at: datetime
    author: UserPublic
    likes_count: int
    comments_count: int
    liked_by_current_user: bool
    recent_comments: List[FeedComment] = []

    class Config:
        from_attributes = True
