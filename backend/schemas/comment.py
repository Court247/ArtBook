from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# ✅ Schema for creating a new comment

class CommentBase(BaseModel):
    content: str
class CommentCreate(BaseModel):
    post_id: str
    content: str

# ✅ Schema for updating a comment
class CommentUpdate(BaseModel):
    content: Optional[str] = None

# ✅ Schema for returning comments to the frontend
class CommentResponse(BaseModel):
    id: str
    user_id: str
    post_id: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True
