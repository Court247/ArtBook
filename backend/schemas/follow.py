from pydantic import BaseModel
from datetime import datetime

# ✅ Schema for creating a follow
class FollowCreate(BaseModel):
    following_id: int  # the user being followed

# ✅ Schema for returning follow relationships
class FollowResponse(BaseModel):
    id: int
    follower_id: int
    following_id: int
    created_at: datetime

# ✅ Schema for returning follower/following lists
class FollowerFollowingResponse(BaseModel):
    id: int
    firebase_uid: str
    display_name: str
    avatar_url: str

    class Config:
        from_attributes = True