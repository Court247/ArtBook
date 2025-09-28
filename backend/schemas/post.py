from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


# Schema for creating a new post
class PostCreate(BaseModel):
    content: str
    media_url: Optional[str] = None

# Schema for updating a post
class PostUpdate(BaseModel):
    content: Optional[str] = None
    media_url: Optional[str] = None

# Schema for returning posts to the frontend
class PostResponse(BaseModel):
    id: int
    user_id: int
    content: str
    media_url: Optional[str]
    created_at: datetime
    
# Nested user info for feed responses
class FeedUser(BaseModel):
    firebase_uid: str
    display_name: str
    avatar_url: Optional[str] = None

    class Config:
        from_attributes = True

# Recent comment preview
class FeedComment(BaseModel):
    id: int
    content: str
    created_at: datetime
    user: FeedUser

    class Config:
        from_attributes = True

# Full feed post response
class FeedPostResponse(BaseModel):
    id: int
    caption: Optional[str]
    image_url: Optional[str]
    created_at: datetime
    author: FeedUser
    likes_count: int
    comments_count: int
    liked_by_current_user: bool
    recent_comments: List[FeedComment] = []

    class Config:
        from_attributes = True
