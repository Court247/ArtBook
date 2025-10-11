# schemas/notification.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class NotificationCreate(BaseModel):
    recipient_id: int
    sender_id: int
    type: str
    post_id: Optional[int] = None
    comment_id: Optional[int] = None
    message: Optional[str] = None


class NotificationResponse(BaseModel):
    id: int
    recipient_id: int
    sender_id: int
    type: str
    message: Optional[str]
    post_id: Optional[int]
    comment_id: Optional[int]
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True
