from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    display_name: str
    email: str
    bio: Optional[str] = None
    avatar_url: Optional[str] = None

class UserUpdate(BaseModel):
    display_name: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    firebase_uid: str
    display_name: str
    email: str
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    is_admin: bool = False
    is_creator: bool = False

    class Config:
        orm_mode = True
