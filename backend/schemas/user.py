from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    display_name: str
    bio: Optional[str] = None          # changed: was required str
    avatar_url: Optional[str] = None

class UserCreate(UserBase):
    pass

class UserCreate(BaseModel):
    firebase_uid: str
    email: str
    display_name: str
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    
    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    firebase_uid: str
    email: str
    display_name: str
    bio: Optional[str]
    avatar_url: Optional[str]
    is_admin: bool
    created_at: datetime
    is_creator: bool

    class Config:
        from_attributes = True  # instead of orm_mode in Pydantic v2