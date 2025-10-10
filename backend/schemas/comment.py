from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# ---------- Base ----------
class CommentBase(BaseModel):
    content: str


# ---------- Create / Update ----------
class CommentCreate(CommentBase):
    post_id: int


class CommentUpdate(BaseModel):
    content: Optional[str] = None


# ---------- Response ----------
class CommentResponse(BaseModel):
    id: int
    user_id: int
    post_id: int
    content: str
    created_at: datetime

    class Config:
        from_attributes = True
