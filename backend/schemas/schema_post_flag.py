from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PostFlagCreate(BaseModel):
    post_id: int
    reason: Optional[str] = None

class PostFlagResponse(BaseModel):
    id: int
    post_id: int
    reported_by: int
    reason: Optional[str]
    reviewed: bool
    created_at: datetime

    class Config:
        from_attributes = True
