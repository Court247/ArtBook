from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional, List, Literal
from .schema_user import UserPublic
import re


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

    @field_validator("content")
    @classmethod
    def validate_content(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Content cannot be empty")
        if len(v) > 2000:
            raise ValueError("Content must be 2000 characters or fewer")
        return v

    @field_validator("media_url")
    @classmethod
    def validate_media_url(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        v = v.strip()
        if not v:
            return None
        if not re.match(r'^https?://', v, re.IGNORECASE):
            raise ValueError("media_url must be a valid HTTP or HTTPS URL")
        return v


# ---------- Create / Update ----------
class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    content: Optional[str] = None
    media_url: Optional[str] = None
    visibility: Optional[Literal["public", "private", "followers"]] = None

    @field_validator("content")
    @classmethod
    def validate_content(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        v = v.strip()
        if not v:
            raise ValueError("Content cannot be empty")
        if len(v) > 2000:
            raise ValueError("Content must be 2000 characters or fewer")
        return v

    @field_validator("media_url")
    @classmethod
    def validate_media_url(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        v = v.strip()
        if not v:
            return None
        if not re.match(r'^https?://', v, re.IGNORECASE):
            raise ValueError("media_url must be a valid HTTP or HTTPS URL")
        return v


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




