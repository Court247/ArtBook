from sqlalchemy import Column, Integer, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from db.database import Base

class Like(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=True)
    repost_id = Column(Integer, ForeignKey("reposts.id", ondelete="CASCADE"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    __table_args__ = (
        UniqueConstraint("user_id", "post_id", name="unique_like"),
        UniqueConstraint("user_id", "repost_id", name="unique_repost_like"),
    )
   
    # Relationships
    user = relationship("User", back_populates="likes")
    post = relationship("Post", back_populates="likes")
    repost = relationship("Repost", back_populates="likes")