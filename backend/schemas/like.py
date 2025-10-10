from pydantic import BaseModel
from datetime import datetime


# ---------- Create ----------
class LikeCreate(BaseModel):
    post_id: int


# ---------- Response ----------
class LikeResponse(BaseModel):
    id: int
    user_id: int
    post_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class LikeCountResponse(BaseModel):
    post_id: int
    like_count: int

    class Config:
        from_attributes = True
