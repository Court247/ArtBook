# schemas/user.py
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from enum import Enum

class RoleEnum(str, Enum):
    creator = "creator"
    admin = "admin"
    premium = "premium"
    regular = "regular"

class UserBase(BaseModel):
    email: EmailStr
    display_name: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None

class UserCreate(UserBase):
    firebase_uid: str
    # optional role during create (creator should not be self-assigned normally)
    role: Optional[RoleEnum] = RoleEnum.regular

class UserUpdate(BaseModel):
    display_name: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None

class UserResponse(BaseModel):
    firebase_uid: str
    email: EmailStr
    display_name: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    role: RoleEnum
    created_at: Optional[datetime] = None

    class Config:
        # Pydantic v2 compatibility: allow reading attributes off ORM objects
        from_attributes = True
