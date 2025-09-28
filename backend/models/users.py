# models/users.py
from sqlalchemy import Column, String, DateTime, Enum
from datetime import datetime
from db.database import Base
import enum
from sqlalchemy.orm import relationship

class RoleEnum(str, enum.Enum):
    creator = "creator"
    admin = "admin"
    premium = "premium"
    regular = "regular"

class StatusEnum(str, enum.Enum):
    active = "active"
    suspended = "suspended"
    deleted = "deleted"
    banned = "banned"

class User(Base):
    __tablename__ = "users"

    firebase_uid = Column(String(128), primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    display_name = Column(String(255), nullable=True)
    bio = Column(String, default="")
    avatar_url = Column(String, default="")

    role = Column(Enum(RoleEnum), nullable=False, default=RoleEnum.regular)
    status = Column(Enum(StatusEnum), nullable=False, default=StatusEnum.active)

    created_at = Column(DateTime, default=datetime.utcnow)

    def is_creator(self) -> bool:
        return self.role == RoleEnum.creator

    def is_admin(self) -> bool:
        return self.role in [RoleEnum.admin, RoleEnum.creator]

    def is_active(self) -> bool:
        return self.status == StatusEnum.active

    def is_banned(self) -> bool:
        return self.status == StatusEnum.banned

    def is_suspended(self) -> bool:
        return self.status == StatusEnum.suspended

    # Relationships
    posts = relationship("Post", back_populates="author", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="author", cascade="all, delete-orphan")
    likes = relationship("Like", back_populates="user", cascade="all, delete-orphan")
    followers = relationship(
        "Follow", foreign_keys="Follow.following_id", back_populates="following", cascade="all, delete-orphan"
    )
    following = relationship(
        "Follow", foreign_keys="Follow.follower_id", back_populates="follower", cascade="all, delete-orphan"
    )