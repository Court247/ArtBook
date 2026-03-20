# schemas/user.py
from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import datetime
from enum import Enum
import re

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

    @field_validator("display_name")
    @classmethod
    def validate_display_name(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Display name cannot be empty")
        if len(v) > 50:
            raise ValueError("Display name must be 50 characters or fewer")
        if re.search(r'[<>"\'&]', v):
            raise ValueError("Display name contains invalid special characters: < > \" ' &")
        return v

class UserCreate(UserBase):
    firebase_uid: str
    # optional role during create (creator should not be self-assigned normally)
    role: Optional[RoleEnum] = RoleEnum.regular

class UserUpdate(BaseModel):
    display_name: str
    bio: Optional[str] = None
    avatar_url: Optional[str] = None

    @field_validator("display_name")
    @classmethod
    def validate_display_name(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Display name cannot be empty")
        if len(v) > 50:
            raise ValueError("Display name must be 50 characters or fewer")
        if re.search(r'[<>"\'&]', v):
            raise ValueError("Display name contains invalid special characters: < > \" ' &")
        return v

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