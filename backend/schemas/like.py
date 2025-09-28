from pydantic import BaseModel
from datetime import datetime

# ✅ Schema for creating a like
class LikeCreate(BaseModel):
    post_id: int

# ✅ Schema for returning a like
class LikeResponse(BaseModel):
    id: int
    user_id: int
    post_id: int
    created_at: datetime

# ✅ Schema for returning like counts
class LikeCountResponse(BaseModel):
    post_id: int
    like_count: int
    
class Config:
    from_attributes = True