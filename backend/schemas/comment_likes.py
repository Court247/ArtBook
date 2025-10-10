from pydantic import BaseModel
from datetime import datetime

class CommentLikeCreate(BaseModel):
    comment_id: int

class CommentLikeResponse(BaseModel):
    id: int
    user_id: int
    comment_id: int
    created_at: datetime

    class Config:
        from_attributes = True
