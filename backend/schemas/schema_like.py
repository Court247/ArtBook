from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# ---------- Create ----------
class LikeCreate(BaseModel):
    post_id: Optional[int] = None
    repost_id: Optional[int] = None

# ---------- Response ----------
class LikeResponse(BaseModel):
    id: int
    user_id: int
    post_id: int
    repost_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True


class LikeCountResponse(BaseModel):
    post_id: int
    like_count: int

    class Config:
        from_attributes = True