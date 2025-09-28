# models/comment.py
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from db.database import Base

class Comment(Base):
    __tablename__ = "comments"

    id = Column(String(36), primary_key=True, index=True)  # UUID string
    user_id = Column(String(128), ForeignKey("users.firebase_uid", ondelete="CASCADE"), nullable=False)
    post_id = Column(String(36), ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    author = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")
    likes = relationship("Like", back_populates="comment", cascade="all, delete-orphan")