from pydantic import BaseModel
from datetime import datetime


# ---------- Create ----------
class FollowCreate(BaseModel):
    following_id: int


# ---------- Response ----------
class FollowResponse(BaseModel):
    id: int
    follower_id: int
    following_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ---------- Follower / Following Lists ----------
class FollowerFollowingResponse(BaseModel):
    id: int
    firebase_uid: str
    display_name: str
    avatar_url: str

    class Config:
        from_attributes = True
