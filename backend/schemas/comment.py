from pydantic import BaseModel
from datetime import datetime

class CommentCreate(BaseModel):
    content: str

class CommentResponse(BaseModel):
    id: int
    post_id: int
    user_id: int
    content: str
    created_at: datetime

    class Config:
        orm_mode = True
