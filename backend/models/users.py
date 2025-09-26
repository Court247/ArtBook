from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from db.database import Base

class User(Base):
    __tablename__ = "users"
    firebase_uid = Column(String(128), primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    display_name = Column(String(255), nullable=True)
    bio = Column(String, default="")
    avatar_url = Column(String, default="")
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_creator = Column(Boolean, default=False)

