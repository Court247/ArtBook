from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    firebase_uid: str
    email: str
    display_name: Optional[str] = None

class UserUpdate(BaseModel):
    display_name: Optional[str]
    bio: Optional[str]
    avatar_url: Optional[str]

class UserResponse(BaseModel):
    id: int
    firebase_uid: str
    email: str
    display_name: Optional[str]
    bio: Optional[str]
    avatar_url: Optional[str]

    class Config:
        orm_mode = True
