from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PostCreate(BaseModel):
    caption: Optional[str] = ""
    image_url: str

class PostResponse(BaseModel):
    id: int
    user_id: int
    caption: Optional[str]
    image_url: str
    created_at: datetime

    class Config:
        orm_mode = True
