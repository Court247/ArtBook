from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class RepostCreate(BaseModel):
    original_post_id: int
    quote: Optional[str] = None  # optional quote text

class RepostResponse(BaseModel):
    id: int
    user_id: int
    original_post_id: int
    quote: Optional[str]
    is_quote: bool
    created_at: datetime

    class Config:
        from_attributes = True
