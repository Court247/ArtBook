from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# ---------- Base ----------
class CommentBase(BaseModel):
    content: str


# ---------- Create / Update ----------
# Let's the client sent either post_id or repost_id and the router will derive the right post_id when repost_id is given. 
# This way the client doesn't need to know about the internal workings of the repost system and can just send the comment to the right place.

class CommentCreate(CommentBase):
    post_id: Optional[int] = None
    repost_id: Optional[int] = None


class CommentUpdate(BaseModel):
    content: Optional[str] = None


# ---------- Response ----------
class CommentResponse(BaseModel):
    id: int
    user_id: int
    post_id: int
    repost_id: Optional[int] = None
    content: str
    created_at: datetime

    class Config:
        from_attributes = True