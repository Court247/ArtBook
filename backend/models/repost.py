from sqlalchemy import Column, Integer, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from db.database import Base

class Repost(Base):
    __tablename__ = "reposts"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    original_post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)
    quote = Column(Text, nullable=True)
    is_quote = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="reposts")
    original_post = relationship("Post", back_populates="reposts")
    #comments = relationship("Comment", back_populates="repost", cascade="all, delete-orphan")