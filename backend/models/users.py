from sqlalchemy import Column, Integer, String, DateTime, Enum
from datetime import datetime
from db.database import Base
import enum
from sqlalchemy.orm import relationship


# ---------- Enums ----------
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


# ---------- Model ----------
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    firebase_uid = Column(String(128), unique=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    display_name = Column(String(255), nullable=True)
    bio = Column(String, nullable=True)
    avatar_url = Column(String, nullable=True)

    role = Column(Enum(RoleEnum), nullable=False, default=RoleEnum.regular)
    status = Column(Enum(StatusEnum), nullable=False, default=StatusEnum.active)
    created_at = Column(DateTime, default=datetime.utcnow)

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
    reports = relationship("PostFlag", back_populates="reporter", cascade="all, delete-orphan")
    comment_likes = relationship("CommentLike", back_populates="user", cascade="all, delete-orphan")
    # notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")
    