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

class StatusEnum(str, Enum):
    active = "active"
    suspended = "suspended"
    deleted = "deleted"
    banned = "banned"

class UserBase(BaseModel):
    email: EmailStr
    display_name: str
    bio: Optional[str] = None
    avatar_url: Optional[str] = None

class UserCreate(UserBase):
    firebase_uid: str
    # optional role during create (creator should not be self-assigned normally)
    role: Optional[RoleEnum] = RoleEnum.regular

class UserUpdate(BaseModel):
    display_name: str
    bio: Optional[str] = None
    avatar_url: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    firebase_uid: str
    email: EmailStr
    display_name: str
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    role: RoleEnum
    status: StatusEnum
    created_at: Optional[datetime] = None

    class Config:
        # Pydantic v2 compatibility: allow reading attributes off ORM objects
        from_attributes = True

class UserPublic(BaseModel):
    id: int
    firebase_uid: str
    display_name: str
    avatar_url: Optional[str]

    class Config:
        from_attributes = True