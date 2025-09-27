# models/users.py
from sqlalchemy import Column, String, DateTime, Enum
from datetime import datetime
from db.database import Base
import enum

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
